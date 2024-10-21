from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(..., example="Laptop")
    description: str = Field(None, example="A high-performance laptop")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    name: str = Field(None, example="Updated Laptop")
    description: str = Field(None, example="An updated high-performance laptop")

class ItemInDB(ItemBase):
    id: int

    class Config:
        orm_mode = True