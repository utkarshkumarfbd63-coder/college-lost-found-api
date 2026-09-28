from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Item, ItemCreate, ItemRead, ItemStatus, ItemUpdate, MessageResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="College Lost & Found API",
    description="Report, find, and manage items lost or found on campus.",
    version="1.0.0",
    lifespan=lifespan,
)

SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/", tags=["Health"])
def read_root() -> dict[str, str]:
    return {"message": "College Lost & Found API is running"}


@app.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED, tags=["Items"])
def create_item(item_data: ItemCreate, session: SessionDep) -> Item:
    item = Item.model_validate(item_data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/items", response_model=list[ItemRead], tags=["Items"])
def read_items(session: SessionDep) -> list[Item]:
    return list(session.exec(select(Item)).all())


@app.get("/items/status/{status}", response_model=list[ItemRead], tags=["Items"])
def read_items_by_status(status: ItemStatus, session: SessionDep) -> list[Item]:
    statement = select(Item).where(Item.status == status)
    return list(session.exec(statement).all())


@app.get("/items/category/{category}", response_model=list[ItemRead], tags=["Items"])
def read_items_by_category(category: str, session: SessionDep) -> list[Item]:
    statement = select(Item).where(Item.category == category)
    return list(session.exec(statement).all())


@app.get("/items/{item_id}", response_model=ItemRead, tags=["Items"])
def read_item(item_id: int, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=ItemRead, tags=["Items"])
def update_item(item_id: int, item_data: ItemUpdate, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item.sqlmodel_update(item_data.model_dump(exclude_unset=True))
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.delete("/items/{item_id}", response_model=MessageResponse, tags=["Items"])
def delete_item(item_id: int, session: SessionDep) -> MessageResponse:
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    session.delete(item)
    session.commit()
    return MessageResponse(message=f"Item {item_id} deleted successfully")