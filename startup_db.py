from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db_setup import get_db
from app.database.models import Product, Ingredient, ProductIngredient, IncompatibleIngredient, CompatibilityWarning, ActiveIngredient
from datetime import datetime

db: Session = next(get_db())

try:
    # Skapa ingredienser
    ingredients_data = [
        {'ingredient': 'Hyaluronic Acid'},
        {'ingredient': 'Niacinamide'},
        {'ingredient': 'Vitamin C'},
        {'ingredient': 'Retinol'},
        {'ingredient': 'Glycerin'},
        {'ingredient': 'Ceramides'},
        {'ingredient': 'Salicylic Acid'},
        {'ingredient': 'Peptides'},
        {'ingredient': 'Squalane'},
        {'ingredient': 'Aloe Vera'}
    ]

    for ingredient_data in ingredients_data:
        ingredient = Ingredient(**ingredient_data)
        db.add(ingredient)

    db.commit()

    # Skapa produkter
    products_data = [
        {
            'product_name': 'Hydrating Serum',
            'product_img': 'https://example.com/hydrating-serum.jpg',
            'description': 'A lightweight serum that deeply hydrates and plumps the skin',
            'company_name': 'The Ordinary'
        },
        {
            'product_name': 'Moisture Barrier Cream',
            'product_img': 'https://example.com/barrier-cream.jpg',
            'description': 'Rich cream that repairs and strengthens skin barrier',
            'company_name': 'CeraVe'
        },
        {
            'product_name': 'Vitamin C Brightening Serum',
            'product_img': 'https://example.com/vitamin-c-serum.jpg',
            'description': 'Powerful antioxidant serum that brightens and evens skin tone',
            'company_name': 'Skinceuticals'
        },
        {
            'product_name': 'Gentle Cleanser',
            'product_img': 'https://example.com/cleanser.jpg',
            'description': 'Non-stripping cleanser suitable for all skin types',
            'company_name': 'La Roche-Posay'
        },
        {
            'product_name': 'BHA Exfoliant',
            'product_img': 'https://example.com/bha.jpg',
            'description': 'Chemical exfoliant that unclogs pores and smooths skin texture',
            'company_name': 'Paula\'s Choice'
        }
    ]

    for product_data in products_data:
        product = Product(**product_data)
        db.add(product)

    db.commit()

    # Koppla produkter och ingredienser
    product_ingredients_data = [
        # Hydrating Serum ingredienser
        {'product_id': 1, 'ingredient_id': 1},  # Hyaluronic Acid
        {'product_id': 1, 'ingredient_id': 5},  # Glycerin
        {'product_id': 1, 'ingredient_id': 9},  # Squalane
        
        # Moisture Barrier Cream ingredienser
        {'product_id': 2, 'ingredient_id': 6},  # Ceramides
        {'product_id': 2, 'ingredient_id': 5},  # Glycerin
        {'product_id': 2, 'ingredient_id': 8},  # Peptides
        
        # Vitamin C Brightening Serum ingredienser
        {'product_id': 3, 'ingredient_id': 3},  # Vitamin C
        {'product_id': 3, 'ingredient_id': 2},  # Niacinamide
        {'product_id': 3, 'ingredient_id': 1},  # Hyaluronic Acid
        
        # Gentle Cleanser ingredienser
        {'product_id': 4, 'ingredient_id': 5},  # Glycerin
        {'product_id': 4, 'ingredient_id': 10}, # Aloe Vera
        {'product_id': 4, 'ingredient_id': 9},  # Squalane
        
        # BHA Exfoliant ingredienser
        {'product_id': 5, 'ingredient_id': 7},  # Salicylic Acid
        {'product_id': 5, 'ingredient_id': 5},  # Glycerin
        {'product_id': 5, 'ingredient_id': 10}  # Aloe Vera
    ]

    for product_ingredient_data in product_ingredients_data:
        product_ingredient = ProductIngredient(**product_ingredient_data)
        db.add(product_ingredient)

    db.commit()

    # Skapa inkompatibla ingredienser och förklaringar
    incompatible_ingredients_data = [
        {'ingredient1_id': 1, 'ingredient2_id': 3, 'reason': 'Hyaluronic Acid and Vitamin C can cause pH imbalance.'},
        {'ingredient1_id': 2, 'ingredient2_id': 4, 'reason': 'Niacinamide and Retinol can cause irritation when used together.'},
        {'ingredient1_id': 3, 'ingredient2_id': 4, 'reason': 'Vitamin C and Retinol should not be used together due to different pH levels.'},
        {'ingredient1_id': 5, 'ingredient2_id': 7, 'reason': 'Glycerin and Salicylic Acid may cause over-exfoliation.'},
        {'ingredient1_id': 8, 'ingredient2_id': 9, 'reason': 'Peptides and Squalane have no significant interaction, but can reduce effectiveness.'}
    ]

    for incompatible_data in incompatible_ingredients_data:
        incompatible = IncompatibleIngredient(**incompatible_data)
        db.add(incompatible)

    db.commit()

    # Skapa kompatibilitetsvarningar
    compatibility_warnings_data = [
        {'ingredient_id': 1, 'incompatible_with_id': 3, 'warning_message': 'Do not use Hyaluronic Acid and Vitamin C together.'},
        {'ingredient_id': 2, 'incompatible_with_id': 4, 'warning_message': 'Avoid using Niacinamide and Retinol together to prevent irritation.'},
        {'ingredient_id': 3, 'incompatible_with_id': 4, 'warning_message': 'Vitamin C and Retinol are best used at different times of the day.'}
    ]

    for warning_data in compatibility_warnings_data:
        warning = CompatibilityWarning(**warning_data)
        db.add(warning)

    db.commit()

    # Skapa aktiva ingredienser med krav på solskydd
    active_ingredients_data = [
        {'ingredient_id': 4, 'requires_sunscreen': True, 'additional_info': 'Retinol increases skin sensitivity to sunlight.'},
        {'ingredient_id': 7, 'requires_sunscreen': True, 'additional_info': 'Salicylic Acid can make the skin more prone to sunburn.'},
        {'ingredient_id': 3, 'requires_sunscreen': True, 'additional_info': 'Vitamin C enhances protection against UV rays but requires additional sunscreen.'}
    ]

    for active_data in active_ingredients_data:
        active_ingredient = ActiveIngredient(**active_data)
        db.add(active_ingredient)

    db.commit()
    
    print("Hudvårdsprodukter och ingredienser har lagts till i databasen!")

except Exception as e:
    db.rollback()
    print(f"Ett fel uppstod: {e}")

finally:
    db.close()