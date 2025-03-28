# Heroes API

这是一个使用 FastAPI 和 SQLModel 构建的英雄管理系统 API。

## 功能特性

- 英雄信息的增删改查
- 基于 SQLite 数据库存储
- RESTful API 设计
- 完整的 API 文档

## 技术栈

- FastAPI
- SQLModel
- SQLite
- Python 3.10+

## 安装

1. 克隆项目

```bash
git clone [项目地址]
cd heroes-api
```

2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
pyproject.toml 文件中配置了依赖，使用 uv sync 安装依赖

```bash
uv sync
```

## 运行

1. 启动服务器

```bash
uvicorn main:app --reload
```

2. 访问 API 文档

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## API 端点

- `GET /heroes/`: 获取所有英雄
- `POST /heroes/`: 创建新英雄
- `GET /heroes/{hero_id}`: 获取特定英雄
- `PUT /heroes/{hero_id}`: 更新英雄信息
- `DELETE /heroes/{hero_id}`: 删除英雄
...

## 许可证

MIT License

Copyright (c) 2025 codelifterx