from pydantic import BaseModel, Field

class ProductSchema(BaseModel):
    product_name: str = Field(
        description="name of the product, unique and required",
        min_length=1, 
        max_length=100
    )
    product_img: str = Field(
        description="URL to product image",
        max_length=255
    )
    description: str = Field(
        description="description of the product",
        max_length=1000
    )
    company_name: str = Field(
        description="name of the company that makes the product",
        max_length=100
    )

class IngredientSchema(BaseModel):
    ingredient: str = Field(
        description="name of the ingredient, unique and required",
        min_length=1,
        max_length=100
    )

class ProductIngredientSchema(BaseModel):
    product_id: int = Field(
        description="the id linking to the product table, unique including ingredient id + required"
    )
    ingredient_id: int = Field(
        description="the id linking to the ingredient table, unique including product id + required"
    )