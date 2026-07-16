build and deploy authService:
1. start Docker
2. login to AWS
    `aws login --profile tony-dev --region us-east-1`
3. login to AWS ECR
    ` aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 555146423685.dkr.ecr.us-east-1.amazonaws.com`

3. build the authService stack:
    `npm.cmd run build`

4. deploy the authService stack:
    `npm.cmd run deploy`


Feature Development
PHASE 1 — 创建 authService -> AWS RDS PostgreSQL
Step 1 — 打开 RDS

进入：

AWS RDS Console

点击：

Create database
Step 2 — 选择配置
Engine

选择：

PostgreSQL

推荐：

PostgreSQL 16
Step 3 — 选择模板

先选：

Free tier

或者：

Dev/Test
Step 4 — DB Instance 配置

推荐：

配置	推荐
DB instance identifier	virtualbrain-auth-db
Master username	postgres
Password	自己设强密码

记下来：

username
password

后面要用。

Step 5 — Instance size

推荐：

db.t4g.micro

很便宜。

Step 6 — Storage

推荐：

20 GB

够用了。

Step 7 — Connectivity（非常关键）

这里最容易错。

Public access

开发阶段：

YES

先简单跑通。

生产再改 private。

Step 8 — Security Group

新建 security group：

比如：

virtualbrain-rds-sg
Step 9 — Database name

填写：

virtualbrain
Step 10 — 创建数据库

点击：

Create database

等待 5-10 分钟。

PHASE 2 — 配置 Security Group
Step 11 — 打开 RDS Instance

找到：

Connectivity & security

记下：

Endpoint

类似：

virtualbrain-auth-db.xxxxxx.us-east-1.rds.amazonaws.com
Step 12 — 修改 inbound rules

进入：

EC2 -> Security Groups

找到：

virtualbrain-rds-sg

添加：

Type	Port	Source
PostgreSQL	5432	My IP

开发阶段先允许自己电脑访问。

PHASE 3 — 本地验证 PostgreSQL
Step 13 — 安装 PostgreSQL client

Mac:

brew install postgresql

Windows：

推荐：

pgAdmin

或者：

PostgreSQL Download

Step 14 — 测试连接
psql \
-h YOUR_ENDPOINT \
-U postgres \
-d virtualbrain

成功说明：

RDS OK。

PHASE 4 — 修改 authService
Step 15 — 安装 Python dependencies

在：

app/authService

安装：

pip install sqlalchemy psycopg2-binary alembic

更新：

requirements.txt
Step 16 — 修改 DATABASE_URL

以前：

sqlite:///./virtualbrain.db

改成：

postgresql+psycopg2://postgres:PASSWORD@ENDPOINT:5432/virtualbrain

但不要 hardcode。

Step 17 — 使用 environment variable
config.py
import os

DATABASE_URL = os.getenv("DATABASE_URL")
Step 18 — 创建 db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Step 19 — FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
PHASE 5 — 创建 Models
Step 20 — 创建 models/user.py
from sqlalchemy import Column, Integer, String
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
Step 21 — Base metadata
from sqlalchemy.orm import declarative_base

Base = declarative_base()
PHASE 6 — Alembic Migration
Step 22 — 初始化 Alembic
alembic init alembic

生成：

alembic/
alembic.ini
Step 23 — 配置 alembic.ini

改：

sqlalchemy.url =

为：

sqlalchemy.url = postgresql+psycopg2://...

或者动态读取 env。

Step 24 — 配置 env.py

导入：

from models import Base
target_metadata = Base.metadata
Step 25 — 创建 migration
alembic revision --autogenerate -m "create users"
Step 26 — 执行 migration
alembic upgrade head

这时候：

RDS 已经有：

users

表了。

PHASE 7 — Lambda 环境变量
Step 27 — 设置 Lambda ENV

进入：

Lambda
→ authService
→ Configuration
→ Environment Variables

添加：

KEY	VALUE
DATABASE_URL	postgresql+psycopg2://...
Step 28 — Dockerfile 确认依赖

确保：

RUN pip install -r requirements.txt

包含：

sqlalchemy
psycopg2-binary
alembic
PHASE 8 — Deploy
Step 29 — Build image

你现在应该已经有：

npm run release

或者：

docker buildx ...
aws lambda update-function-code ...

重新 deploy。

PHASE 10（后续优化）
1. Lambda + RDS Proxy
2. Secrets Manager: (store DB PW and env vars)
4. pgvector: 未来 AI assistantService