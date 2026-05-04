import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 從環境變數讀取 DB 連線字串
# 預設使用 docker-compose 內的 service 名稱 "db" 作為 hostname
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://app_user:app_password@db:5432/app_db",
)

# 建立 SQLAlchemy engine
# pool_pre_ping=True 可避免使用到已失效的 DB connection（實務上很重要）
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 建立 session factory（每個 request 會產生一個 session）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM base class（所有 model 都要繼承）
Base = declarative_base()


def get_db():
    """
    FastAPI dependency:
    每個 request 會呼叫一次，確保 DB session 正確開啟與關閉

    使用 yield 是為了讓 FastAPI 自動在 request 結束後做 cleanup
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
