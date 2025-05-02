from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db_setup import get_db, init_db
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, update, delete, insert, and_, or_
from sqlalchemy.sql.expression import func
from app.database.models import Product, ProductIngredient, ActiveIngredient, IncompatibleIngredient, Ingredient, ProductStat

@asynccontextmanager
async def lifespan(app: FastAPI):
  init_db()
  yield

app =  FastAPI(lifespan=lifespan)

# Middleware
origin = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "https://mixskincare.netlify.app"
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
def list_products_with_ingredients(limit: int = 5, db: Session = Depends(get_db)):
  products = db.scalars(select(Product).options(selectinload(Product.ingredients).selectinload(ProductIngredient.ingredient)).limit(limit)).all()
  if not products:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  return products

@app.get("/product/id/{product_id}")
def fetch_product_with_id(product_id: int, db: Session = Depends(get_db)):
    result = db.scalar(select(Product).where(Product.id == product_id)
        .options(selectinload(Product.ingredients).selectinload(ProductIngredient.ingredient)))
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@app.get("/product/{searchterm}")
def fetch_product(searchterm: str, db: Session = Depends(get_db)):
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


@app.get("/product/{product_id}/similar")
def find_similar_products(
    product_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    # Fetches the original product with its ingredients
    original_product = db.scalar(
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.ingredients).selectinload(ProductIngredient.ingredient))
    )
    
    if not original_product:
        raise HTTPException(status_code=404, detail="Produkt hittades inte")
    
    # Retrieve all other products with their ingredients, filtered by same category
    all_products = db.scalars(
        select(Product)
        .where(
            and_(
                Product.id != product_id,
                Product.category == original_product.category
            )
        )
        .options(selectinload(Product.ingredients).selectinload(ProductIngredient.ingredient))
    ).all()
    
    # Create sets of original product ingredients with full ingredient info
    original_ingredients = {
        pi.ingredient.id: pi.ingredient.ingredient 
        for pi in original_product.ingredients
    }
    
    # Calculate similarity for each product
    product_similarities = []
    for product in all_products:
        # Create set of current product ingredients with full ingredient info
        product_ingredients = {
            pi.ingredient.id: pi.ingredient.ingredient 
            for pi in product.ingredients
        }
        
        # Find matching and non-matching ingredients
        matching_ingredient_ids = set(original_ingredients.keys()) & set(product_ingredients.keys())
        original_only_ids = set(original_ingredients.keys()) - set(product_ingredients.keys())
        product_only_ids = set(product_ingredients.keys()) - set(original_ingredients.keys())
        
        # Create detailed ingredient lists
        matching_ingredients = [
            {"id": ing_id, "name": original_ingredients[ing_id]}
            for ing_id in matching_ingredient_ids
        ]
        
        original_only_ingredients = [
            {"id": ing_id, "name": original_ingredients[ing_id]}
            for ing_id in original_only_ids
        ]
        
        product_only_ingredients = [
            {"id": ing_id, "name": product_ingredients[ing_id]}
            for ing_id in product_only_ids
        ]
        
        product_similarities.append({
            "product": product,
            "similarity_score": len(matching_ingredients),
            "matching_ingredients": matching_ingredients,
            "original_only_ingredients": original_only_ingredients,
            "product_only_ingredients": product_only_ingredients
        })
    
    # Take the top N most similar products
    similar_products = []
    for ps in product_similarities[:limit]:
        product = ps["product"]
        similar_products.append({
            "id": product.id,
            "name": product.product_name,
            "product_img": product.product_img, 
            "description": product.description,
            "category": product.category,
            "company_name": product.company_name,
            "similarity_score": ps["similarity_score"],
            "total_ingredients": len(product.ingredients),
            "matching_ingredients": ps["matching_ingredients"],
            "original_only_ingredients": ps["original_only_ingredients"],
            "product_only_ingredients": ps["product_only_ingredients"]
        })
    
    return {
        "original_product": {
            "id": original_product.id,
            "name": original_product.product_name,
             "product_img": original_product.product_img,
            "category": original_product.category,
            "total_ingredients": len(original_product.ingredients)
        },
        "similar_products": similar_products
    }


@app.post("/track/product-view/{product_id}")
def track_product_view(product_id: int, db: Session = Depends(get_db)):
    # Get or create product statistics
    stats = db.scalar(select(ProductStat).where(ProductStat.product_id == product_id))
    
    if not stats:
        # Check if the product exists
        product = db.scalar(select(Product).where(Product.id == product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Create statistics if they do not exist
        stats = ProductStat(product_id=product_id, view_count=1)
        db.add(stats)
    else:
        # Increase the counter
        stats.view_count += 1
    
    db.commit()
    return {"status": "success"}


@app.get("/popular-products")
def get_popular_products(limit: int = 25, random_limit: int = 10, db: Session = Depends(get_db)):
    # First get popular products based on view count
    popular_products = db.scalars(
        select(Product)
        .join(ProductStat)
        .order_by(ProductStat.view_count.desc())
        .limit(limit)
        .options(selectinload(Product.ingredients).selectinload(ProductIngredient.ingredient))
    ).all()
    
    # Get the IDs of popular products to exclude them from random selection
    popular_product_ids = [p.id for p in popular_products]
    
    # Then get additional random products that are not in the popular list
    if random_limit > 0:
        random_products = db.scalars(
            select(Product)
            .where(Product.id.not_in(popular_product_ids) if popular_product_ids else True)
            .order_by(func.random())
            .limit(random_limit)
            .options(selectinload(Product.ingredients).selectinload(ProductIngredient.ingredient))
        ).all()
        
        # Combine both lists into one
        combined_products = list(popular_products) + list(random_products)
    else:
        combined_products = popular_products
    
    return combined_products