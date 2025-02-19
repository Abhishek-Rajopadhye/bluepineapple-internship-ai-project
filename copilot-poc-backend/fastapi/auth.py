from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from database import get_db
from models import User
from passlib.hash import bcrypt

router = APIRouter()

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    """
    Registers a new user with the given username and password.
    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.
        db (Session, optional): The database session. Defaults to Depends(get_db).
    Returns:
        dict: A dictionary containing a success message.
    """
    user = User(username=username, password=bcrypt.hash(password))
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(username: str, password: str, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    Authenticates a user and generates an access token.
    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        Authorize (AuthJWT, optional): Dependency that provides JWT authorization. Defaults to Depends().
        db (Session, optional): Dependency that provides the database session. Defaults to Depends(get_db).
    Raises:
        HTTPException: If the credentials are invalid, raises a 401 HTTP exception.
    Returns:
        dict: A dictionary containing the access token.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = Authorize.create_access_token(subject=user.id)
    return {"access_token": access_token}
