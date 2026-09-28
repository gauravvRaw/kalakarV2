# Graph Report - Kalakaar  (2026-09-27)

## Corpus Check
- 61 files · ~51,957 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 367 nodes · 779 edges · 21 communities (15 shown, 6 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 20 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9b2a1366`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- useLanguage
- ProductContext.tsx
- package.json
- What You Must Do When Invoked
- client.ts
- expo
- LanguageContext.tsx
- graphify reference: extra exports and benchmark
- AGENTS.md
- graphify reference: query, path, explain
- tsconfig.json
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- rules/graphify.md
- workflows/graphify.md
- extraction-spec.md

## God Nodes (most connected - your core abstractions)
1. `useLanguage()` - 25 edges
2. `useProduct()` - 23 edges
3. `react-native` - 21 edges
4. `react` - 20 edges
5. `COLORS` - 19 edges
6. `@expo/vector-icons` - 14 edges
7. `User` - 12 edges
8. `What You Must Do When Invoked` - 12 edges
9. `expo` - 11 edges
10. `Post` - 11 edges

## Surprising Connections (you probably didn't know these)
- `MainNavigator()` --calls--> `useProduct()`  [EXTRACTED]
  App.tsx → src/context/ProductContext.tsx
- `create_session()` --uses--> `User`  [INFERRED]
  backend/auth.py → backend/models/user.py
- `get_user_by_name()` --uses--> `User`  [INFERRED]
  backend/auth.py → backend/models/user.py
- `get_current_user()` --uses--> `Session`  [INFERRED]
  backend/auth.py → backend/models/session.py
- `get_current_user()` --uses--> `User`  [INFERRED]
  backend/auth.py → backend/models/user.py

## Import Cycles
- None detected.

## Communities (21 total, 6 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.06
Nodes (69): asyncio, create_session(), get_current_user(), get_user_by_name(), hash_password(), DbSession, verify_password(), Base (+61 more)

### Community 1 - "useLanguage"
Cohesion: 0.12
Nodes (41): @expo/vector-icons, react, react-native, AudioButton(), AudioButtonProps, styles, Badge(), BadgeProps (+33 more)

### Community 2 - "ProductContext.tsx"
Cohesion: 0.11
Nodes (34): FilterPillsProps, ProductCardProps, ProductContext, ProductContextType, ProductProvider(), INITIAL_PRODUCTS, SAMPLE_CRAFTS, analyzeAudioMetadata() (+26 more)

### Community 3 - "package.json"
Cohesion: 0.05
Nodes (43): { defineConfig }, expoConfig, dependencies, expo, expo-audio, expo-font, expo-image-picker, @expo/metro-runtime (+35 more)

### Community 4 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 5 - "client.ts"
Cohesion: 0.15
Nodes (21): ref_expo_constants, ApiUnreachableError, checkBackendHealth(), createPostRequest(), fetchPosts(), getApiBaseUrl(), hostFromExpo(), isNetworkFailure() (+13 more)

### Community 6 - "expo"
Cohesion: 0.10
Nodes (20): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, predictiveBackGestureEnabled, expo (+12 more)

### Community 8 - "LanguageContext.tsx"
Cohesion: 0.18
Nodes (15): App(), MainNavigator(), styles, expo, expo-status-bar, Header(), styles, LANGUAGE_OPTIONS (+7 more)

### Community 9 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 10 - "AGENTS.md"
Cohesion: 0.29
Nodes (6): Building with EAS, Commands, Expo has changed — do not trust your training data, graphify, Navigation & Routing, Rules

### Community 11 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 12 - "tsconfig.json"
Cohesion: 0.40
Nodes (4): expo/tsconfig.base, compilerOptions, strict, extends

### Community 13 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 14 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 15 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

## Knowledge Gaps
- **134 isolated node(s):** `styles`, `name`, `slug`, `version`, `orientation` (+129 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 172 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react-native` connect `useLanguage` to `LanguageContext.tsx`, `ProductContext.tsx`, `package.json`, `client.ts`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `react` connect `useLanguage` to `LanguageContext.tsx`, `ProductContext.tsx`, `package.json`, `client.ts`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **What connects `styles`, `name`, `slug` to the rest of the system?**
  _134 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06493506493506493 - nodes in this community are weakly interconnected._
- **Should `useLanguage` be split into smaller, more focused modules?**
  _Cohesion score 0.12099213551119177 - nodes in this community are weakly interconnected._
- **Should `ProductContext.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.11097560975609756 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.045454545454545456 - nodes in this community are weakly interconnected._