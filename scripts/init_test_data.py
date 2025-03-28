from database import engine
from models.models import Hero, Team, Mission, HeroMissionLink
from sqlmodel import Session

def init_test_data():
    # 创建数据库和表
    # create_db_and_tables()
    
    with Session(engine) as session:
        # 创建队伍
        avengers = Team(
            name="复仇者联盟", 
            description="地球最强英雄联盟",
            headquarters="复仇者大厦"  # 添加总部信息
        )
        x_men = Team(
            name="X战警", 
            description="变种人英雄团队",
            headquarters="X学院"  # 添加总部信息
        )
        session.add_all([avengers, x_men])
        session.commit()

        # 创建英雄
        heroes = [
            Hero(
                name="钢铁侠",
                real_name="托尼·斯塔克",
                secret_name="Iron Man",  # 添加英雄代号
                description="天才发明家，穿着机甲的超级英雄",
                team_id=avengers.id
            ),
            Hero(
                name="美国队长",
                real_name="史蒂夫·罗杰斯",
                secret_name="Captain America",  # 添加英雄代号
                description="超级士兵血清的产物，正义的化身",
                team_id=avengers.id
            ),
            Hero(
                name="金刚狼",
                real_name="罗根",
                secret_name="Wolverine",  # 添加英雄代号
                description="自愈能力超强的变种人",
                team_id=x_men.id
            ),
            Hero(
                name="凤凰女",
                real_name="琴·格雷",
                secret_name="Phoenix",  # 添加英雄代号
                description="强大的心灵感应能力者",
                team_id=x_men.id
            )
        ]
        session.add_all(heroes)
        session.commit()

        # 创建任务
        missions = [
            Mission(
                name="拯救纽约",
                description="对抗外星人入侵纽约的行动",
                status="已完成",
                difficulty=5
            ),
            Mission(
                name="保护变种人",
                description="解救被关押的变种人同胞",
                status="进行中",
                difficulty=4
            ),
            Mission(
                name="对抗奥创",
                description="阻止奥创毁灭人类的计划",
                status="已完成",
                difficulty=5
            )
        ]
        session.add_all(missions)
        session.commit()

        # 创建英雄-任务关联
        hero_missions = [
            HeroMissionLink(hero_id=heroes[0].id, mission_id=missions[0].id),  # 钢铁侠-拯救纽约
            HeroMissionLink(hero_id=heroes[1].id, mission_id=missions[0].id),  # 美国队长-拯救纽约
            HeroMissionLink(hero_id=heroes[2].id, mission_id=missions[1].id),  # 金刚狼-保护变种人
            HeroMissionLink(hero_id=heroes[3].id, mission_id=missions[1].id),  # 凤凰女-保护变种人
            HeroMissionLink(hero_id=heroes[0].id, mission_id=missions[2].id),  # 钢铁侠-对抗奥创
            HeroMissionLink(hero_id=heroes[1].id, mission_id=missions[2].id),  # 美国队长-对抗奥创
        ]
        session.add_all(hero_missions)
        session.commit()

if __name__ == "__main__":
    init_test_data()
    print("测试数据初始化完成！") 