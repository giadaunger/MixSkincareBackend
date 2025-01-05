from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, UniqueConstraint

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class ProductIngredient(Base):
    __tablename__ = "product_ingredients"
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    
    # Relationships
    product: Mapped["Product"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="products")

    __table_args__ = (
        UniqueConstraint("product_id", "ingredient_id"),
    )


class Ingredient(Base):
    __tablename__ = "ingredients"
    ingredient: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Relationship
    products: Mapped[list["ProductIngredient"]] = relationship(back_populates="ingredient")

    def __repr__(self):
        return f"<Ingredient={self.ingredient}>"


class Product(Base):
    __tablename__ = "products"
    product_name: Mapped[str] = mapped_column(String(100), unique=True)
    product_img: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    company_name: Mapped[str] = mapped_column(String(100))
    
    # Relationship
    ingredients: Mapped[list["ProductIngredient"]] = relationship(back_populates="product")

    def __repr__(self):
        return f"<Product={self.product_name}>"