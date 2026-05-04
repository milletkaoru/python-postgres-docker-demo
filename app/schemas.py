from pydantic import BaseModel


class ItemCreate(BaseModel):
    """
    API 請求用 schema（client -> server）
    """
    name: str


class ItemOut(BaseModel):
    """
    API 回應用 schema（server -> client）

    from_attributes=True 可以讓 ORM object 直接轉成 JSON
    """
    id: int
    name: str

    class Config:
        from_attributes = True
