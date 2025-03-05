from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from app.config import Config
import asyncio

DATABASE_URL = Config.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)

# Base class for models
Base = declarative_base()

# Dependency function to get a database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Function to check if tables exist & create them if missing
async def ensure_tables_exist():
    async with engine.begin() as conn:
        # Check if 'users' table exists
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
        users_table_exists = result.scalar() is not None

        # Check if 'conversations' table exists
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'"))
        conversations_table_exists = result.scalar() is not None

        # If tables don't exist, create them
        if not users_table_exists or not conversations_table_exists:
            print("🔹 Tables not found, creating tables...")
            await conn.run_sync(Base.metadata.create_all)
        else:
            print("All tables exist.")

# Function to initialize the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(ensure_tables_exist())
