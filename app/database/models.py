from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime, timezone

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
    ingredient: Mapped[str] = mapped_column(String(1000), unique=True)
    
    # Relationships
    products: Mapped[list["ProductIngredient"]] = relationship(back_populates="ingredient")
    active_ingredient: Mapped["ActiveIngredient"] = relationship(back_populates="ingredient", uselist=False)

    def __repr__(self):
        return f"<Ingredient={self.ingredient}>"


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(1000), unique=True)
    product_img: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(5000))
    category: Mapped[str] = mapped_column(String(500))
    company_name: Mapped[str] = mapped_column(String(1000))
    
    # Relationships
    ingredients: Mapped[list["ProductIngredient"]] = relationship(back_populates="product")
    stats: Mapped["ProductStat"] = relationship(back_populates="product", uselist=False)
    variants: Mapped[list["ProductVariant"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    urls: Mapped[list["ProductURL"]] = relationship(back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product={self.product_name}>"
    

class ProductVariant(Base):
    __tablename__ = "product_variants"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    size_ml: Mapped[int] = mapped_column(Integer)  
    price: Mapped[int] = mapped_column(Integer)    
    is_available: Mapped[bool] = mapped_column(default=True)  
    
    # Relationships
    product: Mapped["Product"] = relationship(back_populates="variants")

    def __repr__(self):
        return f"<ProductVariant product_id={self.product_id} size={self.size_ml}ml price={self.price}>"


class ProductURL(Base):
    __tablename__ = "product_urls"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    url: Mapped[str] = mapped_column(String(2000))
    store_name: Mapped[str] = mapped_column(String(200))  
    is_active: Mapped[bool] = mapped_column(default=True)  
    
    # Relationships
    product: Mapped["Product"] = relationship(back_populates="urls")

    def __repr__(self):
        return f"<ProductURL product_id={self.product_id} store={self.store_name} type={self.url_type}>"


class IncompatibleIngredient(Base):
    __tablename__ = "incompatible_ingredients"
    ingredient1_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
    ingredient2_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)

    # Relationships
    ingredient1: Mapped["Ingredient"] = relationship(foreign_keys=[ingredient1_id])
    ingredient2: Mapped["Ingredient"] = relationship(foreign_keys=[ingredient2_id])


class ActiveIngredient(Base):
    __tablename__ = "active_ingredients"
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)

    # Relationships
    ingredient: Mapped["Ingredient"] = relationship(back_populates="active_ingredient")

    def __repr__(self):
        return f"<ActiveIngredient requires_sunscreen={self.ingredient_id}>"


class ProductStat(Base):
    __tablename__ = "product_stats"
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)

    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    reset_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    
    # Relationship
    product: Mapped["Product"] = relationship(back_populates="stats")


class BlogStat(Base):
    __tablename__ = "blog_stats"
    blog_path: Mapped[str] = mapped_column(String(255), primary_key=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    reset_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))