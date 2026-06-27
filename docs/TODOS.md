# TODOS.md — Persistent Task List for azure-ai-pantheon

This file holds the project's task list in a way that survives reboots. 
It can be updated by the agent (via tools) or the user.

Use simple markdown checkboxes. Move completed items to a "Done" section or delete them.

## Current / Active
- [ ] Deep-dive into existing `azure-hermes-factory` Bicep and Docker code
- [ ] Research Microsoft Agent Framework (MAF) patterns for ACA + multi-agent orchestration
- [ ] Design high-level architecture for Pantheon (MAF as conductor for Hermes + OpenClaw)
- [ ] Decide on primary language for MAF implementation (Python or .NET)
- [ ] Prototype basic MAF agent that can call an external Hermes/OpenClaw instance

## Backlog
- Improve container wrappers for better health, observability, and MCP exposure
- Add unified control plane features (scaling, versioning via ACA revisions)
- Integrate telemetry with Microsoft Foundry
- Create deployment templates specific to the Pantheon layer

## Done
- [x] 2026-06-27: Set up robust reboot-safe context system (AGENTS.md + LIVE_STATE.md + save scripts + git discipline)

## Notes
- For short-term in-session tasks, the `todo_write` tool can be used, then persisted here at save time.
- Keep this list reasonably short and actionable.
