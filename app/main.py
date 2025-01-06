from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db_setup import get_db, init_db
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, update, delete, insert
from app.database.models import Product, ProductIngredient

@asynccontextmanager
async def lifespan(app: FastAPI):
  init_db()
  yield

app =  FastAPI(lifespan=lifespan)

# Middleware
origin = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/product", status_code=200)
def list_products(db: Session = Depends(get_db)):
  products = db.scalars(select(Product)).all()
  if not products:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  return products

@app.get("/product/ingredients", status_code=200)
def list_products_with_ingredients(db: Session = Depends(get_db)):
  products = db.scalars(select(Product).options(selectinload(Product.ingredients).selectinload(ProductIngredient.ingredient))).all()
  if not products:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  return products

@app.get("/product/{searchterm}")
def fetch_product(searchterm, db: Session = Depends(get_db)):
    result = db.scalars(select(Product).where(Product.product_name.icontains(searchterm))
        .options(selectinload(Product.ingredients).selectinload(ProductIngredient.ingredient))).all()
    return result