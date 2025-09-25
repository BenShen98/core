"""Mock Balena Supervisor API for testing Home Assistant container control.

This module provides a FastAPI app that simulates the Balena Supervisor endpoints
for application state and container service control (start, stop, restart).
"""

import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Simple in-memory container state
appName = "self-prod"
state = {
    appName: {
        "appId": 2090997,
        "commit": "d3e3b4263d7ad3d2ba80256d7c891a55",
        "services": {
            "ha": {
                "status": "Running",
                "releaseId": 3453009,
                "downloadProgress": None,
            },
            "debugger": {
                "status": "Running",
                "releaseId": 3453009,
                "downloadProgress": None,
            },
            "avahi": {
                "status": "Running",
                "releaseId": 3453009,
                "downloadProgress": None,
            },
        },
    }
}


class ContainerControlRequestBody(BaseModel):
    """Request body for stop/start/restart a container service."""

    serviceName: str  # noqa: N815


@app.get("/v2/applications/state")
async def get_applications_state():
    """Mocking the /v2/applications/state endpoint of Balena Supervisor."""
    return state


@app.post("/v2/applications/{appid}/{action}")
async def control_application(
    appid: int, action: str, body: ContainerControlRequestBody
):
    """Mocking the /v2/applications/{appid}/start-service, stop-service, restart-service endpoint of Balena Supervisor."""
    if appid != state[appName]["appId"]:
        raise HTTPException(status_code=404, detail="App not found")

    if action not in ["start-service", "stop-service", "restart-service"]:
        raise HTTPException(status_code=400, detail="Invalid action")

    if body.serviceName not in state[appName]["services"]:
        raise HTTPException(status_code=404, detail="Service not found")

    if action == "start-service":
        state[appName]["services"][body.serviceName] = "Running"
    elif action == "stop-service":
        state[appName]["services"][body.serviceName] = "Stopped"
    elif action == "restart-service":
        state[appName]["services"][body.serviceName] = "Running"

    return "OK"


if __name__ == "__main__":
    host = os.environ.get("MOCK_SUPERVISOR_HOST", "0.0.0.0")
    port = int(os.environ.get("BALENA_SUPERVISOR_PORT", "8080"))
    auth_key = os.environ.get("BALENA_SUPERVISOR_API_KEY", "testkey")
    uvicorn.run("mock_balena:app", host=host, port=port, reload=True)
