from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import QueuePool

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "sqlite:///./heroes.db"
DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./heroes.db"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session 

async_engine = create_async_engine(DATABASE_URL_ASYNC)

# 异步会话依赖
async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session
        
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


