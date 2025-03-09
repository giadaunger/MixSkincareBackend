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
        {'ingredient': 'Ceramide NP'},
        {'ingredient': 'Salicylic Acid'},
        {'ingredient': 'Lactic Acid'},
        {'ingredient': 'Vitamin C'},
        {'ingredient': 'Vitamin E'},
        {'ingredient': 'Aloe Vera Extract'},
        {'ingredient': 'Jojoba Oil'},
        {'ingredient': 'Argan Oil'},
        {'ingredient': 'Tea Tree Oil'},
        {'ingredient': 'Zinc Oxide'},
        {'ingredient': 'Titanium Dioxide'},
        {'ingredient': 'Retinol'},
        {'ingredient': 'Peptides'},
        {'ingredient': 'Collagen'},
        {'ingredient': 'Propolis Extract'},
        {'ingredient': 'Rice Extract'},
        {'ingredient': 'Mugwort Extract'},
        {'ingredient': 'Bakuchiol'},
        {'ingredient': 'Rosehip Seed Oil'},
        {'ingredient': 'Shea Butter'},
        {'ingredient': 'Green Tea Extract'},
        {'ingredient': 'Hemp Seed Oil'},
        {'ingredient': 'Matcha Extract'},
        {'ingredient': 'Kombucha Extract'},
        {'ingredient': 'Alpha Arbutin'},
        {'ingredient': 'Fermented Rice Water'},
        {'ingredient': 'Oat Extract'},
        {'ingredient': 'Beta Glucan'},
        {'ingredient': 'Licorice Root Extract'},
        {'ingredient': 'Tranexamic Acid'},
        {'ingredient': 'Urea'},
        {'ingredient': 'Mandelic Acid'},
        {'ingredient': 'Marula Oil'},
        {'ingredient': 'Avocado Oil'},
        {'ingredient': 'Honey Extract'},
        {'ingredient': 'Bifida Ferment Lysate'},
        {'ingredient': 'Adenosine'},
        {'ingredient': 'Coenzyme Q10'}
    ]

    for ingredient_data in ingredients_data:
        # Kontrollera om ingrediensen redan finns
        existing = db.query(Ingredient).filter(Ingredient.ingredient == ingredient_data['ingredient']).first()
        if not existing:
            ingredient = Ingredient(**ingredient_data)
            db.add(ingredient)

    db.commit()

    # Skapa produkter med kategorier
    products_data = [
        {
            'product_name': 'Dermide Cica Barrier Sleeping Pack',
            'product_img': '/product_img_dummy_data/product1.png',
            'description': 'En sovmask som hjälper till att lugna hud som blivit utmattad av skadliga UV-strålar och andra miljöfaktorer över natten.',
            'category': 'Ansiktsmask',
            'company_name': 'Purito',
            'price': 24900
        },
        {
            'product_name': 'Skin Purifier',
            'product_img': '/product_img_dummy_data/product2.png',
            'description': 'Clinisoothe är en mycket effektiv toner som bidrar till att hålla huden i god balans.',
            'category': 'Ansiktsvatten',
            'company_name': 'Clinisoothe',
            'price': 18900
        },
        {
            'product_name': 'Ageless Day Cream',
            'product_img': '/product_img_dummy_data/product3.png',
            'description': 'Ageless Day Cream är en återfuktande och skyddande anti-age dagkräm med SPF 15.',
            'category': 'Dagkräm',
            'company_name': 'Emma S.',
            'price': 32900
        },
        {
            'product_name': 'Supple Preparation Unscented Toner',
            'product_img': '/product_img_dummy_data/product4.png',
            'description': 'Klairs Supple Preparation Unscented Facial Toner är en lätt, fuktgivande toner.',
            'category': 'Toner',
            'company_name': 'Klairs',
            'price': 19900
        },
        {
            'product_name': 'Advanced Snail 92 All in one Cream',
            'product_img': '/product_img_dummy_data/product5.png',
            'description': 'Ge din hud en magisk glöd med kultfavoriten Advanced Snail 92 All In One Cream!',
            'category': 'Ansiktskräm',
            'company_name': 'Cosrx',
            'price': 24900
        },
        {
            'product_name': 'Watermelon Dew Serum',
            'product_img': '/product_img_dummy_data/product6.png',
            'description': 'Serumet innehåller hyaluronsyra i tre olika molekylstorlekar.',
            'category': 'Serum',
            'company_name': 'Smuuti Skin',
            'price': 29900
        },
        {
            'product_name': 'Hyaluronic Acid 2% + B5',
            'product_img': '/product_img_dummy_data/product7.png',
            'description': 'Hyaluronic Acid 2% + B5 ger omedelbar uppfriskande fukt.',
            'category': 'Serum',
            'company_name': 'The Ordinary',
            'price': 12900
        },
        {
            'product_name': 'Revive Eye Serum: Ginseng+Retinal',
            'product_img': '/product_img_dummy_data/product8.png',
            'description': 'Ett utjämnande ögonserum i krämform som behandlar fina linjer och rynkor.',
            'category': 'Ögonkräm',
            'company_name': 'Beauty of Joseon',
            'price': 19900
        },
        {
            'product_name': 'Glycolic Acid 7% Exfoliating Toner',
            'product_img': '/product_img_dummy_data/product9.png',
            'description': 'En glykolsyra-baserad exfolierande toner som märkbart jämnar ut hudens textur.',
            'category': 'Serum',
            'company_name': 'The Ordinary',
            'price': 13900
        },
        {
            'product_name': 'Advanced Snail 96 Mucin Power Essence',
            'product_img': '/product_img_dummy_data/product10.png',
            'description': 'Innehåller hela 96,3% filtrerat snigelsekret för optimal hudvård.',
            'category': 'Essence',
            'company_name': 'Cosrx',
            'price': 22900
        },
        {
            'product_name': 'Vitamin C Serum',
            'product_img': '/product_img_dummy_data/product11.png',
            'description': 'Ett kraftfullt serum med vitamin C som ljusar upp och jämnar ut hudtonen.',
            'category': 'Serum',
            'company_name': 'Skinceuticals',
            'price': 36900
        },
        {
            'product_name': 'Rice Overnight Mask',
            'product_img': '/product_img_dummy_data/product12.png',
            'description': 'En återfuktande sovmask med risextrakt som återupplivar trött hud över natten.',
            'category': 'Ansiktsmask',
            'company_name': 'I\'m From',
            'price': 28900
        },
        {
            'product_name': 'Tea Tree Oil Cleanser',
            'product_img': '/product_img_dummy_data/product13.png',
            'description': 'En mild rengöringsgel med tea tree oil som effektivt bekämpar akne och orenheter.',
            'category': 'Rengöring',
            'company_name': 'Some By Mi',
            'price': 17900
        },
        {
            'product_name': 'Multi-Peptide Serum',
            'product_img': '/product_img_dummy_data/product14.png',
            'description': 'Ett kraftfullt anti-age serum som bekämpar fina linjer och rynkor med flera peptidkomplex.',
            'category': 'Serum',
            'company_name': 'The Inkey List',
            'price': 15900
        },
        {
            'product_name': 'Aloe Vera Soothing Gel',
            'product_img': '/product_img_dummy_data/product15.png',
            'description': 'En lugnande och återfuktande gel med 99% aloe vera som passar alla hudtyper.',
            'category': 'Gel',
            'company_name': 'Benton',
            'price': 14900
        },
        {
            'product_name': 'Mineral Sunscreen SPF50',
            'product_img': '/product_img_dummy_data/product16.png',
            'description': 'Ett fysikaliskt solskydd med hög skyddsfaktor som inte lämnar vit film.',
            'category': 'Solskydd',
            'company_name': 'Purito',
            'price': 21900
        },
        {
            'product_name': 'Ceramide Barrier Cream',
            'product_img': '/product_img_dummy_data/product17.png',
            'description': 'En intensivt återfuktande kräm som stärker hudens barriär med ceramider och peptider.',
            'category': 'Ansiktskräm',
            'company_name': 'Dr. Jart+',
            'price': 34900
        },
        {
            'product_name': 'BHA Exfoliant Liquid',
            'product_img': '/product_img_dummy_data/product18.png',
            'description': 'En exfolierande toner med salicylsyra (BHA) som rensar porer och förebygger akne.',
            'category': 'Toner',
            'company_name': 'Paula\'s Choice',
            'price': 31900
        },
        {
            'product_name': 'Propolis Ampoule',
            'product_img': '/product_img_dummy_data/product19.png',
            'description': 'Ett koncentrerat serum med propolisextrakt som ger näring och lyster till huden.',
            'category': 'Serum',
            'company_name': 'COSRX',
            'price': 26900
        },
        {
            'product_name': 'Lactic Acid Treatment',
            'product_img': '/product_img_dummy_data/product20.png',
            'description': 'En mild exfolierande behandling med mjölksyra som förbättrar hudens textur och lyster.',
            'category': 'Exfoliering',
            'company_name': 'Sunday Riley',
            'price': 39900
        },
        {
            'product_name': 'Galactomyces Essence',
            'product_img': '/product_img_dummy_data/product21.png',
            'description': 'En näringsrik essence med fermenterad jäst som utjämnar hudton och ger en strålande lyster.',
            'category': 'Essence',
            'company_name': 'COSRX',
            'price': 25900
        },
        {
            'product_name': 'Centella Calming Gel',
            'product_img': '/product_img_dummy_data/product22.png',
            'description': 'En lätt gel med centella asiatica som lugnar irriterad och röd hud på ett skonsamt sätt.',
            'category': 'Gel',
            'company_name': 'Skin1004',
            'price': 18900
        },
        {
            'product_name': 'Oil-Free Moisturizer',
            'product_img': '/product_img_dummy_data/product23.png',
            'description': 'En lätt, oljefri fuktkräm som återfuktar utan att täppa till porerna, perfekt för fet och kombinerad hud.',
            'category': 'Ansiktskräm',
            'company_name': 'La Roche-Posay',
            'price': 21900
        },
        {
            'product_name': 'Retinol Night Serum',
            'product_img': '/product_img_dummy_data/product24.png',
            'description': 'Ett effektivt nattserum med retinol som bekämpar tecken på åldrande medan du sover.',
            'category': 'Serum',
            'company_name': 'Medik8',
            'price': 42900
        },
        {
            'product_name': 'AHA/BHA Clarifying Treatment',
            'product_img': '/product_img_dummy_data/product25.png',
            'description': 'En exfolierande behandling med både AHA och BHA som effektivt rensar huden och förebygger akne.',
            'category': 'Exfoliering',
            'company_name': 'COSRX',
            'price': 23900
        },
        {
            'product_name': 'Cica Repair Balm',
            'product_img': '/product_img_dummy_data/product26.png',
            'description': 'En återuppbyggande balm med cica (centella asiatica) som reparerar skadad och irriterad hud.',
            'category': 'Balm',
            'company_name': 'Dr. Jart+',
            'price': 33900
        },
        {
            'product_name': 'Hydrating Cleansing Oil',
            'product_img': '/product_img_dummy_data/product27.png',
            'description': 'En mild rengöringsolja som effektivt löser upp smink och orenheter utan att torka ut huden.',
            'category': 'Rengöring',
            'company_name': 'DHC',
            'price': 27900
        },
        {
            'product_name': 'Nourishing Face Mist',
            'product_img': '/product_img_dummy_data/product28.png',
            'description': 'En uppfriskande ansiktsmist med närande botaniska extrakt som ger fukt under hela dagen.',
            'category': 'Mist',
            'company_name': 'Glow Recipe',
            'price': 19900
        },
        {
            'product_name': 'Pore Refining Clay Mask',
            'product_img': '/product_img_dummy_data/product29.png',
            'description': 'En djuprengörande lermask som reducerar porer och absorberar överskottsolja för en mattare hud.',
            'category': 'Ansiktsmask',
            'company_name': 'Innisfree',
            'price': 16900
        },
        {
            'product_name': 'Vitamin E Night Oil',
            'product_img': '/product_img_dummy_data/product30.png',
            'description': 'En närande nattolja med vitamin E som återställer hudens fuktbalans medan du sover.',
            'category': 'Ansiktsolja',
            'company_name': 'The Body Shop',
            'price': 29900
        },
        {
            'product_name': 'Mugwort Essence',
            'product_img': '/product_img_dummy_data/product31.png',
            'description': 'En lugnande essence med artemisia (mugwort) som reducerar rodnad och irritation.',
            'category': 'Essence',
            'company_name': 'I\'m From',
            'price': 26900
        },
        {
            'product_name': 'Bakuchiol Booster',
            'product_img': '/product_img_dummy_data/product32.png',
            'description': 'Ett växtbaserat alternativ till retinol som ger anti-age effekter utan irritation.',
            'category': 'Serum',
            'company_name': 'Bybi Beauty',
            'price': 29900
        },
        {
            'product_name': 'Rosehip Seed Oil',
            'product_img': '/product_img_dummy_data/product33.png',
            'description': 'En näringsrik ansiktsolja som hjälper till att läka ärr och utjämna hudton.',
            'category': 'Ansiktsolja',
            'company_name': 'The Ordinary',
            'price': 15900
        },
        {
            'product_name': 'Lip Sleeping Mask',
            'product_img': '/product_img_dummy_data/product34.png',
            'description': 'En intensivt återfuktande läppmask som mjukgör och reparerar läpparna över natten.',
            'category': 'Läppvård',
            'company_name': 'Laneige',
            'price': 22900
        },
        {
            'product_name': 'Green Tea Enzyme Powder Wash',
            'product_img': '/product_img_dummy_data/product35.png',
            'description': 'En mild enzymbaserad rengöring i pulverform som exfolierar huden utan att irritera.',
            'category': 'Rengöring',
            'company_name': 'Tosowoong',
            'price': 18900
        },
        {
            'product_name': 'Matcha Hemp Hydrating Cleanser',
            'product_img': '/product_img_dummy_data/product36.png',
            'description': 'En mild rengöring med matcha, hampa och grönt te som effektivt rengör utan att torka ut.',
            'category': 'Rengöring',
            'company_name': 'Krave Beauty',
            'price': 22900
        },
        {
            'product_name': 'Kombucha Essence',
            'product_img': '/product_img_dummy_data/product37.png',
            'description': 'En essence med fermenterad kombucha som ger glöd och förbättrar hudtexturen.',
            'category': 'Essence',
            'company_name': 'Fresh',
            'price': 34900
        },
        {
            'product_name': 'Alpha Arbutin Solution',
            'product_img': '/product_img_dummy_data/product38.png',
            'description': 'En effektiv lösning som jämnar ut hudtonen och reducerar hyperpigmentering och mörka fläckar.',
            'category': 'Serum',
            'company_name': 'The Ordinary',
            'price': 11900
        },
        {
            'product_name': 'Fermented Rice Water Toner',
            'product_img': '/product_img_dummy_data/product39.png',
            'description': 'En ljusande toner med fermenterat risvatten som ger en jämnare och mer strålande hy.',
            'category': 'Toner',
            'company_name': 'Secret Key',
            'price': 17900
        },
        {
            'product_name': 'Oat Cleansing Balm',
            'product_img': '/product_img_dummy_data/product40.png',
            'description': 'En närande rengöringsbalm med havre som varsamt tar bort smink och orenheter utan att torka ut huden.',
            'category': 'Rengöring',
            'company_name': 'The Inkey List',
            'price': 13900
        },
        {
            'product_name': 'Brightening Treatment Essence',
            'product_img': '/product_img_dummy_data/product41.png',
            'description': 'En upplyftande essence med lakritsrot-extrakt som reducerar mörka fläckar och ojämn hudton.',
            'category': 'Essence',
            'company_name': 'Missha',
            'price': 24900
        },
        {
            'product_name': 'Tranexamic Acid Night Serum',
            'product_img': '/product_img_dummy_data/product42.png',
            'description': 'Ett kraftfullt nattserum med tranexamic acid som motverkar hyperpigmentering och rodnad.',
            'category': 'Serum',
            'company_name': 'Facetheory',
            'price': 32900
        },
        {
            'product_name': 'Barrier Repair Moisturizer',
            'product_img': '/product_img_dummy_data/product43.png',
            'description': 'En återuppbyggande fuktkräm med 5% urea som reparerar hudens fuktbarriär.',
            'category': 'Ansiktskräm',
            'company_name': 'CeraVe',
            'price': 19900
        },
        {
            'product_name': 'Mandelic Acid 10% Treatment',
            'product_img': '/product_img_dummy_data/product44.png',
            'description': 'En exfolierande behandling med mandelsyra som är skonsam även för känslig hud.',
            'category': 'Exfoliering',
            'company_name': 'Wishtrend',
            'price': 23900
        },
        {
            'product_name': 'Virgin Marula Facial Oil',
            'product_img': '/product_img_dummy_data/product45.png',
            'description': 'En lyxig ansiktsolja med antioxidantrik marulaolja för ökad lyster och näring.',
            'category': 'Ansiktsolja',
            'company_name': 'Drunk Elephant',
            'price': 45900
        },
        {
            'product_name': 'Avocado Melt Sleeping Mask',
            'product_img': '/product_img_dummy_data/product46.png',
            'description': 'En näringsrik sovmask med avokadoolja och extrakt som återfuktar och lugnar under natten.',
            'category': 'Ansiktsmask',
            'company_name': 'Glow Recipe',
            'price': 27900
        },
        {
            'product_name': 'Royal Honey Propolis Enrich Essence',
            'product_img': '/product_img_dummy_data/product47.png',
            'description': 'En närande essence med honung och propolis som stärker, återfuktar och ger lyster.',
            'category': 'Essence',
            'company_name': 'Cosrx',
            'price': 26900
        },
        {
            'product_name': 'Probiotic Power Treatment',
            'product_img': '/product_img_dummy_data/product48.png',
            'description': 'En behandling med probiotika som balanserar hudens mikrobiom och stärker barriärfunktionen.',
            'category': 'Serum',
            'company_name': 'Allies of Skin',
            'price': 38900
        },
        {
            'product_name': 'Firming Adenosine Cream',
            'product_img': '/product_img_dummy_data/product49.png',
            'description': 'En uppstramande kräm med adenosin som motverkar rynkor och förbättrar hudens elasticitet.',
            'category': 'Ansiktskräm',
            'company_name': 'Mizon',
            'price': 28900
        },
        {
            'product_name': 'Antioxidant Youth Preserving Cream',
            'product_img': '/product_img_dummy_data/product50.png',
            'description': 'En kraftfull anti-age kräm med coenzym Q10 som skyddar mot fria radikaler och miljöföroreningar.',
            'category': 'Ansiktskräm',
            'company_name': 'Klairs',
            'price': 32900
        }
    ]

    for product_data in products_data:
        # Kontrollera om produkten redan finns
        existing = db.query(Product).filter(Product.product_name == product_data['product_name']).first()
        if not existing:
            product = Product(**product_data)
            db.add(product)

    db.commit()

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
        {'product_id': 10, 'ingredient_id': 13}, # Butylene Glycol
        
        # Nya produkter och deras ingredienser
        # Vitamin C Serum
        {'product_id': 11, 'ingredient_id': 1},  # Water
        {'product_id': 11, 'ingredient_id': 23}, # Vitamin C
        {'product_id': 11, 'ingredient_id': 24}, # Vitamin E
        {'product_id': 11, 'ingredient_id': 4},  # Glycerin

        # Rice Overnight Mask
        {'product_id': 12, 'ingredient_id': 1},  # Water
        {'product_id': 12, 'ingredient_id': 35}, # Rice Extract
        {'product_id': 12, 'ingredient_id': 4},  # Glycerin
        {'product_id': 12, 'ingredient_id': 6},  # Niacinamide

        # Tea Tree Oil Cleanser
        {'product_id': 13, 'ingredient_id': 1},  # Water
        {'product_id': 13, 'ingredient_id': 28}, # Tea Tree Oil
        {'product_id': 13, 'ingredient_id': 21}, # Salicylic Acid
        {'product_id': 13, 'ingredient_id': 4},  # Glycerin

        # Multi-Peptide Serum
        {'product_id': 14, 'ingredient_id': 1},  # Water
        {'product_id': 14, 'ingredient_id': 32}, # Peptides
        {'product_id': 14, 'ingredient_id': 7},  # Hyaluronic Acid
        {'product_id': 14, 'ingredient_id': 4},  # Glycerin

        # Aloe Vera Soothing Gel
        {'product_id': 15, 'ingredient_id': 1},  # Water
        {'product_id': 15, 'ingredient_id': 25}, # Aloe Vera Extract
        {'product_id': 15, 'ingredient_id': 16}, # Allantoin
        {'product_id': 15, 'ingredient_id': 4},  # Glycerin

        # Mineral Sunscreen SPF50
        {'product_id': 16, 'ingredient_id': 1},  # Water
        {'product_id': 16, 'ingredient_id': 29}, # Zinc Oxide
        {'product_id': 16, 'ingredient_id': 30}, # Titanium Dioxide
        {'product_id': 16, 'ingredient_id': 5},  # Squalane

        # Ceramide Barrier Cream
        {'product_id': 17, 'ingredient_id': 1},  # Water
        {'product_id': 17, 'ingredient_id': 20}, # Ceramide NP
        {'product_id': 17, 'ingredient_id': 32}, # Peptides
        {'product_id': 17, 'ingredient_id': 4},  # Glycerin

        # BHA Exfoliant Liquid
        {'product_id': 18, 'ingredient_id': 1},  # Water
        {'product_id': 18, 'ingredient_id': 21}, # Salicylic Acid
        {'product_id': 18, 'ingredient_id': 4},  # Glycerin
        {'product_id': 18, 'ingredient_id': 13}, # Butylene Glycol

        # Propolis Ampoule
        {'product_id': 19, 'ingredient_id': 1},  # Water
        {'product_id': 19, 'ingredient_id': 34}, # Propolis Extract
        {'product_id': 19, 'ingredient_id': 7},  # Hyaluronic Acid
        {'product_id': 19, 'ingredient_id': 4},  # Glycerin

        # Lactic Acid Treatment
        {'product_id': 20, 'ingredient_id': 1},  # Water
        {'product_id': 20, 'ingredient_id': 22}, # Lactic Acid
        {'product_id': 20, 'ingredient_id': 4},  # Glycerin
        {'product_id': 20, 'ingredient_id': 5},   # Squalane

        # Galactomyces Essence
        {'product_id': 21, 'ingredient_id': 1},   # Water
        {'product_id': 21, 'ingredient_id': 6},   # Niacinamide
        {'product_id': 21, 'ingredient_id': 13},  # Butylene Glycol

        # Centella Calming Gel
        {'product_id': 22, 'ingredient_id': 1},   # Water
        {'product_id': 22, 'ingredient_id': 2},   # Centella Asiatica Extract
        {'product_id': 22, 'ingredient_id': 16},  # Allantoin

        # Oil-Free Moisturizer
        {'product_id': 23, 'ingredient_id': 1},   # Water
        {'product_id': 23, 'ingredient_id': 4},   # Glycerin
        {'product_id': 23, 'ingredient_id': 7},   # Hyaluronic Acid

        # Retinol Night Serum
        {'product_id': 24, 'ingredient_id': 1},   # Water
        {'product_id': 24, 'ingredient_id': 31},  # Retinol
        {'product_id': 24, 'ingredient_id': 24},  # Vitamin E

        # AHA/BHA Clarifying Treatment
        {'product_id': 25, 'ingredient_id': 1},   # Water
        {'product_id': 25, 'ingredient_id': 9},   # Glycolic Acid (AHA)
        {'product_id': 25, 'ingredient_id': 21},  # Salicylic Acid (BHA)

        # Cica Repair Balm
        {'product_id': 26, 'ingredient_id': 1},   # Water
        {'product_id': 26, 'ingredient_id': 2},   # Centella Asiatica Extract
        {'product_id': 26, 'ingredient_id': 20},  # Ceramide NP

        # Hydrating Cleansing Oil
        {'product_id': 27, 'ingredient_id': 26},  # Jojoba Oil
        {'product_id': 27, 'ingredient_id': 27},  # Argan Oil
        {'product_id': 27, 'ingredient_id': 24},  # Vitamin E

        # Nourishing Face Mist
        {'product_id': 28, 'ingredient_id': 1},   # Water
        {'product_id': 28, 'ingredient_id': 4},   # Glycerin
        {'product_id': 28, 'ingredient_id': 25},  # Aloe Vera Extract

        # Pore Refining Clay Mask
        {'product_id': 29, 'ingredient_id': 1},   # Water
        {'product_id': 29, 'ingredient_id': 21},  # Salicylic Acid
        {'product_id': 29, 'ingredient_id': 16},  # Allantoin

        # Vitamin E Night Oil
        {'product_id': 30, 'ingredient_id': 24},  # Vitamin E
        {'product_id': 30, 'ingredient_id': 26},  # Jojoba Oil
        {'product_id': 30, 'ingredient_id': 5},    # Squalane

        # Mugwort Essence
        {'product_id': 31, 'ingredient_id': 1},   # Water
        {'product_id': 31, 'ingredient_id': 36},  # Mugwort Extract
        {'product_id': 31, 'ingredient_id': 4},   # Glycerin

        # Bakuchiol Booster
        {'product_id': 32, 'ingredient_id': 37},  # Bakuchiol
        {'product_id': 32, 'ingredient_id': 26},  # Jojoba Oil
        {'product_id': 32, 'ingredient_id': 5},   # Squalane

        # Rosehip Seed Oil
        {'product_id': 33, 'ingredient_id': 38},  # Rosehip Seed Oil
        {'product_id': 33, 'ingredient_id': 24},  # Vitamin E

        # Lip Sleeping Mask
        {'product_id': 34, 'ingredient_id': 39},  # Shea Butter
        {'product_id': 34, 'ingredient_id': 4},   # Glycerin
        {'product_id': 34, 'ingredient_id': 24},  # Vitamin E

        # Green Tea Enzyme Powder Wash
        {'product_id': 35, 'ingredient_id': 40},  # Green Tea Extract
        {'product_id': 35, 'ingredient_id': 4},   # Glycerin
        {'product_id': 35, 'ingredient_id': 25},  # Aloe Vera Extract

        # Matcha Hemp Hydrating Cleanser
        {'product_id': 36, 'ingredient_id': 1},   # Water
        {'product_id': 36, 'ingredient_id': 42},  # Matcha Extract
        {'product_id': 36, 'ingredient_id': 41},  # Hemp Seed Oil

        # Kombucha Essence
        {'product_id': 37, 'ingredient_id': 1},   # Water
        {'product_id': 37, 'ingredient_id': 43},  # Kombucha Extract
        {'product_id': 37, 'ingredient_id': 4},   # Glycerin

        # Alpha Arbutin Solution
        {'product_id': 38, 'ingredient_id': 1},   # Water
        {'product_id': 38, 'ingredient_id': 44},  # Alpha Arbutin
        {'product_id': 38, 'ingredient_id': 7},   # Hyaluronic Acid

        # Fermented Rice Water Toner
        {'product_id': 39, 'ingredient_id': 1},   # Water
        {'product_id': 39, 'ingredient_id': 45},  # Fermented Rice Water
        {'product_id': 39, 'ingredient_id': 6},   # Niacinamide

        # Oat Cleansing Balm
        {'product_id': 40, 'ingredient_id': 46},  # Oat Extract
        {'product_id': 40, 'ingredient_id': 5},   # Squalane
        {'product_id': 40, 'ingredient_id': 39},   # Shea Butter

        # Brightening Treatment Essence
        {'product_id': 41, 'ingredient_id': 1},   # Water
        {'product_id': 41, 'ingredient_id': 48},  # Licorice Root Extract
        {'product_id': 41, 'ingredient_id': 6},   # Niacinamide

        # Tranexamic Acid Night Serum
        {'product_id': 42, 'ingredient_id': 1},   # Water
        {'product_id': 42, 'ingredient_id': 49},  # Tranexamic Acid
        {'product_id': 42, 'ingredient_id': 6},   # Niacinamide

        # Barrier Repair Moisturizer
        {'product_id': 43, 'ingredient_id': 1},   # Water
        {'product_id': 43, 'ingredient_id': 50},  # Urea
        {'product_id': 43, 'ingredient_id': 20},  # Ceramide NP

        # Mandelic Acid 10% Treatment
        {'product_id': 44, 'ingredient_id': 1},   # Water
        {'product_id': 44, 'ingredient_id': 51},  # Mandelic Acid
        {'product_id': 44, 'ingredient_id': 4},   # Glycerin

        # Virgin Marula Facial Oil
        {'product_id': 45, 'ingredient_id': 52},  # Marula Oil
        {'product_id': 45, 'ingredient_id': 24},  # Vitamin E

        # Avocado Melt Sleeping Mask
        {'product_id': 46, 'ingredient_id': 1},   # Water
        {'product_id': 46, 'ingredient_id': 53},  # Avocado Oil
        {'product_id': 46, 'ingredient_id': 4},   # Glycerin

        # Royal Honey Propolis Enrich Essence
        {'product_id': 47, 'ingredient_id': 1},   # Water
        {'product_id': 47, 'ingredient_id': 54},  # Honey Extract
        {'product_id': 47, 'ingredient_id': 34},  # Propolis Extract

        # Probiotic Power Treatment
        {'product_id': 48, 'ingredient_id': 1},   # Water
        {'product_id': 48, 'ingredient_id': 55},  # Bifida Ferment Lysate
        {'product_id': 48, 'ingredient_id': 7},   # Hyaluronic Acid

        # Firming Adenosine Cream
        {'product_id': 49, 'ingredient_id': 1},   # Water
        {'product_id': 49, 'ingredient_id': 56},  # Adenosine
        {'product_id': 49, 'ingredient_id': 32},  # Peptides

        # Antioxidant Youth Preserving Cream
        {'product_id': 50, 'ingredient_id': 1},   # Water
        {'product_id': 50, 'ingredient_id': 57},  # Coenzyme Q10
        {'product_id': 50, 'ingredient_id': 23}   # Vitamin C
    ]

    for product_ingredient_data in product_ingredients_data:
        # Kontrollera om produkt-ingrediens-relationen redan finns
        existing = db.query(ProductIngredient).filter(
            ProductIngredient.product_id == product_ingredient_data['product_id'],
            ProductIngredient.ingredient_id == product_ingredient_data['ingredient_id']
        ).first()
        
        if not existing:
            product_ingredient = ProductIngredient(**product_ingredient_data)
            db.add(product_ingredient)

    db.commit()

    # Skapa inkompatibla ingredienser
    incompatible_ingredients_data = [
        {'ingredient1_id': 8, 'ingredient2_id': 9},   # Retinal och Glycolic Acid
        {'ingredient1_id': 6, 'ingredient2_id': 8},   # Niacinamide och Retinal
        {'ingredient1_id': 6, 'ingredient2_id': 9},   # Niacinamide och Glycolic Acid
        {'ingredient1_id': 7, 'ingredient2_id': 9},   # Hyaluronic Acid och Glycolic Acid
        {'ingredient1_id': 8, 'ingredient2_id': 10},  # Retinal och Snail Secretion
        {'ingredient1_id': 23, 'ingredient2_id': 6},  # Vitamin C och Niacinamide
        {'ingredient1_id': 31, 'ingredient2_id': 9},  # Retinol och Glycolic Acid
        {'ingredient1_id': 31, 'ingredient2_id': 22}, # Retinol och Lactic Acid
        {'ingredient1_id': 31, 'ingredient2_id': 21}, # Retinol och Salicylic Acid
        {'ingredient1_id': 21, 'ingredient2_id': 9},   # Salicylic Acid och Glycolic Acid
        {'ingredient1_id': 51, 'ingredient2_id': 31},  # Mandelic Acid och Retinol
        {'ingredient1_id': 49, 'ingredient2_id': 9},   # Tranexamic Acid och Glycolic Acid
        {'ingredient1_id': 23, 'ingredient2_id': 51}   # Vitamin C och Mandelic Acid
    ]

    for incompatible_data in incompatible_ingredients_data:
        # Kontrollera om inkompatibiliteten redan finns
        existing = db.query(IncompatibleIngredient).filter(
            (IncompatibleIngredient.ingredient1_id == incompatible_data['ingredient1_id']) & 
            (IncompatibleIngredient.ingredient2_id == incompatible_data['ingredient2_id'])
        ).first()
        
        if not existing:
            incompatible = IncompatibleIngredient(**incompatible_data)
            db.add(incompatible)

    db.commit()

    # Skapa aktiva ingredienser 
    active_ingredients_data = [
        {'ingredient_id': 8},  # Retinal
        {'ingredient_id': 9},  # Glycolic Acid
        {'ingredient_id': 6},  # Niacinamide
        {'ingredient_id': 7},  # Hyaluronic Acid
        {'ingredient_id': 21}, # Salicylic Acid
        {'ingredient_id': 22}, # Lactic Acid
        {'ingredient_id': 23}, # Vitamin C
        {'ingredient_id': 31}, # Retinol
        {'ingredient_id': 32},  # Peptides
        {'ingredient_id': 37},  # Bakuchiol
        {'ingredient_id': 44},  # Alpha Arbutin
        {'ingredient_id': 49},  # Tranexamic Acid
        {'ingredient_id': 51},  # Mandelic Acid
        {'ingredient_id': 56},   # Adenosine
    ]

    for active_data in active_ingredients_data:
        # Kontrollera om aktiv ingrediens redan finns
        existing = db.query(ActiveIngredient).filter(
            ActiveIngredient.ingredient_id == active_data['ingredient_id']
        ).first()
        
        if not existing:
            active_ingredient = ActiveIngredient(**active_data)
            db.add(active_ingredient)

    db.commit()
    
    print("Hudvårdsprodukter och ingredienser har lagts till i databasen!")

except Exception as e:
    db.rollback()
    print(f"Ett fel uppstod: {e}")

finally:
    db.close()