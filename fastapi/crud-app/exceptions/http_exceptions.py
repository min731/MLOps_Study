from fastapi import HTTPException

class ItemNotFoundException(HTTPException):
    def __init__(self, item_id: int):
        super().__init__(status_code=404, detail=f"Item with id {item_id} not found")

class ItemAlreadyExistsException(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=400, detail=f"Item with name {name} already exists")
