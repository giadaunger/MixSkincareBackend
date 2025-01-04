from pydantic import BaseModel

class IngredientSchema(BaseModel):
  id: int
  ingredient: str

class ProductSchema(BaseModel):
  id: int
  product_name: str
  product_img: str
  ingredients: list[IngredientSchema]