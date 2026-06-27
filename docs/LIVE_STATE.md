# LIVE_STATE.md — Current Project Memory (Always Up-to-Date)

> **This is the single most important file for resuming work.**  
> It is routinely updated at the end of significant work or sessions.  
> A fresh Grok session should read this *after* AGENTS.md.

**Last Updated**: 2026-06-27 15:45 (Routine context saving system fully implemented)

---

## Current Goal
Build the azure-ai-pantheon orchestration layer using Microsoft Agent Framework (MAF) to manage and coordinate Hermes Agent and OpenClaw instances running in Azure Container Apps.

## What We Are Working On Right Now
- Establishing a reliable, routine process for saving project memory so almost nothing is lost after reboots.
- The "Routine Context Saving Protocol" has been designed and implemented.

## Last Major Accomplishments
- 2026-06-27: Cloned the repo into the project workspace.
- 2026-06-27: Designed and implemented full **Routine Context Saving Protocol**:
  - Created `docs/LIVE_STATE.md` (always-current snapshot)
  - Created `docs/SESSION_LOG.md` (append-only history)
  - Created `scripts/save-context.ps1` (easy routine saver)
  - Updated `AGENTS.md` with detailed saving protocol
  - Added `docs/TODOS.md` for persistent tasks
  - Enhanced resume script
  - Committed everything with good messages.

## Next Immediate Steps
1. Study the existing `azure-hermes-factory` and `oc-agent-main` implementations in detail.
2. Research current MAF patterns for multi-agent orchestration and ACA deployment.
3. Propose high-level architecture for the Pantheon conductor.
4. Decide on implementation language for MAF layer (Python vs .NET/C#).
5. (Ongoing) Use the new save-context routine after every meaningful piece of work.

## Current Open Questions / Risks
- How will MAF "talk to" existing Hermes/OpenClaw runtimes? (HTTP endpoints, MCP, A2A protocol, direct calls, etc.)
- Will we evolve the existing Docker + Bicep factories or create new ones specific to Pantheon?
- Scope: Is Pantheon only the orchestrator, or does it also include improved deployment for the agents themselves?
- Observability integration with Microsoft Foundry.

## Key Facts That Must Not Be Lost
- Workspace: C:\Users\openclaw\Documents\grok
- GitHub user/org: clgintellicloud-hub
- Existing agent deployments use Node.js wrappers around `hermes-agent` CLI inside ACA containers.
- gh CLI is already authenticated with repo scope.
- Strong preference for filesystem-based context that survives reboots.

## Active Todos / Work Items
(See docs/TODOS.md or the live todo list in the current session)

---

**How to keep this file accurate:**
- This file gets updated (via search_replace or write) whenever major progress happens.
- It is deliberately short and scannable.
- Timestamp + summary of changes is added on every update.
