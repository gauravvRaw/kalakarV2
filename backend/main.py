import asyncio
import json
import os
import urllib.error
import urllib.request
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session as DbSession

from auth import CurrentUser, create_session, get_user_by_name, hash_password, verify_password
from database import Base, SessionLocal, engine, get_db
from models.post import Post
from models.session import Session
from models.user import User
from schemas import AuthResponse, Credentials, PostCreate, PostOut, PostUpdate, ProfileOut
from seed import seed_default_account


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_default_account(db)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Kalakaar Auth",
    description="Local name/password auth with per-user posts stored in SQLite.",
    lifespan=lifespan,
)


def _translate_audio_to_english(audio: bytes, filename: str, content_type: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Audio transcription is not configured. Set OPENAI_API_KEY on the backend.",
        )

    boundary = "----KalakaarAudioBoundary"
    safe_name = filename.replace('"', "")
    parts = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nwhisper-1\r\n".encode(),
        (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
            f"filename=\"{safe_name}\"\r\nContent-Type: {content_type}\r\n\r\n"
        ).encode(),
        audio,
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    request = urllib.request.Request(
        "https://api.openai.com/v1/audio/translations",
        data=b"".join(parts),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            result = json.loads(response.read())
            transcript = result.get("text", "").strip()
            if not transcript:
                raise HTTPException(status_code=422, detail="No speech was detected in the recording.")
            return transcript
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise HTTPException(status_code=502, detail=f"Audio transcription failed: {detail[:300]}") from error
    except urllib.error.URLError as error:
        raise HTTPException(status_code=502, detail="Could not reach the transcription service.") from error


@app.post("/audio/translate")
async def translate_audio(request: Request):
    audio = await request.body()
    if not audio:
        raise HTTPException(status_code=400, detail="Audio file is empty.")
    if len(audio) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Audio files must be 25 MB or smaller.")

    content_type = request.headers.get("content-type", "audio/mp4").split(";", 1)[0]
    filename = request.headers.get("x-audio-filename", "voice-recording.m4a")
    try:
        transcript = await asyncio.to_thread(
            _translate_audio_to_english, audio, filename, content_type
        )
    except HTTPException:
        raise
    return {"text": transcript, "language": "en"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


def _auth_payload(db: DbSession, user: User) -> AuthResponse:
    return AuthResponse(token=create_session(db, user), profile=ProfileOut.model_validate(user))


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/auth/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(body: Credentials, db: DbSession = Depends(get_db)):
    name = body.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    if get_user_by_name(db, name):
        raise HTTPException(status_code=409, detail="That name is already taken")

    user = User(
        name=name,
        password_hash=hash_password(body.password),
        location="",
        cluster="",
        avatar_url="",
        verified=False,
        is_default=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _auth_payload(db, user)


@app.post("/auth/login", response_model=AuthResponse)
def login(body: Credentials, db: DbSession = Depends(get_db)):
    user = get_user_by_name(db, body.name)
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect name or password")
    return _auth_payload(db, user)


@app.post("/auth/logout")
def logout(user: CurrentUser, db: DbSession = Depends(get_db)):
    db.query(Session).filter(Session.user_id == user.id).delete()
    db.commit()
    return {"ok": True}


@app.get("/auth/me", response_model=ProfileOut)
def current_profile(user: CurrentUser):
    return user


@app.get("/posts", response_model=list[PostOut])
def list_posts(user: CurrentUser, db: DbSession = Depends(get_db)):
    return (
        db.query(Post)
        .filter(Post.user_id == user.id)
        .order_by(Post.created_at.desc())
        .all()
    )


@app.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(body: PostCreate, user: CurrentUser, db: DbSession = Depends(get_db)):
    post = Post(user_id=user.id, **body.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int, user: CurrentUser, db: DbSession = Depends(get_db)):
    post = db.get(Post, post_id)
    if post is None or post.user_id != user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.patch("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, body: PostUpdate, user: CurrentUser, db: DbSession = Depends(get_db)):
    post = db.get(Post, post_id)
    if post is None or post.user_id != user.id:
        raise HTTPException(status_code=404, detail="Post not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, user: CurrentUser, db: DbSession = Depends(get_db)):
    post = db.get(Post, post_id)
    if post is None or post.user_id != user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
