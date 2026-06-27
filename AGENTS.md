# AGENTS.md

> **This file exists so that any future Grok (or other AI coding agent) session can quickly recover full project context after a computer reboot, new terminal, or new conversation.**

## Project Identity
- **Name**: azure-ai-pantheon
- **Tagline**: AI Agent orchestration
- **Repo**: https://github.com/clgintellicloud-hub/azure-ai-pantheon.git
- **Workspace Path**: `C:\Users\openclaw\Documents\grok`
- **Purpose**: Build a management and orchestration layer ("Pantheon") for multiple AI agents — specifically **Hermes Agent** and **OpenClaw** — running as containerized workloads inside **Azure Container Apps (ACA)**, with **Microsoft Agent Framework (MAF)** as a primary orchestration technology.

## Core Objective
Create a system that can:
- Deploy, manage, version, scale, and observe Hermes and OpenClaw agents on ACA.
- Use Microsoft Agent Framework (MAF) for higher-level coordination, workflows, routing between agent types, unified interfaces, and observability.
- Act as the "conductor" or meta-orchestrator on top of the lower-level agent runtimes.

## Current State (as of 2026-06-27)
- Repository was just cloned into this directory.
- Contains only an initial commit with a minimal README.
- No application code, infrastructure, or detailed docs yet in this repo.
- Active development workspace is this folder.

## Critical Related Codebases (Prior Work)
These contain existing patterns the Pantheon should build upon or evolve:

1. **Azure Hermes Factory**  
   Path: `C:\Users\openclaw\Documents\claude-code\azure-hermes-factory\`  
   - Bicep-based IaC for ACA (dev + prod resource groups)  
   - ACR, Container Apps Environment, multiple agents  
   - Dockerized wrappers for Hermes + "analyst" + generic OpenClaw-style agents  
   - Uses Node.js HTTP shim that spawns the real `hermes-agent` CLI  
   - Scripts for build, revisions, rollback, smoke tests

2. **OC Agent Main**  
   Path: `C:\Users\openclaw\Downloads\oc-agent-main\oc-agent-main\`  
   - Very similar structure to the above, more OpenClaw-focused configs

These two should be studied when designing the Pantheon layer.

## Key Technologies
- **Microsoft Agent Framework (MAF)** — Primary framework for the orchestration layer (Python and/or .NET). Unifies concepts from Semantic Kernel + AutoGen. Supports workflows, agents, middleware, sessions, MCP, strong telemetry.
- **Azure Container Apps (ACA)** — Runtime platform for the individual Hermes/OpenClaw containers and potentially MAF orchestrators.
- **Hermes Agent** (Nous Research) — Self-improving autonomous agent with skills, learning loop, memory. Currently wrapped and deployed via the factories.
- **OpenClaw** — Another popular autonomous agent platform being run side-by-side.
- **Bicep** — Current IaC language.
- **Docker** — For packaging agents.
- **Microsoft Foundry** — Likely target for observability and higher-level agent features.
- GitHub CLI (`gh`) — Already authenticated as `clgintellicloud-hub`.

## Architecture Direction (Early Thinking)
- Lower layer: Existing containerized Hermes and OpenClaw instances on ACA (from the factories).
- Orchestration layer: MAF agents/workflows that can discover, invoke, route to, monitor, and compose the above agents.
- Possible patterns:
  - MAF as supervisor / router
  - Hermes/OpenClaw exposed via HTTP or MCP and treated as tools or sub-agents
  - Unified control plane for versioning, scaling, A/B testing (leveraging ACA revisions)
  - Strong observability (OTel → Application Insights → Foundry)

## How to Resume Work After Reboot or New Session
When you (Grok or another agent) start fresh:

1. Change to the project directory:
   ```powershell
   cd "C:\Users\openclaw\Documents\grok"
   ```

2. **Read the following files first** (in this order):
   - `AGENTS.md` (this file)
   - `README.md`
   - Any files under `docs/`

3. Explore the filesystem:
   ```powershell
   Get-ChildItem -Force
   Get-ChildItem -Recurse -Depth 2
   ```

4. Review prior work (very important):
   - List and read key files from `..\claude-code\azure-hermes-factory\`
   - Review the `oc-agent-main` folder

5. Ask the user or review recent commits for the latest task.

6. (Recommended) Run any local resume helper if present:
   ```powershell
   .\scripts\resume-context.ps1
   ```

## Documentation Conventions in This Repo
- `AGENTS.md` — Primary context file for AI agents (update this often).
- `README.md` — High-level for humans + points to AGENTS.md.
- `docs/` — Detailed architecture, decisions, status, runbooks.
- Keep status, decisions, and current goals in committed Markdown files.
- Update this file whenever major context changes (architecture decisions, new related code locations, major progress).

## Recommended Practices
- Commit context files early and often (`AGENTS.md`, `docs/*.md`).
- Use clear, self-contained Markdown so a fresh session can understand the project without the full chat history.
- When making progress, summarize changes back into `docs/STATUS.md` or this file.

## Routine Context Saving Protocol (Critical for No Data Loss)

This is the **official process** to ensure almost nothing important is lost after a reboot or new session.

### 1. Primary Files That Must Stay Current
- `docs/LIVE_STATE.md` — The single source of "what is happening RIGHT NOW". Short, scannable, frequently overwritten with latest status.
- `docs/SESSION_LOG.md` — Append-only historical record of work sessions.
- `AGENTS.md` — Only updated for major structural changes (new related repos, big architecture shifts, etc.).
- `docs/DECISIONS.md` — Record important "why" decisions as they are made.
- `docs/STATUS.md` — Higher-level overview (less frequently updated than LIVE_STATE).

### 2. When to Save Context (The Triggers)
Save context **routinely** at these points:
- End of a focused work block (e.g., "I just finished analyzing the Bicep modules").
- After any significant decision or discovery.
- Before ending a long session or when the user says "save context", "update state", or "commit the memory".
- At the end of implementing a feature or fixing something important.

### 3. How to Save (The Method)
**Preferred method (agent or human):**
```powershell
cd "C:\Users\openclaw\Documents\grok"
powershell -ExecutionPolicy Bypass -File .\scripts\save-context.ps1 `
  -Summary "Summarized what was just accomplished" `
  -FocusArea "MAF research / Hermes factory analysis" `
  -NextSteps "Next step 1\nNext step 2"
```

The script will:
- Update `docs/LIVE_STATE.md` with the new current state and timestamp.
- Append a structured entry to `docs/SESSION_LOG.md`.
- Stage the important context files.
- Print a suggested git commit message.

**Alternative (direct agent action):**
I can directly edit `docs/LIVE_STATE.md` and append to `docs/SESSION_LOG.md` using tools, then stage + commit. This is often cleaner during active work.

### 4. Git Discipline
- Context changes should almost always be committed.
- Use clear messages starting with `chore(context): ...`
- This makes `git log` itself a useful recovery tool.

### 5. Agent Behavior Rules (For Me)
When I am working on this project:
- I will proactively keep `docs/LIVE_STATE.md` accurate.
- After any non-trivial progress, I will either run the save script or directly update the live state files.
- At the end of my response, if meaningful work happened, I will offer: "Would you like me to save the current context now?"
- I will not rely solely on chat history.

### 6. User Actions That Help
- Say "save context" or "update live state" at natural stopping points.
- Review `docs/LIVE_STATE.md` occasionally and correct anything that feels outdated.
- Do not delete or heavily refactor these files without updating the protocol in this AGENTS.md.

Following this protocol means that even if the entire conversation history disappears, a new session that reads `AGENTS.md` + `docs/LIVE_STATE.md` + recent SESSION_LOG entries will have excellent continuity.
- For task tracking, prefer files in `docs/` or `TODO.md` alongside any in-session todo tools.

## Branching Strategy

**All feature branches MUST use the `grok/` prefix.**

### Rules
- `main` remains `main` (never prefixed).
- Feature, enhancement, fix, refactor, docs, etc. branches must be named:
  - `grok/<kebab-case-description>`
- Examples:
  - `grok/add-maf-orchestrator`
  - `grok/hermes-openclaw-integration`
  - `grok/improve-aca-deployment`
  - `grok/context-persistence-updates`
- Never use bare names like `feature-x`, `my-work`, etc.

### How to Create a Feature Branch
Use the provided helper script (recommended):

```powershell
cd "C:\Users\openclaw\Documents\grok"
.\scripts\create-grok-branch.ps1 add-maf-orchestrator
# or with bypass if needed:
powershell -ExecutionPolicy Bypass -File .\scripts\create-grok-branch.ps1 "your-feature-name"
```

The script normalizes the name and enforces the `grok/` prefix.

Alternatively (manual):
```powershell
git checkout -b grok/your-feature-name
```

### Git Alias (Optional Convenience)
The alias is already configured in this working tree:
```powershell
git grok-branch add-maf-orchestrator
```

**Note**: The alias is basic and accepts only the feature name (it creates + checks out `grok/<name>`).  
For flags like `-NoCheckout`, call the script directly:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\create-grok-branch.ps1 "add-maf-orchestrator" -NoCheckout
```

### Why the Prefix?
- Clearly identifies branches created as part of Grok-assisted development in this project.
- Makes it easy to filter and manage work in GitHub, PRs, and local checkout.
- Enforces team / agent consistency.

This rule applies to **all current and future feature branches**. If you see a non-`grok/` feature branch, rename it:
```powershell
git branch -m old-name grok/old-name
```

## Contact / Ownership
- GitHub account context: `clgintellicloud-hub`
- User frequently works with Hermes, OpenClaw, and Azure agent deployments.

---

**Last updated**: 2026-06-27 (initial creation to preserve context across sessions)

**Next step for any new session**: Read this file completely, then explore the related factory directories.
