from fastapi import FastAPI, Depends
import uvicorn
from contextlib import asynccontextmanager

from database import create_db_and_tables
from routers import heroes, teams, missions
from scripts.init_test_data import init_test_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    create_db_and_tables()

    # 初始化测试数据
    init_test_data()
    
    yield
    # 关闭时执行
    pass

app = FastAPI(title="Hero API", lifespan=lifespan)

# 注册路由
app.include_router(teams.router)
app.include_router(heroes.router)
app.include_router(missions.router)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True) 