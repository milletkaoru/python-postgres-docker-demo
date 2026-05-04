from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Item(Base):
    """
    ORM model 對應 PostgreSQL 的資料表

    設計重點：
    - id 為 primary key
    - name 加 index，因為查詢會用到（效能考量）
    """

    __tablename__ = "items"

    # 主鍵
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # 商品名稱（不可為 NULL）
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
