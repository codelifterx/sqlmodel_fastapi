from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from database import get_session
from models.models import Mission, Hero
from schemas.schemas import MissionCreate, MissionRead, HeroRead

# 创建任务相关的路由器，设置前缀和标签
router = APIRouter(prefix="/missions", tags=["missions"])

@router.post("/", response_model=MissionRead)
def create_mission(mission: MissionCreate, session: Session = Depends(get_session)):
    """创建新任务"""
    db_mission = Mission(**mission.model_dump())
    session.add(db_mission)
    session.commit()
    session.refresh(db_mission)
    return db_mission

@router.get("/", response_model=List[MissionRead])
def read_missions(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    """获取任务列表，支持分页"""
    missions = session.exec(select(Mission).offset(skip).limit(limit)).all()
    return missions

@router.put("/missions/{mission_id}", response_model=MissionRead)
def update_mission(mission_id: int, mission_update: MissionCreate, session: Session = Depends(get_session)):
    """更新指定任务的信息"""
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    # 只更新提供的字段
    mission_data = mission_update.model_dump(exclude_unset=True)
    for key, value in mission_data.items():
        setattr(mission, key, value)
    
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission

@router.get("/{mission_id}", response_model=MissionRead)
def read_mission(mission_id: int, session: Session = Depends(get_session)):
    """获取单个任务的详细信息"""
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission 

@router.delete("/missions/{mission_id}", status_code=204)
def delete_mission(mission_id: int, session: Session = Depends(get_session)):
    """删除指定任务"""
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    session.delete(mission)
    session.commit()
    return None

@router.post("/{mission_id}/heroes/{hero_id}", status_code=204)
def add_hero_to_mission(mission_id: int, hero_id: int, session: Session = Depends(get_session)):
    """将英雄添加到任务中"""
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    mission.heroes.append(hero)
    session.commit()
    return None

@router.delete("/{mission_id}/heroes/{hero_id}", status_code=204)
def remove_hero_from_mission(mission_id: int, hero_id: int, session: Session = Depends(get_session)):
    """从任务中移除英雄"""
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    mission.heroes.remove(hero)
    session.commit()
    return None

@router.get("/{mission_id}/heroes", response_model=List[HeroRead])
def read_mission_heroes(mission_id: int, session: Session = Depends(get_session)):
    """获取指定任务的所有英雄"""
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission.heroes
