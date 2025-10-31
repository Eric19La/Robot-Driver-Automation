"""
FastAPI Web Service for Robot Driver
Provides HTTP endpoints to execute automation tasks remotely
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
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


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information"""
    gemini_configured = bool(os.getenv("GEMINI_API_KEY"))

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Robot Driver Automation API</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 10px;
            }}
            .endpoint {{
                background: #f9f9f9;
                padding: 15px;
                margin: 10px 0;
                border-left: 4px solid #4CAF50;
                border-radius: 4px;
            }}
            .endpoint strong {{
                color: #4CAF50;
            }}
            .status {{
                display: inline-block;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 14px;
                margin-left: 10px;
            }}
            .enabled {{
                background: #4CAF50;
                color: white;
            }}
            .disabled {{
                background: #ff9800;
                color: white;
            }}
            a {{
                color: #4CAF50;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            code {{
                background: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: monospace;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Robot Driver Automation API</h1>
            <p><strong>Version:</strong> 1.0.0</p>
            <p>Network-accessible automation service using Playwright and AI</p>

            <h2>📡 Available Endpoints</h2>

            <div class="endpoint">
                <strong>POST /execute</strong> - Execute an automation task
                <br><small>Send a task message to automate web actions</small>
            </div>

            <div class="endpoint">
                <strong>GET /health</strong> - <a href="/health">Health check endpoint</a>
                <br><small>Check service status and available features</small>
            </div>

            <div class="endpoint">
                <strong>GET /docs</strong> - <a href="/docs">Interactive API documentation</a>
                <br><small>Swagger UI for testing endpoints</small>
            </div>

            <h2>🎯 Execution Modes</h2>

            <div class="endpoint">
                <strong>Basic Mode</strong> <span class="status enabled">Available</span>
                <br><small>Fixed task execution (product search on Amazon)</small>
            </div>

            <div class="endpoint">
                <strong>AI Mode</strong> <span class="status {'enabled' if gemini_configured else 'disabled'}">
                    {'Available' if gemini_configured else 'Configure GEMINI_API_KEY'}
                </span>
                <br><small>AI-powered dynamic task execution using Google Gemini</small>
            </div>

            <h2>🚀 Quick Start</h2>
            <p>Test the API using curl:</p>
            <pre><code>curl -X POST "http://localhost:8000/execute" \\
  -H "Content-Type: application/json" \\
  -d '{{"message": "test", "mode": "basic"}}'</code></pre>

            <p>Or use the <a href="/docs">interactive documentation</a> to test endpoints in your browser.</p>

            <h2>📚 Documentation</h2>
            <p>See the README.md file for complete setup instructions and usage examples.</p>
        </div>
    </body>
    </html>
    """
    return html_content


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
