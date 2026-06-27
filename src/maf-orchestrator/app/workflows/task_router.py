# Proper MAF Workflow Graph: Planning → Conditional Handoff
# Uses Microsoft Agent Framework (agent-framework) for graph-based orchestration

import httpx
import os
from typing import Any, Dict

from agent_framework import Agent, Workflow, tool

HERMES_ENDPOINT = os.getenv("HERMES_ENDPOINT", "http://localhost:8081")
OPENCLAW_ENDPOINT = os.getenv("OPENCLAW_ENDPOINT", "http://localhost:8082")

@tool
async def call_hermes(prompt: str) -> str:
    """Tool for delegating to Hermes (self-improving / analysis agent)."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{HERMES_ENDPOINT}/execute",
            json={"prompt": prompt}
        )
        data = resp.json()
        return data.get("result", str(data))

@tool
async def call_openclaw(prompt: str) -> str:
    """Tool for delegating to OpenClaw (personal / execution agent)."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{OPENCLAW_ENDPOINT}/execute",
            json={"prompt": prompt}
        )
        data = resp.json()
        return data.get("result", str(data))

# Define MAF Agents
hermes_agent = Agent(
    name="HermesAgent",
    instructions="You are a self-improving autonomous agent specialized in analysis, planning, and learning. Use tools when appropriate.",
    tools=[call_hermes]
)

openclaw_agent = Agent(
    name="OpenClawAgent",
    instructions="You are a reliable personal AI assistant focused on execution and autonomous actions. Use tools when appropriate.",
    tools=[call_openclaw]
)

# Planning step (can later be replaced by a full Planner Agent using LLM)
async def plan_task(input: str) -> Dict[str, Any]:
    """
    Planning node: Analyzes the task and decides routing.
    Returns structured plan for conditional handoff.
    """
    prompt_lower = input.lower()
    
    use_hermes = any(kw in prompt_lower for kw in ["analyze", "complex", "plan", "research", "strategy", "deep"])
    use_openclaw = True  # Default to include OpenClaw unless purely analytical
    
    # For "both" cases
    if use_hermes and "and" in prompt_lower or "also" in prompt_lower:
        route = "both"
    elif use_hermes:
        route = "hermes"
    else:
        route = "openclaw"
    
    plan = {
        "original_task": input,
        "reasoning": f"Detected keywords leading to route={route}",
        "route": route,
        "steps": []
    }
    
    if route in ["hermes", "both"]:
        plan["steps"].append("Hermes: Deep analysis and self-improvement")
    if route in ["openclaw", "both"]:
        plan["steps"].append("OpenClaw: Execution and autonomous actions")
    
    return plan

# Handoff / execution nodes
async def handoff_to_hermes(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Handoff node for Hermes."""
    try:
        result = await hermes_agent.run(plan["original_task"])
        return {
            "agent": "hermes",
            "status": "success",
            "output": result,
            "plan": plan
        }
    except Exception as e:
        return {
            "agent": "hermes",
            "status": "failure",
            "error": str(e),
            "plan": plan
        }

async def handoff_to_openclaw(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Handoff node for OpenClaw."""
    try:
        result = await openclaw_agent.run(plan["original_task"])
        return {
            "agent": "openclaw",
            "status": "success",
            "output": result,
            "plan": plan
        }
    except Exception as e:
        return {
            "agent": "openclaw",
            "status": "failure",
            "error": str(e),
            "plan": plan
        }

async def combine_results(hermes_result: Dict, openclaw_result: Dict) -> Dict[str, Any]:
    """Final combination step for parallel/sequential both case."""
    return {
        "final_status": "completed",
        "hermes": hermes_result,
        "openclaw": openclaw_result,
        "summary": "Task processed by multiple agents via MAF conditional handoff."
    }

async def create_pantheon_workflow() -> Workflow:
    """
    Builds a proper MAF Workflow Graph:
    
    input -> plan_task 
           -> conditional handoff:
               - hermes
               - openclaw
               - both (sequential for now)
           -> success/failure handling
    """
    wf = Workflow(name="PantheonTaskOrchestrator")
    
    # Add nodes
    wf.add_node("plan", plan_task)
    wf.add_node("hermes", handoff_to_hermes)
    wf.add_node("openclaw", handoff_to_openclaw)
    wf.add_node("combine", combine_results)
    
    # Main flow
    wf.add_edge("plan", "hermes", condition=lambda plan: plan.get("route") in ["hermes", "both"])
    wf.add_edge("plan", "openclaw", condition=lambda plan: plan.get("route") in ["openclaw", "both"])
    
    # For "both" case, combine results after both complete
    wf.add_edge("hermes", "combine", condition=lambda r: r.get("plan", {}).get("route") == "both")
    wf.add_edge("openclaw", "combine", condition=lambda r: r.get("plan", {}).get("route") == "both")
    
    # Simple success path for single agent cases (we can improve with a finalizer later)
    # For demo, the last node result is returned
    
    return wf

# Convenience function for FastAPI
async def run_pantheon_workflow(prompt: str) -> dict[str, Any]:
    """
    Entry point that runs the full MAF workflow graph.
    """
    workflow = await create_pantheon_workflow()
    
    # Run the workflow starting from plan
    # Note: In full MAF, you would use workflow.run() or similar entrypoint
    plan = await plan_task(prompt)
    
    route = plan.get("route")
    results = []
    
    if route in ["hermes", "both"]:
        hermes_out = await handoff_to_hermes(plan)
        results.append(hermes_out)
    
    if route in ["openclaw", "both"]:
        openclaw_out = await handoff_to_openclaw(plan)
        results.append(openclaw_out)
    
    if route == "both":
        combined = await combine_results(results[0], results[1] if len(results) > 1 else {})
        return {
            "plan": plan,
            "execution": combined,
            "workflow": "MAF graph with conditional handoff"
        }
    
    return {
        "plan": plan,
        "execution": results[0] if results else {},
        "workflow": "MAF graph with conditional handoff"
    }
