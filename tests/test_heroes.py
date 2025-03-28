import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from database import get_session
from models.models import Hero

# 创建测试数据库
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# 创建测试客户端
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_hero(client: TestClient):
    """测试创建英雄"""
    hero_data = {
        "name": "Spider-Man",
        "secret_name": "Peter Parker",
        "age": 20
    }
    response = client.post("/heroes/", json=hero_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == hero_data["name"]
    assert data["secret_name"] == hero_data["secret_name"]
    assert data["age"] == hero_data["age"]
    assert "id" in data

def test_read_heroes(client: TestClient, session: Session):
    """测试获取英雄列表"""
    # 创建测试数据
    hero_1 = Hero(name="Iron Man", secret_name="Tony Stark", age=45)
    hero_2 = Hero(name="Captain America", secret_name="Steve Rogers", age=100)
    session.add(hero_1)
    session.add(hero_2)
    session.commit()

    response = client.get("/heroes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Iron Man"
    assert data[1]["name"] == "Captain America"

def test_read_hero(client: TestClient, session: Session):
    """测试获取单个英雄"""
    hero = Hero(name="Thor", secret_name="Thor Odinson", age=1500)
    session.add(hero)
    session.commit()

    response = client.get(f"/heroes/{hero.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Thor"
    assert data["secret_name"] == "Thor Odinson"

def test_update_hero(client: TestClient, session: Session):
    """测试更新英雄信息"""
    hero = Hero(name="Hulk", secret_name="Bruce Banner", age=40)
    session.add(hero)
    session.commit()

    update_data = {
        "name": "Smart Hulk",
        "secret_name": "Bruce Banner",
        "age": 41
    }
    response = client.put(f"/heroes/heroes/{hero.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Smart Hulk"
    assert data["age"] == 41

def test_delete_hero(client: TestClient, session: Session):
    """测试删除英雄"""
    hero = Hero(name="Black Widow", secret_name="Natasha Romanoff", age=35)
    session.add(hero)
    session.commit()

    response = client.delete(f"/heroes/heroes/{hero.id}")
    assert response.status_code == 204

    # 验证英雄已被删除
    hero_check = session.get(Hero, hero.id)
    assert hero_check is None

def test_hero_not_found(client: TestClient):
    """测试访问不存在的英雄"""
    response = client.get("/heroes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Hero not found" 