from fastapi import FastAPI, HTTPException, Depends, status, Request
from contextlib import asynccontextmanager
from app.db_setup import get_db, init_db
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, update, delete, insert
from app.database.models import Product

@asynccontextmanager
async def lifespan(app: FastAPI):
  init_db()
  yield

app =  FastAPI(lifespan=lifespan)

@app.get("/product", status_code=200)
def list_products(db: Session = Depends(get_db)):
  products = db.scalars(select(Product)).all()
  if not products:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  return products