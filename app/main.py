from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Item
from .schemas import ItemCreate, ItemOut

# 建立 FastAPI app
app = FastAPI(title="Linux PostgreSQL Python Docker Project")

# 啟動時建立資料表（正式環境會改成 migration）
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    """
    最基本的 endpoint，用來確認服務是否啟動
    """
    return {"message": "project is running"}


@app.get("/health")
def health():
    """
    Liveness probe（服務是否存活）

    用途：
    - Kubernetes / Docker healthcheck
    - 不檢查 DB，只檢查 app 本身
    """
    return {"status": "ok"}


@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    """
    Readiness probe（服務是否準備好處理流量）

    這裡會檢查 DB 是否可用
    若 DB 掛掉，應該回 503
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"database not ready: {e}")


@app.post("/items", response_model=ItemOut)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    """
    建立資料（寫入 DB）

    流程：
    1. 建立 ORM object
    2. 加入 session
    3. commit
    4. refresh 取得 DB 寫入後的值（例如 id）
    """
    item = Item(name=payload.name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)):
    """
    讀取資料（查詢 DB）

    order_by(id.desc) 是為了讓最新資料排前面
    """
    return db.query(Item).order_by(Item.id.desc()).all()
