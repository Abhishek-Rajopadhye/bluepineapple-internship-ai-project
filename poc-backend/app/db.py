from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
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

async def get_db():
    """
    Dependency function to get a database session.

    Yields:
        AsyncSession: An asynchronous database session.
    """
    async with AsyncSessionLocal() as session:
        yield session

async def ensure_tables_exist():
    """
    Function to check if 'users' and 'conversations' tables exist and create them if missing.

    Raises:
        SQLAlchemyError: If there is an error executing the SQL commands.
    """
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
            users_table_exists = result.scalar() is not None

            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'"))
            conversations_table_exists = result.scalar() is not None

            if not users_table_exists or not conversations_table_exists:
                print("🔹 Tables not found, creating tables...")
                await conn.run_sync(Base.metadata.create_all)
            else:
                print("All tables exist.")
    except SQLAlchemyError as sqlError:
        print(sqlError)

async def init_db():
    """
    Function to initialize the database by creating all tables.

    Raises:
        SQLAlchemyError: If there is an error executing the SQL commands.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as sqlError:
        print(f"Error initializing the database: {sqlError}")
        raise

# Run the ensure_tables_exist function to check and create tables if necessary
try:
    asyncio.run(ensure_tables_exist())
except SQLAlchemyError as sqlError:
    print(f"Error running ensure_tables_exist: {sqlError}")