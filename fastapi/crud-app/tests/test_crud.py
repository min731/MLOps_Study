from crud import crud_item
from schemas.item import ItemCreate

def test_create_item(db):
    item = ItemCreate(name="Test Item", description="This is a test item")
    db_item = crud_item.create_item(db, item)
    assert db_item.name == "Test Item"
    assert db_item.description == "This is a test item"

def test_get_item(db):
    item = ItemCreate(name="Test Item", description="This is a test item")
    db_item = crud_item.create_item(db, item)
    
    retrieved_item = crud_item.get_item(db, db_item.id)
    assert retrieved_item.name == "Test Item"
    assert retrieved_item.description == "This is a test item"