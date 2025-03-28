from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from database import get_session, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Hero
from schemas.schemas import HeroCreate, HeroRead

# 创建英雄相关的路由器，设置前缀和标签
router = APIRouter(prefix="/heroes", tags=["heroes"])

@router.post("/", response_model=HeroRead)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    """创建新英雄"""
    db_hero = Hero(**hero.model_dump())
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.get("/", response_model=List[HeroRead])
def read_heroes(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    """获取英雄列表，支持分页"""
    heroes = session.exec(select(Hero).offset(skip).limit(limit)).all()
    return heroes

@router.put("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(hero_id: int, hero_update: HeroCreate, session: Session = Depends(get_session)):
    """更新指定英雄的信息"""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    # 只更新提供的字段
    hero_data = hero_update.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(hero, key, value)
    
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@router.get("/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    """获取单个英雄的详细信息"""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero 

@router.delete("/heroes/{hero_id}", status_code=204)
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    """删除指定英雄"""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    session.delete(hero)
    session.commit()
    return None

@router.get("/heroes/async/", response_model=List[HeroRead])
async def read_heroes_async(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Hero))
    heroes = result.scalars().all()
    return heroes