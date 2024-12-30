from pydantic import BaseModel

class ProductSchema(BaseModel):
  id: int
  product_name: str
  product_img: str