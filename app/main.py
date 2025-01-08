from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db_setup import get_db, init_db
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, update, delete, insert, and_, or_
from sqlalchemy.sql.expression import func
from app.database.models import Product, ProductIngredient, ActiveIngredient, IncompatibleIngredient, Ingredient

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
def list_products(limit: int = 5 ,db: Session = Depends(get_db)):
  products = db.scalars(select(Product).order_by(func.random()).limit(limit)).all()
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


@app.post("/analyze-compatibility/{product1_id}/{product2_id}")
def analyze_compatibility(
    product1_id: int, 
    product2_id: int, 
    db: Session = Depends(get_db)
):
    # Fetches the products with ingredienst
    product1 = db.scalar(
        select(Product)
        .where(Product.id == product1_id)
        .options(selectinload(Product.ingredients).selectinload(ProductIngredient.ingredient))
    )
    product2 = db.scalar(
        select(Product)
        .where(Product.id == product2_id)
        .options(selectinload(Product.ingredients).selectinload(ProductIngredient.ingredient))
    )
    
    if not product1 or not product2:
        raise HTTPException(status_code=404, detail="En eller båda produkterna hittades inte")
    
    # Collect all ingredients from both products
    product1_ingredients = {pi.ingredient for pi in product1.ingredients}
    product2_ingredients = {pi.ingredient for pi in product2.ingredients}
    
    # Retrieve all incompatible ingredients for both products' ingredients
    incompatibilities = db.scalars(
        select(IncompatibleIngredient).where(
            or_(
                IncompatibleIngredient.ingredient1_id.in_([i.id for i in product1_ingredients]),
                IncompatibleIngredient.ingredient2_id.in_([i.id for i in product1_ingredients])
            )
        )
    ).all()
    
    # Collect warnings
    warnings = []
    active_ingredient_warnings = []
    
    # Check for incompatibilities
    for incomp in incompatibilities:
        ingredient1 = db.get(Ingredient, incomp.ingredient1_id)
        ingredient2 = db.get(Ingredient, incomp.ingredient2_id)
        
        # Check if the incompatible ingredients are in the other product
        if (ingredient1 in product1_ingredients and ingredient2 in product2_ingredients) or \
           (ingredient2 in product1_ingredients and ingredient1 in product2_ingredients):
            warnings.append({
                "type": "incompatibility",
                "ingredients": [ingredient1.ingredient, ingredient2.ingredient]
            })
    
    # Check active ingredients
    for ingredient in product1_ingredients.union(product2_ingredients):
        active = db.scalar(
            select(ActiveIngredient).where(ActiveIngredient.ingredient_id == ingredient.id)
        )
        if active:
            active_ingredient_warnings.append({
                "ingredient": ingredient.ingredient,
            })
    
    return {
        "products": {
            "product1": product1.product_name,
            "product2": product2.product_name
        },
        "incompatibility_warnings": warnings,
        "active_ingredients": active_ingredient_warnings,
        "is_compatible": len(warnings) == 0
    }