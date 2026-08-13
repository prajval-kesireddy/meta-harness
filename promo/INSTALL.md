# Install list: Video harness

Run these in the project folder. Install ONLY these; piling on extra skills makes the agent worse, not better.

```bash
npx skills add remotion-dev/skills
```
Official Remotion best-practices skill: video-in-React idioms, composition structure, render pipeline.

```bash
npx skills add obra/superpowers
```
Verification gates: never claim a render is done without checking the actual output file.

```bash
winget install ffmpeg  (or: brew install ffmpeg)
```
ffmpeg (CLI, not MCP): Every path ends in ffmpeg: concat, audio mux, format conversion, thumbnail extraction for audits.

## Registry picks (rated, current)

- **ffmpeg** (9/10): Every video path terminates in ffmpeg: concat, mux, convert, extract stills for the frame loop. Install: `winget install ffmpeg` (verified 2026-08-13)
- **context7 MCP** (8/10): Current library docs on demand; stops the agent from writing against a framework version that no longer exists. Install: `claude mcp add context7 -- npx -y @upstash/context7-mcp` (verified 2026-08-13)
