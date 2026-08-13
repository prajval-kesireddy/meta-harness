# Install list: Website harness

Run these in the project folder. Install ONLY these; piling on extra skills makes the agent worse, not better.

```bash
claude plugin marketplace add anthropics/skills && claude plugin install frontend-design
```
Anthropic's own frontend-design skill: kills the generic AI aesthetic at the token level (typography, spacing, color discipline).

```bash
npx skills add obra/superpowers
```
Process backbone: brainstorming before building, test-driven loops, verification-before-completion gates.

```bash
npx skills add nextlevelbros/gsap-skills
```
GSAP core + ScrollTrigger skills, for motion that feels engineered instead of CSS-transition slop.

```bash
claude mcp add playwright -- npx -y @playwright/mcp@latest
```
playwright: The screenshot-audit loop needs a browser the agent can drive. This is the single highest-leverage install in the whole harness: without it the agent designs blind.

## Registry picks (rated, current)

- **playwright MCP** (10/10): Gives the agent eyes. Every design loop depends on it; the highest-leverage single install for visual work. Install: `claude mcp add playwright -- npx -y @playwright/mcp@latest` (verified 2026-08-13)
- **context7 MCP** (8/10): Current library docs on demand; stops the agent from writing against a framework version that no longer exists. Install: `claude mcp add context7 -- npx -y @upstash/context7-mcp` (verified 2026-08-13)
- **Vercel deploy (CLI or MCP)** (8/10): The shortest reliable path from local build to live URL; the ship phase's default. Install: `npm i -g vercel` (verified 2026-08-13)
- **Gemini image gen (Vertex AI)** (8/10): Current best quality-per-cent for still generation (~$0.13/2K image); the visual pipeline default where a harness needs original imagery. Install: `gcloud auth application-default login, then REST to gemini-3-pro-image` (verified 2026-08-13)
