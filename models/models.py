from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional

class HeroMissionLink(SQLModel, table=True):
    """英雄-任务关联表模型
    
    用于建立英雄和任务之间的多对多关系
    """
    __tablename__ = "hero_mission_link"  # 显式指定表名

    # 定义复合主键
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id", primary_key=True)
    mission_id: Optional[int] = Field(default=None, foreign_key="mission.id", primary_key=True)
    
    # # 建立与英雄和任务表的关系
    # hero: "Hero" = Relationship(back_populates="hero_missions")
    # mission: "Mission" = Relationship(back_populates="hero_missions")

    # 记录英雄加入任务的时间
    join_time: datetime | None = None

class Team(SQLModel, table=True):
    """团队模型
    
    包含团队的基本信息和与英雄的一对多关系
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # 团队名称
    headquarters: str  # 总部位置
    
    # 与英雄表建立一对多关系
    heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    """英雄模型
    
    包含英雄的基本信息，与团队的多对一关系，以及与任务的多对多关系
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # 英雄名称
    secret_name: str  # 秘密身份
    age: Optional[int] = None  # 年龄（可选）
    
    # 与团队的关联
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes") 

    # 与任务的多对多关系
    # hero_missions: List[HeroMissionLink] = Relationship(back_populates="hero")
    missions: List["Mission"] = Relationship(
        back_populates="heroes",
        link_model=HeroMissionLink
        # sa_relationship_kwargs={"overlaps": "hero_missions"}
        # sa_relationship_kwargs={
        #     "overlaps": ["hero_missions", "hero"]  # 添加所有重叠的关系
        # }
    )

class Mission(SQLModel, table=True):
    """任务模型
    
    包含任务的基本信息和与英雄的多对多关系
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # 任务名称
    description: Optional[str] = None
    
    # 与英雄的多对多关系
    # hero_missions: List[HeroMissionLink] = Relationship(
    #     back_populates="mission",
    #     sa_relationship_kwargs={"overlaps": "heroes"}
    # )
    heroes: List[Hero] = Relationship(
        back_populates="missions",
        link_model=HeroMissionLink
        # sa_relationship_kwargs={"overlaps": "hero_missions"}
        # # sa_relationship_kwargs={
        # #     "overlaps": ["hero_missions", "mission"]  # 添加所有重叠的关系
        # # }
    )
