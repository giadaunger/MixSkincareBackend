from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func
from datetime import datetime

class Base(DeclarativeBase):
  id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

class Ingredient(Base):
  __tablename__ = "ingredients"
  ingredient: Mapped[str]

  def __repr__(self):
    return f"<Ingredient={self.ingredient}>"
  

class Product(Base):
  __tablename__ = "products"
  product_name: Mapped[str]
  product_img: Mapped[str]
  description: Mapped[str]
  company_name: Mapped[str]

  def __repr__(self):
    return f"<Product={self.product_name}>"