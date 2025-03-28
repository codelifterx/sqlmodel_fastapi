from typing import List, Optional
from sqlmodel import SQLModel

# 团队相关模式
class TeamBase(SQLModel):
    """团队基础模式
    
    包含团队的基本属性字段
    """
    name: str  # 团队名称
    headquarters: str  # 总部位置

class TeamCreate(TeamBase):
    """创建团队时使用的模式
    
    继承自TeamBase，不需要额外字段
    """
    pass

class TeamRead(TeamBase):
    """读取团队信息时使用的模式
    
    继承自TeamBase，添加了id字段
    """
    id: int  # 团队唯一标识符

# 英雄相关模式
class HeroBase(SQLModel):
    """英雄基础模式
    
    包含英雄的基本属性字段
    """
    name: str  # 英雄名称
    secret_name: str  # 秘密身份
    age: Optional[int] = None  # 年龄（可选）

class HeroCreate(HeroBase):
    """创建英雄时使用的模式
    
    继承自HeroBase，添加了team_id字段
    """
    team_id: Optional[int] = None  # 所属团队ID（可选）

class HeroRead(HeroBase):
    """读取英雄信息时使用的模式
    
    继承自HeroBase，添加了id和team_id字段
    """
    id: int  # 英雄唯一标识符
    team_id: Optional[int] = None  # 所属团队ID（可选）

# 任务相关模式
class MissionBase(SQLModel):
    """任务基础模式
    
    包含任务的基本属性字段
    """
    name: str  # 任务名称

class MissionCreate(MissionBase):
    """创建任务时使用的模式
    
    继承自MissionBase，不需要额外字段
    """
    pass

class MissionRead(MissionBase):
    """读取任务信息时使用的模式
    
    继承自MissionBase，添加了id字段
    """
    id: int  # 任务唯一标识符
