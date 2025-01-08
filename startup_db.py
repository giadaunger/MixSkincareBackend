from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db_setup import get_db
from app.database.models import Product, Ingredient, ProductIngredient, IncompatibleIngredient, ActiveIngredient
from datetime import datetime

db: Session = next(get_db())

try:
    # Skapa ingredienser
    ingredients_data = [
        {'ingredient': 'Water'},
        {'ingredient': 'Centella Asiatica Extract'},
        {'ingredient': 'Caprylic/Capric Triglyceride'},
        {'ingredient': 'Glycerin'},
        {'ingredient': 'Squalane'},
        {'ingredient': 'Niacinamide'},
        {'ingredient': 'Hyaluronic Acid'},
        {'ingredient': 'Retinal'},
        {'ingredient': 'Glycolic Acid'},
        {'ingredient': 'Snail Secretion Filtrate'},
        {'ingredient': 'Panthenol'},
        {'ingredient': 'Sodium Hyaluronate'},
        {'ingredient': 'Butylene Glycol'},
        {'ingredient': 'Betaine'},
        {'ingredient': '1, 2-Hexanediol'},
        {'ingredient': 'Allantoin'},
        {'ingredient': 'Carbomer'},
        {'ingredient': 'Ethylhexylglycerin'},
        {'ingredient': 'Phenoxyethanol'},
        {'ingredient': 'Ceramide NP'}
    ]

    for ingredient_data in ingredients_data:
        ingredient = Ingredient(**ingredient_data)
        db.add(ingredient)

    db.commit()

    # Skapa produkter med kategorier
    products_data = [
        {
            'product_name': 'Dermide Cica Barrier Sleeping Pack',
            'product_img': 'product1.png',
            'description': 'En sovmask som hjälper till att lugna hud som blivit utmattad av skadliga UV-strålar och andra miljöfaktorer över natten.',
            'category': 'Ansiktsmask',
            'company_name': 'Purito'
        },
        {
            'product_name': 'Skin Purifier',
            'product_img': 'product2.png',
            'description': 'Clinisoothe är en mycket effektiv toner som bidrar till att hålla huden i god balans.',
            'category': 'Ansiktsvatten',
            'company_name': 'Clinisoothe'
        },
        {
            'product_name': 'Ageless Day Cream',
            'product_img': 'product3.png',
            'description': 'Ageless Day Cream är en återfuktande och skyddande anti-age dagkräm med SPF 15.',
            'category': 'Dagkräm',
            'company_name': 'Emma S.'
        },
        {
            'product_name': 'Supple Preparation Unscented Toner',
            'product_img': 'product4.png',
            'description': 'Klairs Supple Preparation Unscented Facial Toner är en lätt, fuktgivande toner.',
            'category': 'Toner',
            'company_name': 'Klairs'
        },
        {
            'product_name': 'Advanced Snail 92 All in one Cream',
            'product_img': 'product5.png',
            'description': 'Ge din hud en magisk glöd med kultfavoriten Advanced Snail 92 All In One Cream!',
            'category': 'Ansiktskräm',
            'company_name': 'Cosrx'
        },
        {
            'product_name': 'Watermelon Dew Serum',
            'product_img': 'product6.png',
            'description': 'Serumet innehåller hyaluronsyra i tre olika molekylstorlekar.',
            'category': 'Serum',
            'company_name': 'Smuuti Skin'
        },
        {
            'product_name': 'Hyaluronic Acid 2% + B5',
            'product_img': 'product7.png',
            'description': 'Hyaluronic Acid 2% + B5 ger omedelbar uppfriskande fukt.',
            'category': 'Serum',
            'company_name': 'The Ordinary'
        },
        {
            'product_name': 'Revive Eye Serum: Ginseng+Retinal',
            'product_img': 'product8.png',
            'description': 'Ett utjämnande ögonserum i krämform som behandlar fina linjer och rynkor.',
            'category': 'Ögonkräm',
            'company_name': 'Beauty of Joseon'
        },
        {
            'product_name': 'Glycolic Acid 7% Exfoliating Toner',
            'product_img': 'product9.png',
            'description': 'En glykolsyra-baserad exfolierande toner som märkbart jämnar ut hudens textur.',
            'category': 'Serum',
            'company_name': 'The Ordinary'
        },
        {
            'product_name': 'Advanced Snail 96 Mucin Power Essence',
            'product_img': 'product10.png',
            'description': 'Innehåller hela 96,3% filtrerat snigelsekret för optimal hudvård.',
            'category': 'Essence',
            'company_name': 'Cosrx'
        }
    ]

    for product_data in products_data:
        product = Product(**product_data)
        db.add(product)

    db.commit()

    # Resten av koden är samma som förut...
    # Koppla produkter och ingredienser
    product_ingredients_data = [
        # Dermide Cica Barrier Sleeping Pack
        {'product_id': 1, 'ingredient_id': 1},  # Water
        {'product_id': 1, 'ingredient_id': 2},  # Centella Asiatica Extract
        {'product_id': 1, 'ingredient_id': 4},  # Glycerin
        {'product_id': 1, 'ingredient_id': 20}, # Ceramide NP

        # Skin Purifier
        {'product_id': 2, 'ingredient_id': 1},  # Water
        
        # Ageless Day Cream
        {'product_id': 3, 'ingredient_id': 1},  # Water
        {'product_id': 3, 'ingredient_id': 4},  # Glycerin
        {'product_id': 3, 'ingredient_id': 5},  # Squalane

        # Supple Preparation Unscented Toner
        {'product_id': 4, 'ingredient_id': 1},  # Water
        {'product_id': 4, 'ingredient_id': 13}, # Butylene Glycol
        {'product_id': 4, 'ingredient_id': 4},  # Glycerin

        # Advanced Snail 92
        {'product_id': 5, 'ingredient_id': 10}, # Snail Secretion
        {'product_id': 5, 'ingredient_id': 14}, # Betaine
        {'product_id': 5, 'ingredient_id': 3},  # Caprylic/Capric Triglyceride

        # Watermelon Dew Serum
        {'product_id': 6, 'ingredient_id': 1},  # Water
        {'product_id': 6, 'ingredient_id': 6},  # Niacinamide
        {'product_id': 6, 'ingredient_id': 7},  # Hyaluronic Acid

        # Hyaluronic Acid 2%
        {'product_id': 7, 'ingredient_id': 1},  # Water
        {'product_id': 7, 'ingredient_id': 7},  # Hyaluronic Acid
        {'product_id': 7, 'ingredient_id': 11}, # Panthenol

        # Revive Eye Serum
        {'product_id': 8, 'ingredient_id': 1},  # Water
        {'product_id': 8, 'ingredient_id': 8},  # Retinal
        {'product_id': 8, 'ingredient_id': 4},  # Glycerin

        # Glycolic Acid 7%
        {'product_id': 9, 'ingredient_id': 1},  # Water
        {'product_id': 9, 'ingredient_id': 9},  # Glycolic Acid
        {'product_id': 9, 'ingredient_id': 4},  # Glycerin

        # Advanced Snail 96
        {'product_id': 10, 'ingredient_id': 10}, # Snail Secretion
        {'product_id': 10, 'ingredient_id': 14}, # Betaine
        {'product_id': 10, 'ingredient_id': 13}  # Butylene Glycol
    ]

    for product_ingredient_data in product_ingredients_data:
        product_ingredient = ProductIngredient(**product_ingredient_data)
        db.add(product_ingredient)

    db.commit()

    # Skapa inkompatibla ingredienser
    incompatible_ingredients_data = [
        {'ingredient1_id': 8, 'ingredient2_id': 9},   # Retinal och Glycolic Acid
        {'ingredient1_id': 6, 'ingredient2_id': 8},   # Niacinamide och Retinal
        {'ingredient1_id': 6, 'ingredient2_id': 9},   # Niacinamide och Glycolic Acid
        {'ingredient1_id': 7, 'ingredient2_id': 9},   # Hyaluronic Acid och Glycolic Acid
        {'ingredient1_id': 8, 'ingredient2_id': 10}   # Retinal och Snail Secretion
    ]

    for incompatible_data in incompatible_ingredients_data:
        incompatible = IncompatibleIngredient(**incompatible_data)
        db.add(incompatible)

    db.commit()

    # Skapa aktiva ingredienser 
    active_ingredients_data = [
        {'ingredient_id': 8},  # Retinal
        {'ingredient_id': 9},  # Glycolic Acid
        {'ingredient_id': 6},  # Niacinamide
        {'ingredient_id': 7}   # Hyaluronic Acid
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