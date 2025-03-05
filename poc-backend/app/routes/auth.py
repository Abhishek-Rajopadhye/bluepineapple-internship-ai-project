from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.models import User
from app.dependencies import hash_password, verify_password, create_access_token, get_current_user
from pydantic import BaseModel

# FastAPI router for authentication
router = APIRouter()

# Pydantic models for request validation
class UserRegister(BaseModel):
    emailId: str
    password: str

class UserLogin(BaseModel):
    emailId: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    """
    Register a new user by hashing the password and storing user details in the database.
    """
    print()
    # Check if the username already exists
    result = await db.execute(select(User).where(User.username == user_data.emailId))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash password and create a new user
    new_user = User(username=user_data.emailId, password_hash=hash_password(user_data.password))
    db.add(new_user)
    await db.commit()

    return {"message": "User registered successfully"}

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and return a JWT access token.
    """
    # Retrieve user from database
    result = await db.execute(select(User).where(User.username == user_data.emailId))
    user = result.scalars().first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generate access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token}

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get details of the currently authenticated user.
    """
    return {"id": current_user.id, "username": current_user.username}
