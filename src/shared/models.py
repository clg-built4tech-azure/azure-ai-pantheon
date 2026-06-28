from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TaskRequest(BaseModel):
    prompt: str
    metadata: Dict[str, Any] = {}
    checkpoint_id: Optional[str] = None

class Plan(BaseModel):
    original_task: str
    reasoning: str
    route: str
    steps: List[str]

class AgentResult(BaseModel):
    agent: str
    status: str
    output: Any
    plan: Optional[Plan] = None

class WorkflowResult(BaseModel):
    plan: Plan
    execution: Any
    checkpoint_id: Optional[str] = None
    summary: str
    agents_used: List[str] = []

class HealthResponse(BaseModel):
    status: str
    framework: str
    version: str
