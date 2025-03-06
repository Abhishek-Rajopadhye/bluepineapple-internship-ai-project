import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from app.db import Base, get_db
from app.main import app

# Test database (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    """
    Override the get_db dependency to use a test database.

    Yields:
        AsyncSession: The test database session.
    """
    async with TestingSessionLocal() as session:
        yield session

async def ensure_test_tables_exist():
    """
    Ensures all tables are created in the test database.

    Raises:
        SQLAlchemyError: If an error occurs during table creation.
    """
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
            users_table_exists = result.scalar() is not None

            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'"))
            conversations_table_exists = result.scalar() is not None

            if not users_table_exists or not conversations_table_exists:
                print("🔹 Tables not found in test DB, creating tables...")
                await conn.run_sync(Base.metadata.create_all)
            else:
                print("All tables exist in test DB.")
    except SQLAlchemyError as sqlError:
        print(f"Error ensuring test tables exist: {sqlError}")
        raise

async def init_test_db():
    """
    Initializes the test database by creating all tables.

    Raises:
        SQLAlchemyError: If an error occurs during database initialization.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Test database initialized successfully.")
    except SQLAlchemyError as sqlError:
        print(f"Error initializing test database: {sqlError}")
        raise

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """
    Pytest fixture to ensure tables exist before any test runs.

    This ensures that tables exist in the in-memory test database.
    """
    await ensure_test_tables_exist()  # Ensure tables exist before tests start
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Cleanup after tests

@pytest_asyncio.fixture(scope="session")
async def client():
    """
    Fixture to provide a test FastAPI client.

    Yields:
        AsyncClient: The test HTTP client.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
