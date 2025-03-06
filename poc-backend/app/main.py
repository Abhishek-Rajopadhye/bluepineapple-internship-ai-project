from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.routes import auth, llm, call
import asyncio

# Create FastAPI app instance
app = FastAPI(title="FastAPI LLM Service", version="1.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
asyncio.run(init_db())

# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(llm.router, prefix="/api/llm", tags=["LLM"])
app.include_router(call.router, prefix="/api/call", tags=["Call"])

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
