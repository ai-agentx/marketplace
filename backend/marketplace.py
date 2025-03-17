import json
import logging
import os
import uuid
import uvicorn

from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("marketplace")

app = FastAPI(title="marketplace", description="rest api for the marketplace")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent_registry: Dict[str, Dict] = {}
agent_executions: Dict[str, List[Dict]] = {}


class AgentCapability(BaseModel):
    name: str
    description: str
    parameters: Optional[Dict] = None


class AgentRegistration(BaseModel):
    name: str
    description: str
    version: str
    author: str
    contact_email: Optional[str] = None
    homepage_url: Optional[str] = None
    api_endpoint: str
    capabilities: List[AgentCapability]
    auth_type: str = "none"
    auth_details: Optional[Dict] = None
    pricing_model: Optional[str] = None
    pricing_details: Optional[Dict] = None
    tags: List[str] = []

    @field_validator('auth_type')
    def validate_auth_type(cls, v):
        if v not in ["none", "api_key", "oauth"]:
            raise ValueError("auth_type must be one of: none, api_key, oauth")
        return v


class AgentExecutionRequest(BaseModel):
    agent_id: str
    input_data: Dict
    execution_parameters: Optional[Dict] = None
    auth_credentials: Optional[Dict] = None


class AgentSearchParams(BaseModel):
    capabilities: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    pricing_model: Optional[str] = None
    query: Optional[str] = None


API_KEYS = {
    "test_key": {"user_id": "test_user", "role": "admin"}
}


def get_current_user(api_key: str = Header(None, alias="X-API-Key")):
    if api_key is None:
        return {"user_id": "anonymous", "role": "guest"}

    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return API_KEYS[api_key]


@app.get("/")
async def root():
    return {"message": "marketplace"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/manifest")
async def get_manifest():
    manifest = {
        "schema_version": "v1",
        "name": "marketplace",
        "description": "A marketplace for discovering and executing AI agents",
        "auth": {
            "type": "api_key",
            "instructions": "Provide your API key in the X-API-Key header"
        },
        "api": {
            "type": "openapi",
            "url": f"{os.getenv('BASE_URL', 'http://localhost:9091')}/openapi.json"
        },
        "logo_url": f"{os.getenv('BASE_URL', 'http://localhost:9091')}/static/logo.png",
        "contact_email": "support@agentx.ai",
        "legal_info_url": f"{os.getenv('BASE_URL', 'http://localhost:9091')}/legal"
    }

    return manifest


@app.post("/agents", status_code=status.HTTP_201_CREATED)
async def register_agent(
        agent: AgentRegistration,
        current_user: Dict = Depends(get_current_user)
):
    agent_id = str(uuid.uuid4())

    agent_data = agent.model_dump()
    agent_data.update({
        "id": agent_id,
        "created_at": datetime.utcnow().isoformat(),
        "created_by": current_user["user_id"],
        "status": "active",
    })

    agent_registry[agent_id] = agent_data
    logger.info(f"Agent registered: {agent_id}")

    return {"agent_id": agent_id, "status": "registered", "agent": agent_data}


@app.get("/agents")
async def list_agents(
        search: AgentSearchParams = Depends(),
):
    results = []

    for agent_id, agent in agent_registry.items():
        if search.capabilities and not any(cap["name"] in search.capabilities for cap in agent["capabilities"]):
            continue

        if search.tags and not any(tag in search.tags for tag in agent["tags"]):
            continue

        if search.author and agent["author"] != search.author:
            continue

        if search.pricing_model and agent["pricing_model"] != search.pricing_model:
            continue

        if search.query:
            query = search.query.lower()
            if (query not in agent["name"].lower() and
                    query not in agent["description"].lower() and
                    not any(query in cap["name"].lower() or query in cap["description"].lower()
                            for cap in agent["capabilities"])):
                continue

        results.append(agent)

    return {"agents": results, "count": len(results)}


@app.get("/agents/search")
async def search_agents(
        query: Optional[str] = None,
        capabilities: Optional[str] = None,
        tags: Optional[str] = None,
):
    capabilities_list = capabilities.split(",") if capabilities else None
    tags_list = tags.split(",") if tags else None

    search_params = {
        "query": query,
        "capabilities": capabilities_list,
        "tags": tags_list
    }

    search_params = {k: v for k, v in search_params.items() if v is not None}

    # TBD: FIXME


@app.get("/agents/{agent_id}")
async def get_agent(
        agent_id: str,
):
    if agent_id not in agent_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID {agent_id} not found",
        )

    return agent_registry[agent_id]


@app.post("/agents/{agent_id}/execute")
async def execute_agent(
        agent_id: str,
        execution: AgentExecutionRequest,
        current_user: Dict = Depends(get_current_user)
):
    if agent_id not in agent_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID {agent_id} not found",
        )

    agent = agent_registry[agent_id]

    execution_id = str(uuid.uuid4())
    execution_record = {
        "id": execution_id,
        "agent_id": agent_id,
        "user_id": current_user["user_id"],
        "input": execution.input_data,
        "parameters": execution.execution_parameters,
        "status": "completed",
        "created_at": datetime.utcnow().isoformat(),
        "completed_at": datetime.utcnow().isoformat(),
        "result": {
            "message": f"Simulated response from agent '{agent['name']}'",
            "data": {"generated_output": f"This is a simulated response for input: {execution.input_data}"}
        }
    }

    if agent_id not in agent_executions:
        agent_executions[agent_id] = []
    agent_executions[agent_id].append(execution_record)

    return execution_record


@app.get("/agents/{agent_id}/executions")
async def list_agent_executions(
        agent_id: str,
        current_user: Dict = Depends(get_current_user)
):
    if agent_id not in agent_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID {agent_id} not found",
        )

    executions = agent_executions.get(agent_id, [])

    if current_user["role"] != "admin":
        executions = [e for e in executions if e["user_id"] == current_user["user_id"]]

    return {"executions": executions, "count": len(executions)}


@app.get("/agents/{agent_id}/executions/{execution_id}")
async def get_execution(
        agent_id: str,
        execution_id: str,
        current_user: Dict = Depends(get_current_user)
):
    if agent_id not in agent_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID {agent_id} not found",
        )

    executions = agent_executions.get(agent_id, [])
    execution = next((e for e in executions if e["id"] == execution_id), None)

    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Execution with ID {execution_id} not found",
        )

    if current_user["role"] != "admin" and execution["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this execution",
        )

    return execution


@app.delete("/agents/{agent_id}")
async def delete_agent(
        agent_id: str,
        current_user: Dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete agents",
        )

    if agent_id not in agent_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID {agent_id} not found",
        )

    agent = agent_registry.pop(agent_id)

    return {"message": f"Agent '{agent['name']}' (ID: {agent_id}) deleted successfully"}


@app.put("/agents/{agent_id}")
async def update_agent(
        agent_id: str,
        agent_update: AgentRegistration,
        current_user: Dict = Depends(get_current_user)
):
    if agent_id not in agent_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID {agent_id} not found",
        )

    existing_agent = agent_registry[agent_id]

    if current_user["role"] != "admin" and existing_agent["created_by"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this agent",
        )

    updated_data = agent_update.dict()
    existing_agent.update(updated_data)
    existing_agent["updated_at"] = datetime.utcnow().isoformat()

    return {"message": f"Agent '{existing_agent['name']}' updated successfully", "agent": existing_agent}


def main():
    api_key_str = os.getenv("API_KEYS")
    if api_key_str:
        try:
            global API_KEYS
            API_KEYS = json.loads(api_key_str)
        except json.JSONDecodeError:
            logger.error("Failed to parse API_KEYS environment variable as JSON")

    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "9091")),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )


if __name__ == "__main__":
    main()
