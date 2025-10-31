"""
FastAPI Web Service for Robot Driver
Provides HTTP endpoints to execute automation tasks remotely
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal
import asyncio
import os

from robot_driver import search_product_price
from ai_robot_driver import AIRobotDriver

app = FastAPI(
    title="Robot Driver Automation API",
    description="Automate web tasks using Playwright and AI",
    version="1.0.0"
)


class TaskRequest(BaseModel):
    """Request model for automation tasks"""
    message: str = Field(
        ...,
        description="The task or goal to execute (e.g., 'Find the price of wireless mouse on Amazon')",
        example="Find the price of wireless mouse on Amazon"
    )
    mode: Literal["basic", "ai"] = Field(
        default="basic",
        description="Execution mode: 'basic' for fixed task, 'ai' for dynamic AI-powered execution"
    )
    max_steps: Optional[int] = Field(
        default=15,
        description="Maximum steps for AI mode (ignored in basic mode)",
        ge=1,
        le=50
    )


class TaskResponse(BaseModel):
    """Response model for automation tasks"""
    success: bool
    message: str
    mode: str
    steps_taken: Optional[int] = None
    price: Optional[str] = None
    product: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Robot Driver Automation API",
        "version": "1.0.0",
        "endpoints": {
            "POST /execute": "Execute an automation task",
            "GET /health": "Health check endpoint",
            "GET /docs": "Interactive API documentation"
        },
        "modes": {
            "basic": "Fixed task execution (product search)",
            "ai": "AI-powered dynamic task execution (requires GEMINI_API_KEY)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    gemini_configured = bool(os.getenv("GEMINI_API_KEY"))

    return {
        "status": "healthy",
        "features": {
            "basic_mode": True,
            "ai_mode": gemini_configured
        }
    }


@app.post("/execute", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """
    Execute an automation task

    Args:
        request: Task request with message and execution mode

    Returns:
        Task execution result with success status and details
    """
    try:
        if request.mode == "basic":
            # Execute basic fixed task
            result = await search_product_price("wireless mouse")

            return TaskResponse(
                success=result["success"],
                message=result["message"],
                mode="basic",
                price=result.get("price"),
                product=result.get("product")
            )

        elif request.mode == "ai":
            # Check if API key is configured
            if not os.getenv("GEMINI_API_KEY"):
                raise HTTPException(
                    status_code=503,
                    detail="AI mode not available: GEMINI_API_KEY not configured"
                )

            # Execute AI-powered task
            driver = AIRobotDriver()
            result = await driver.execute_goal(
                goal=request.message,
                max_steps=request.max_steps
            )

            return TaskResponse(
                success=result["success"],
                message=result["message"],
                mode="ai",
                steps_taken=result["steps_taken"]
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid mode: {request.mode}. Use 'basic' or 'ai'"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Task execution failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": f"Internal server error: {str(exc)}"
        }
    )


if __name__ == "__main__":
    import uvicorn

    print("Starting Robot Driver API...")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")

    uvicorn.run(app, host="0.0.0.0", port=8000)
