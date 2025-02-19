from fastapi import FastAPI
from database import engine, Base
from auth import router as auth_router
from routes.copilot import router as copilot_router
from routes.call import router as call_router

app = FastAPI()

# Initialize Database
Base.metadata.create_all(bind=engine)

# Register Routes
app.include_router(auth_router, prefix="/auth")
app.include_router(copilot_router, prefix="/api")
app.include_router(call_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Customer Support API is running"}
