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
    warnings: Mapped[list["CompatibilityWarning"]] = relationship("CompatibilityWarning", back_populates="ingredient", foreign_keys="CompatibilityWarning.ingredient_id")
    active_ingredient: Mapped["ActiveIngredient"] = relationship(back_populates="ingredient", uselist=False)

    def __repr__(self):
        return f"<Ingredient={self.ingredient}>"


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(100), unique=True)
    product_img: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    company_name: Mapped[str] = mapped_column(String(100))
    
    # Relationships
    ingredients: Mapped[list["ProductIngredient"]] = relationship(back_populates="product")

    def __repr__(self):
        return f"<Product={self.product_name}>"


class IncompatibleIngredient(Base):
    __tablename__ = "incompatible_ingredients"
    ingredient1_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    ingredient2_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    reason: Mapped[str] = mapped_column(String(255))

    # Relationships
    ingredient1: Mapped["Ingredient"] = relationship(foreign_keys=[ingredient1_id])
    ingredient2: Mapped["Ingredient"] = relationship(foreign_keys=[ingredient2_id])


class CompatibilityWarning(Base):
    __tablename__ = "compatibility_warnings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    warning_message: Mapped[str] = mapped_column(String(255))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    incompatible_with_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))

    # Relationships
    ingredient: Mapped["Ingredient"] = relationship("Ingredient", foreign_keys=[ingredient_id], back_populates="warnings")
    incompatible_with: Mapped["Ingredient"] = relationship("Ingredient", foreign_keys=[incompatible_with_id])

    def __repr__(self):
        return f"<CompatibilityWarning={self.warning_message}>"


class IngredientCategory(Base):
    __tablename__ = "ingredient_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Relationships
    ingredients: Mapped[list["CategoryIngredient"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<IngredientCategory={self.category_name}>"


class CategoryIngredient(Base):
    __tablename__ = "category_ingredients"
    category_id: Mapped[int] = mapped_column(ForeignKey("ingredient_categories.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)

    # Relationships
    category: Mapped["IngredientCategory"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="categories")


class ActiveIngredient(Base):
    __tablename__ = "active_ingredients"
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    requires_sunscreen: Mapped[bool] = mapped_column()
    additional_info: Mapped[str] = mapped_column(String(255))

    # Relationships
    ingredient: Mapped["Ingredient"] = relationship(back_populates="active_ingredient")

    def __repr__(self):
        return f"<ActiveIngredient requires_sunscreen={self.requires_sunscreen}>"
