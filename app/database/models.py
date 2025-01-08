from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class ProductIngredient(Base):
    __tablename__ = "product_ingredients"
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    
    # Relationships
    product: Mapped["Product"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="products")


class Ingredient(Base):
    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ingredient: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Relationships
    products: Mapped[list["ProductIngredient"]] = relationship(back_populates="ingredient")
    categories: Mapped[list["CategoryIngredient"]] = relationship(back_populates="ingredient")
    active_ingredient: Mapped["ActiveIngredient"] = relationship(back_populates="ingredient", uselist=False)

    def __repr__(self):
        return f"<Ingredient={self.ingredient}>"


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(100), unique=True)
    product_img: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    category: Mapped[str] = mapped_column(String(255))
    company_name: Mapped[str] = mapped_column(String(100))
    
    # Relationships
    ingredients: Mapped[list["ProductIngredient"]] = relationship(back_populates="product")

    def __repr__(self):
        return f"<Product={self.product_name}>"


class IncompatibleIngredient(Base):
    __tablename__ = "incompatible_ingredients"
    ingredient1_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    ingredient2_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)

    # Relationships
    ingredient1: Mapped["Ingredient"] = relationship(foreign_keys=[ingredient1_id])
    ingredient2: Mapped["Ingredient"] = relationship(foreign_keys=[ingredient2_id])


class CategoryIngredient(Base):
    __tablename__ = "category_ingredients"
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)

    # Relationships
    ingredient: Mapped["Ingredient"] = relationship(back_populates="categories")


class ActiveIngredient(Base):
    __tablename__ = "active_ingredients"
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)

    # Relationships
    ingredient: Mapped["Ingredient"] = relationship(back_populates="active_ingredient")

    def __repr__(self):
        return f"<ActiveIngredient requires_sunscreen={self.ingredient_id}>"
