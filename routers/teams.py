from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from database import get_session
from models.models import Team, Hero
from schemas.schemas import TeamCreate, TeamRead, HeroRead

# 创建团队相关的路由器，设置前缀和标签
router = APIRouter(prefix="/teams", tags=["teams"])

@router.post("/", response_model=TeamRead)
def create_team(team: TeamCreate, session: Session = Depends(get_session)):
    """创建新团队"""
    db_team = Team(**team.model_dump())
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

@router.get("/", response_model=List[TeamRead])
def read_teams(session: Session = Depends(get_session)):
    """获取所有团队列表"""
    teams = session.exec(select(Team)).all()
    return teams

@router.get("/{team_id}", response_model=TeamRead)
def read_team(team_id: int, session: Session = Depends(get_session)):
    """获取单个团队的详细信息"""
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.get("/{team_id}/heroes/", response_model=List[HeroRead])
def read_team_heroes(team_id: int, session: Session = Depends(get_session)):
    """获取指定团队中的所有英雄"""
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team.heroes 

@router.put("/{team_id}", response_model=TeamRead)
def update_hero(team_id: int, team_update: TeamCreate, session: Session = Depends(get_session)):
    """更新指定团队的信息"""
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # 只更新提供的字段
    team_data = team_update.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(team, key, value)
    
    session.add(team)
    session.commit()
    session.refresh(team)
    return team

@router.delete("/{team_id}/heroes/{hero_id}", status_code=204)
def remove_hero_from_team(team_id: int, hero_id: int, session: Session = Depends(get_session)):
    """从团队中移除英雄"""
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    team.heroes.remove(hero)
    session.commit()
    return team.heroes 
