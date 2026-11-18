"""
Sample realistic products data for SHOPORA e-commerce platform.
Total: 10 Categories x 10 Products = 100 Unique Products.
"""

CATEGORIES_DATA = [
    {
        "name": "Men's Pants",
        "slug": "mens-pants",
        "description": "Tailored trousers, casual chinos, rugged cargo pants, and premium denim jeans for men.",
        "image_url": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&auto=format&fit=crop&q=80"
    },
    {
        "name": "Women's Pants",
        "slug": "womens-pants",
        "description": "Chic high-waisted trousers, wide-leg palazzos, trendy cargos, and stretch denim.",
        "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800&auto=format&fit=crop&q=80"
    },
    {
        "name": "T-Shirts",
        "slug": "t-shirts",
        "description": "Premium 100% combed cotton, oversized graphic tees, and minimal crewneck essentials.",
        "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80"
    },
    {
        "name": "Shirts",
        "slug": "shirts",
        "description": "Crisp formal Oxford button-downs, casual linen resort shirts, and checkered overshirts.",
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&auto=format&fit=crop&q=80"
    },
    {
        "name": "Smartphones",
        "slug": "smartphones",
        "description": "Flagship 5G smartphones, foldable innovations, and pro camera powerhouses.",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&auto=format&fit=crop&q=80"
    },
    {
        "name": "Laptops",
        "slug": "laptops",
        "description": "Ultra-thin productivity ultrabooks, AI workstation laptops, and beastly gaming rigs.",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&auto=format&fit=crop&q=80"
    },
    {
        "name": "Electronics",
        "slug": "electronics",
        "description": "4K smart displays, mirrorless vlog cameras, power stations, and home audio gear.",
        "image_url": "https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=800&auto=format&fit=crop&q=80"
    },
    {
        "name": "Headphones",
        "slug": "headphones",
        "description": "Audiophile noise-cancelling wireless headphones, spatial audio earbuds, and studio monitors.",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80"
    },
    {
        "name": "Watches",
        "slug": "watches",
        "description": "Automatic skeleton luxury timepieces, hybrid smartwatch monitors, and chronograph classics.",
        "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&auto=format&fit=crop&q=80"
    },
    {
        "name": "Shoes",
        "slug": "shoes",
        "description": "High-performance marathon running sneakers, retro street kicks, and hand-stitched leather boots.",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80"
    }
]

PRODUCTS_DATA = [
    # 1. Men's Pants (10 products)
    {
        "category_slug": "mens-pants",
        "name": "Levi's 511 Slim Fit Stretch Jeans",
        "brand": "Levi's",
        "original_price": 3999,
        "discounted_price": 2799,
        "stock": 45,
        "rating": 4.6,
        "num_reviews": 128,
        "description": "Classic modern slim fit jeans engineered with Levi's Flex advanced stretch technology for maximum comfort and flexibility. Sits below the waist with a slim leg from hip to ankle.",
        "specifications": {"Fit": "Slim Fit", "Fabric": "99% Cotton, 1% Elastane", "Closure": "Zip Fly with Button", "Care": "Machine wash cold inside out"},
        "sizes": ["30", "32", "34", "36", "38"],
        "colors": ["Indigo Blue", "Washed Black", "Dark Stone"],
        "images": [
            "https://images.unsplash.com/photo-1542272604-780c96856592?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800&auto=format&fit=crop&q=80"
        ],
        "is_featured": True, "is_trending": True, "is_bestseller": True
    },
    {
        "category_slug": "mens-pants",
        "name": "Dockers Signature Iron-Free Khaki Chinos",
        "brand": "Dockers",
        "original_price": 3499,
        "discounted_price": 2449,
        "stock": 30,
        "rating": 4.4,
        "num_reviews": 84,
        "description": "Wrinkle-resistant luxury stretch khaki chinos tailored for boardroom meetings and weekend dinners alike. Features stain defender technology and shirt-gripper waistband.",
        "specifications": {"Fit": "Straight Tapered", "Fabric": "98% Cotton, 2% Spandex", "Pattern": "Solid Khaki", "Stretch": "4-Way Flex"},
        "sizes": ["30", "32", "34", "36"],
        "colors": ["British Khaki", "Navy Blue", "Olive Green"],
        "images": [
            "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "mens-pants",
        "name": "Zara Tailored Linen-Blend Trousers",
        "brand": "Zara",
        "original_price": 4290,
        "discounted_price": 3190,
        "stock": 25,
        "rating": 4.5,
        "num_reviews": 67,
        "description": "Smart pleated trousers crafted from breathable European linen blend. Features front darting, side welt pockets, and an elasticated waistband drawcord.",
        "specifications": {"Fit": "Relaxed Tailored", "Fabric": "55% Linen, 45% Cotton", "Rise": "Mid Rise", "Style": "Pleated Trouser"},
        "sizes": ["30", "32", "34", "36"],
        "colors": ["Sand Beige", "Charcoal Grey", "Off White"],
        "images": [
            "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "mens-pants",
        "name": "H&M Relaxed Fit Multi-Pocket Cargo Pants",
        "brand": "H&M",
        "original_price": 2999,
        "discounted_price": 2099,
        "stock": 40,
        "rating": 4.3,
        "num_reviews": 92,
        "description": "Heavyweight cotton twill utility cargo pants featuring ergonomic flap bellows pockets, reinforced knee stitching, and adjustable ankle cinch cords.",
        "specifications": {"Fit": "Relaxed Baggy", "Fabric": "100% Cotton Twill", "Pockets": "6 Ergonomic Pockets", "Rise": "Regular"},
        "sizes": ["30", "32", "34", "36", "38"],
        "colors": ["Army Green", "Stealth Black", "Coyote Brown"],
        "images": [
            "https://images.unsplash.com/photo-1517445312882-bc9910d016b7?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "mens-pants",
        "name": "Wrangler Rugged Wear Relaxed Bootcut Jeans",
        "brand": "Wrangler",
        "original_price": 3299,
        "discounted_price": 2299,
        "stock": 35,
        "rating": 4.5,
        "num_reviews": 110,
        "description": "Authentic western heritage denim built for durability and enduring style. Features iconic 'W' embroidery on back pockets and heavy-gauge brass rivets.",
        "specifications": {"Fit": "Classic Bootcut", "Fabric": "Heavyweight 14oz Denim", "Fly": "Zipper", "Origin": "Crafted with Pride"},
        "sizes": ["32", "34", "36", "38"],
        "colors": ["Heritage Stone", "Vintage Dark Tint"],
        "images": [
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "mens-pants",
        "name": "Uniqlo Ultra Stretch Active Jogger Pants",
        "brand": "Uniqlo",
        "original_price": 2490,
        "discounted_price": 1990,
        "stock": 50,
        "rating": 4.7,
        "num_reviews": 215,
        "description": "Quick-drying DRY-EX fabric with 360-degree all-way elasticity. Perfect for jogging, gym workouts, lounging, or commuting.",
        "specifications": {"Stretch": "360 Ultra Stretch", "Fabric": "Polyester Quick-Dry", "Waist": "Ribbed with Drawstring"},
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Heather Grey", "Matte Black", "Deep Navy"],
        "images": [
            "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "mens-pants",
        "name": "Tommy Hilfiger Mercer Regular Fit Chinos",
        "brand": "Tommy Hilfiger",
        "original_price": 5999,
        "discounted_price": 3899,
        "stock": 20,
        "rating": 4.6,
        "num_reviews": 53,
        "description": "Elevated preppy aesthetic tailored from organic stretch cotton sateen. Finished with subtle tri-color ribbon detail on coin pocket and back welt pockets.",
        "specifications": {"Fit": "Mercer Straight", "Fabric": "97% Organic Cotton, 3% Elastane", "Logo": "Embroidered Flag Logo"},
        "sizes": ["30", "32", "34", "36"],
        "colors": ["Desert Khaki", "Classic Navy", "Crisp White"],
        "images": [
            "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "mens-pants",
        "name": "Calvin Klein Slim Tapered Wool-Blend Trousers",
        "brand": "Calvin Klein",
        "original_price": 6999,
        "discounted_price": 4499,
        "stock": 18,
        "rating": 4.8,
        "num_reviews": 41,
        "description": "Minimalist luxury tailoring designed for sleek formal evenings. Made from Italian wool blend with natural drape and wrinkle resistance.",
        "specifications": {"Fit": "Slim Tapered", "Fabric": "Wool Blend Fine Weave", "Waist": "Hidden hook and bar"},
        "sizes": ["30", "32", "34", "36"],
        "colors": ["Midnight Charcoal", "Jet Black"],
        "images": [
            "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "mens-pants",
        "name": "Puma Tech Fleece Athleisure Track Pants",
        "brand": "Puma",
        "original_price": 2799,
        "discounted_price": 1799,
        "stock": 38,
        "rating": 4.3,
        "num_reviews": 79,
        "description": "Sporty thermal fleece track pants with taped zippered pockets, articulated knee darts for mobility, and reflective Puma cat branding.",
        "specifications": {"Fit": "Athletic Tapered", "Fabric": "Cotton-Poly Tech Fleece", "Pockets": "Waterproof Zip Pockets"},
        "sizes": ["M", "L", "XL", "XXL"],
        "colors": ["Medium Grey", "Dark Shadow Black"],
        "images": [
            "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "mens-pants",
        "name": "Allen Solly Prime Work-To-Weekend Chinos",
        "brand": "Allen Solly",
        "original_price": 2899,
        "discounted_price": 1899,
        "stock": 42,
        "rating": 4.4,
        "num_reviews": 95,
        "description": "The quintessential Friday dressing essential. Enzyme washed for exceptional softness and broken-in comfort right from day one.",
        "specifications": {"Fit": "Custom Fit", "Fabric": "100% Cotton Twill", "Wash": "Vintage Enzyme Wash"},
        "sizes": ["30", "32", "34", "36"],
        "colors": ["Olive Chino", "Smoky Beige", "Royal Navy"],
        "images": [
            "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&auto=format&fit=crop&q=80"
        ]
    },

    # 2. Women's Pants (10 products)
    {
        "category_slug": "womens-pants",
        "name": "Levi's Ribcage High-Rise Wide-Leg Jeans",
        "brand": "Levi's",
        "original_price": 4499,
        "discounted_price": 3149,
        "stock": 35,
        "rating": 4.7,
        "num_reviews": 140,
        "description": "Levi's highest high rise with a hip-slimming 12-inch rise and wide statement leg. Crafted from non-stretch vintage-inspired authentic denim.",
        "specifications": {"Rise": "Super High Rise (12 inches)", "Leg": "Wide Leg Opening", "Fabric": "100% Sustainable Cotton"},
        "sizes": ["26", "28", "30", "32"],
        "colors": ["Medium Authentic Indigo", "Vintage Bleach Wash"],
        "images": [
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800&auto=format&fit=crop&q=80"
        ],
        "is_featured": True, "is_bestseller": True
    },
    {
        "category_slug": "womens-pants",
        "name": "Zara Flowy High-Waisted Wide Leg Trousers",
        "brand": "Zara",
        "original_price": 3990,
        "discounted_price": 2790,
        "stock": 42,
        "rating": 4.6,
        "num_reviews": 118,
        "description": "Effortless drapey silhouette featuring front double pleats, side seam pockets, and an elongated floor-grazing hem for an ultra-chic runway look.",
        "specifications": {"Waist": "High Rise Elasticated Back", "Fabric": "Crepe Viscose Blend", "Care": "Gentle Machine Wash"},
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": ["Emerald Green", "Classic Black", "Champagne Cream"],
        "images": [
            "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "womens-pants",
        "name": "Mango Belted Linen-Blend Paperbag Trousers",
        "brand": "Mango",
        "original_price": 4590,
        "discounted_price": 3190,
        "stock": 28,
        "rating": 4.5,
        "num_reviews": 76,
        "description": "Summery breathable paperbag waist trousers accompanied by a matching tortoiseshell buckle belt and rolled cuff hems.",
        "specifications": {"Fit": "Relaxed Tapered", "Belt": "Included Detachable Belt", "Fabric": "70% Linen, 30% Cotton"},
        "sizes": ["S", "M", "L"],
        "colors": ["Warm Terracotta", "Natural Linen Ecru"],
        "images": [
            "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "womens-pants",
        "name": "H&M Slim-Fit Ankle Length Treggings",
        "brand": "H&M",
        "original_price": 1799,
        "discounted_price": 1299,
        "stock": 55,
        "rating": 4.4,
        "num_reviews": 182,
        "description": "The perfect hybrid between tailored trousers and ultra-comfy leggings. Thick stretch twill with false front pockets and functional back patch pockets.",
        "specifications": {"Length": "Ankle Length", "Fabric": "Cotton-Rayon-Elastane", "Rise": "Mid-Rise"},
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": ["Pitch Black", "Houndstooth Check", "Navy Blue"],
        "images": [
            "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "womens-pants",
        "name": "Lululemon Align High-Rise Flare Pants",
        "brand": "Lululemon",
        "original_price": 8900,
        "discounted_price": 6490,
        "stock": 22,
        "rating": 4.9,
        "num_reviews": 310,
        "description": "Buttery-soft Nulu fabric that feels weightless on the skin. Four-way stretch, sweat-wicking breathability, and flattering flared bootcut silhouette.",
        "specifications": {"Fabric": "Nulu Weightless Feel", "Inseam": "32.5 inches", "Pocket": "Hidden Waistband Pocket"},
        "sizes": ["2", "4", "6", "8", "10"],
        "colors": ["True Navy", "Black", "Java Brown"],
        "images": [
            "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "womens-pants",
        "name": "Marks & Spencer Sienna Straight Leg Denim",
        "brand": "Marks & Spencer",
        "original_price": 3599,
        "discounted_price": 2499,
        "stock": 34,
        "rating": 4.5,
        "num_reviews": 88,
        "description": "Flattering high-rise cut made with sustainably sourced BCI cotton and elastane for everyday shape retention without sagging.",
        "specifications": {"Fit": "Classic Straight Leg", "Fabric": "Cotton with Spandex Stretch", "Features": "Hold-You-In Pocket Bags"},
        "sizes": ["28", "30", "32", "34"],
        "colors": ["Dark Indigo", "Light Vintage Blue"],
        "images": [
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "womens-pants",
        "name": "Vero Moda High-Waist Cargo Joggers",
        "brand": "Vero Moda",
        "original_price": 3299,
        "discounted_price": 1999,
        "stock": 40,
        "rating": 4.3,
        "num_reviews": 64,
        "description": "Streetwear-inspired satin-sheen cargo pants featuring an elastic drawstring waistband and cuffed elastic ankles.",
        "specifications": {"Fit": "Relaxed Athleisure Cargo", "Material": "Polyester Lyocell Blend", "Details": "Side bellows pockets"},
        "sizes": ["S", "M", "L"],
        "colors": ["Sage Green", "Charcoal Slate", "Beige"],
        "images": [
            "https://images.unsplash.com/photo-1517445312882-bc9910d016b7?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "womens-pants",
        "name": "AND Contemporary Front-Slit Formal Trousers",
        "brand": "AND",
        "original_price": 2999,
        "discounted_price": 1899,
        "stock": 26,
        "rating": 4.4,
        "num_reviews": 47,
        "description": "Contemporary power trousers designed with distinctive front ankle slits to beautifully showcase heels or pointy flats.",
        "specifications": {"Fit": "Slim Formal", "Detail": "Front Ankle Slit", "Waist": "High Rise Tailored Band"},
        "sizes": ["28", "30", "32", "34"],
        "colors": ["Raven Black", "Ruby Burgundy"],
        "images": [
            "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "womens-pants",
        "name": "Forever 21 Retro Corduroy Wide Leg Pants",
        "brand": "Forever 21",
        "original_price": 2499,
        "discounted_price": 1699,
        "stock": 30,
        "rating": 4.2,
        "num_reviews": 51,
        "description": "70s vintage aesthetic revived in cozy wide-wale ribbed corduroy fabric. High-rise fit with dual front patch pockets.",
        "specifications": {"Texture": "Wide-Wale Corduroy", "Fit": "Wide Leg Retro", "Material": "100% Cotton"},
        "sizes": ["26", "28", "30", "32"],
        "colors": ["Rust Orange", "Chocolate Brown", "Cream"],
        "images": [
            "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "womens-pants",
        "name": "Only Royal High Rise Skinny Jeans",
        "brand": "Only",
        "original_price": 2799,
        "discounted_price": 1799,
        "stock": 48,
        "rating": 4.5,
        "num_reviews": 115,
        "description": "Body-hugging skinny jeans featuring power-stretch recovery that sculpts your silhouette and never loses its shape over time.",
        "specifications": {"Fit": "Skinny Ankle", "Stretch": "Power Stretch 45%", "Waist": "High Rise Contoured"},
        "sizes": ["26", "28", "30", "32", "34"],
        "colors": ["Jet Black", "Mid Blue Wash"],
        "images": [
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800&auto=format&fit=crop&q=80"
        ]
    },

    # 3. T-Shirts (10 products)
    {
        "category_slug": "t-shirts",
        "name": "Nike Dri-FIT Legend Athletic Training Tee",
        "brand": "Nike",
        "original_price": 1995,
        "discounted_price": 1395,
        "stock": 60,
        "rating": 4.7,
        "num_reviews": 230,
        "description": "Lightweight sweat-wicking polyester tee with anti-odor finish to keep you fresh through intense gym sessions, cardio, and running.",
        "specifications": {"Technology": "Dri-FIT Moisture Management", "Fit": "Standard Athletic", "Material": "100% Recycled Polyester"},
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": ["Obsidian Blue", "Iron Grey", "Volt Lime"],
        "images": [
            "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80"
        ],
        "is_featured": True, "is_bestseller": True
    },
    {
        "category_slug": "t-shirts",
        "name": "Adidas Originals Trefoil Heavyweight Graphic Tee",
        "brand": "Adidas",
        "original_price": 2499,
        "discounted_price": 1749,
        "stock": 45,
        "rating": 4.6,
        "num_reviews": 165,
        "description": "Iconic heritage Trefoil streetwear graphic screen-printed on ultra-soft 240 GSM single jersey heavyweight cotton.",
        "specifications": {"GSM": "240 Heavyweight", "Collar": "Ribbed Crewneck", "Fabric": "Better Cotton Initiative Single Jersey"},
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Cloud White", "Core Black", "Collegiate Green"],
        "images": [
            "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "t-shirts",
        "name": "Puma Classic Cat Regular Fit Crew Tee",
        "brand": "Puma",
        "original_price": 1499,
        "discounted_price": 899,
        "stock": 70,
        "rating": 4.4,
        "num_reviews": 190,
        "description": "Essential everyday cotton t-shirt with rubberized heat-transfer Puma Archive No. 1 logo at the left chest.",
        "specifications": {"Material": "100% Breathable Cotton", "Neck": "Crew Neck", "Sleeve": "Short Sleeve"},
        "sizes": ["M", "L", "XL", "XXL"],
        "colors": ["White", "Black", "Royal Blue", "High Risk Red"],
        "images": [
            "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "t-shirts",
        "name": "Uniqlo Supima Cotton Crew Neck T-Shirt",
        "brand": "Uniqlo",
        "original_price": 1490,
        "discounted_price": 1190,
        "stock": 80,
        "rating": 4.8,
        "num_reviews": 340,
        "description": "Made from 100% rare, long-staple Supima cotton renowned for its natural luster, silk-like softness, and superior colorfastness.",
        "specifications": {"Cotton": "100% American Supima", "Feel": "Silky and Smooth", "Hem": "Clean Blind Stitch"},
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Navy", "White", "Black", "Olive", "Heather Grey"],
        "images": [
            "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "t-shirts",
        "name": "Zara Oversized Acid Wash Heavyweight Tee",
        "brand": "Zara",
        "original_price": 2290,
        "discounted_price": 1590,
        "stock": 35,
        "rating": 4.5,
        "num_reviews": 78,
        "description": "Boxy drop-shoulder silhouette treated with an authentic mineral acid wash for a unique faded vintage grunge look.",
        "specifications": {"Fit": "Boxy Oversized", "Shoulder": "Dropped Shoulder", "Fabric": "100% Heavy Cotton 260 GSM"},
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Acid Grey", "Washed Olive", "Vintage Lilac"],
        "images": [
            "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "t-shirts",
        "name": "Under Armour Tech 2.0 Short Sleeve Tee",
        "brand": "Under Armour",
        "original_price": 2199,
        "discounted_price": 1539,
        "stock": 40,
        "rating": 4.6,
        "num_reviews": 112,
        "description": "UA Tech fabric has an ultra-soft, more natural feel for unrivaled comfort. Wicks sweat and dries incredibly fast.",
        "specifications": {"Fit": "Fuller Cut Loose Fit", "Material": "100% Polyester", "Anti-Odor": "Prevents Odor-Causing Microbes"},
        "sizes": ["M", "L", "XL"],
        "colors": ["Pitch Gray", "Academy Navy", "Black"],
        "images": [
            "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "t-shirts",
        "name": "Tommy Hilfiger Signature Embroidered Flag Tee",
        "brand": "Tommy Hilfiger",
        "original_price": 3299,
        "discounted_price": 2199,
        "stock": 25,
        "rating": 4.5,
        "num_reviews": 68,
        "description": "Timeless collegiate style crafted from pure organic cotton jersey with the distinguished mini flag embroidered on the chest.",
        "specifications": {"Fit": "Regular Modern", "Material": "100% Transitional Organic Cotton", "Collar": "Rib-Knit"},
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Master Navy", "Snow White", "Crimson Red"],
        "images": [
            "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "t-shirts",
        "name": "H&M 3-Pack Slim Fit Organic Crewneck Tees",
        "brand": "H&M",
        "original_price": 2499,
        "discounted_price": 1799,
        "stock": 50,
        "rating": 4.3,
        "num_reviews": 142,
        "description": "Essential wardrobe multipack consisting of three clean-cut crewneck t-shirts made from soft, certified organic cotton.",
        "specifications": {"Pack": "3 T-Shirts Included", "Material": "100% Organic Cotton", "Cut": "Fitted Silhouette"},
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Black/White/Grey Multi", "Navy/Olive/White Multi"],
        "images": [
            "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "t-shirts",
        "name": "Calvin Klein Monogram Logo Stretch Cotton Tee",
        "brand": "Calvin Klein",
        "original_price": 3499,
        "discounted_price": 2299,
        "stock": 28,
        "rating": 4.6,
        "num_reviews": 59,
        "description": "Sculpted slim tee featuring iconic CK monogram chest graphic and elastane-infused stretch cotton for all-day comfort.",
        "specifications": {"Fit": "Slim Body Fit", "Fabric": "95% Cotton, 5% Elastane", "Graphic": "Matte High-Density Print"},
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Bright White", "Caviar Black"],
        "images": [
            "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "t-shirts",
        "name": "Jack & Jones Graphic Print Skate Tee",
        "brand": "Jack & Jones",
        "original_price": 1699,
        "discounted_price": 999,
        "stock": 65,
        "rating": 4.2,
        "num_reviews": 87,
        "description": "Youthful energetic skate culture inspired graphic print tee finished in high-twist ring-spun combed cotton.",
        "specifications": {"Fit": "Regular Crew", "Print": "Soft Handfeel Discharge Ink", "Origin": "Combed Cotton"},
        "sizes": ["M", "L", "XL"],
        "colors": ["Sun Yellow", "Washed Teal", "Black"],
        "images": [
            "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80"
        ]
    },

    # 4. Shirts (10 products)
    {
        "category_slug": "shirts",
        "name": "Ralph Lauren Classic Fit Oxford Cotton Shirt",
        "brand": "Polo Ralph Lauren",
        "original_price": 8990,
        "discounted_price": 6290,
        "stock": 25,
        "rating": 4.8,
        "num_reviews": 96,
        "description": "The quintessential Ivy League wardrobe cornerstone. Made from durable, breathable Oxford cotton with button-down point collar and signature Pony embroidery.",
        "specifications": {"Fit": "Classic Roomy Fit", "Weave": "Traditional Oxford Cotton Weave", "Collar": "Button-Down Collar"},
        "sizes": ["38", "40", "42", "44"],
        "colors": ["Oxford Blue", "Classic White", "Pink University Stripe"],
        "images": [
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=80"
        ],
        "is_featured": True, "is_bestseller": True
    },
    {
        "category_slug": "shirts",
        "name": "Zara Resort Relaxed 100% Linen Shirt",
        "brand": "Zara",
        "original_price": 3990,
        "discounted_price": 2790,
        "stock": 35,
        "rating": 4.6,
        "num_reviews": 82,
        "description": "Airy cuban-collar camp shirt cut from 100% European pure linen. Relaxed boxy drape made for sun-soaked beach vacations and rooftop evenings.",
        "specifications": {"Material": "100% Pure European Linen", "Collar": "Cuban Camp Collar", "Buttons": "Natural Mother of Pearl"},
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Olive Sage", "Sky Azure", "Optic White"],
        "images": [
            "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "shirts",
        "name": "Tommy Hilfiger Non-Iron Poplin Slim Shirt",
        "brand": "Tommy Hilfiger",
        "original_price": 6499,
        "discounted_price": 4299,
        "stock": 30,
        "rating": 4.7,
        "num_reviews": 65,
        "description": "Executive high-thread-count poplin shirt finished with non-iron technology to stay immaculate from 9 AM presentations to late dinners.",
        "specifications": {"Finish": "Wrinkle-Free Non-Iron", "Fit": "Fitted Slim Silhouette", "Cuffs": "Double Button Convertible"},
        "sizes": ["39", "40", "42", "44"],
        "colors": ["Crisp White", "French Blue", "Micro Grid Print"],
        "images": [
            "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "shirts",
        "name": "Levi's Barstow Western Denim Snap Shirt",
        "brand": "Levi's",
        "original_price": 3899,
        "discounted_price": 2599,
        "stock": 40,
        "rating": 4.6,
        "num_reviews": 118,
        "description": "An authentic western frontier shirt worn by pioneers and outlaws. Features pointed western front and back yokes and pearlescent snap buttons.",
        "specifications": {"Hardware": "Pearlized Snap Fasteners", "Pockets": "Flap Snap Pockets with Red Tab", "Fabric": "100% Washed Cotton Denim"},
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Light Stonewash", "Dark Indigo Rinse"],
        "images": [
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "shirts",
        "name": "Louis Philippe Gods & Kings Egyptian Giza Shirt",
        "brand": "Louis Philippe",
        "original_price": 4999,
        "discounted_price": 3299,
        "stock": 24,
        "rating": 4.7,
        "num_reviews": 51,
        "description": "Crafted from long-staple Egyptian Giza 88 cotton with an opulent silken handfeel and lustrous sheen tailored for luxury celebrations.",
        "specifications": {"Yarn": "2-Ply 100s Giza Cotton", "Collar": "Cutaway Formal Collar", "Stitching": "18 Stitches Per Inch"},
        "sizes": ["39", "40", "42", "44"],
        "colors": ["Platinum White", "Blush Pink", "Powder Blue"],
        "images": [
            "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "shirts",
        "name": "H&M Regular Fit Heavy Flannel Overshirt",
        "brand": "H&M",
        "original_price": 2999,
        "discounted_price": 2099,
        "stock": 42,
        "rating": 4.4,
        "num_reviews": 88,
        "description": "Brushed heavyweight cotton flannel shirt ideal for autumnal layering over t-shirts. Features dual buttoned chest pockets and sturdy tortoise buttons.",
        "specifications": {"Pattern": "Buffalo Plaid Check", "Material": "Brushed Heavy Cotton Flannel", "Fit": "Overshirt Layering Fit"},
        "sizes": ["M", "L", "XL", "XXL"],
        "colors": ["Red & Black Check", "Forest Green Tartan"],
        "images": [
            "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "shirts",
        "name": "Arrow President Mercerized Cotton Shirt",
        "brand": "Arrow",
        "original_price": 3299,
        "discounted_price": 2199,
        "stock": 38,
        "rating": 4.5,
        "num_reviews": 74,
        "description": "Designed for corporate boardroom excellence. Double mercerized cotton fabric enhances luster and strength while remaining silky soft.",
        "specifications": {"Collar": "Semi-Spread Collar", "Pattern": "Fine Dobby Weave", "Cuffs": "Mitred 2-Button Cuffs"},
        "sizes": ["39", "40", "42", "44"],
        "colors": ["Ice Blue", "Lilac Mist"],
        "images": [
            "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "shirts",
        "name": "Uniqlo Premium Linen Long Sleeve Shirt",
        "brand": "Uniqlo",
        "original_price": 2990,
        "discounted_price": 2290,
        "stock": 50,
        "rating": 4.7,
        "num_reviews": 160,
        "description": "Woven from 100% fine French flax linen that gets softer with every single wash. Cool and crisp feel even in tropical humid heat.",
        "specifications": {"Origin": "100% French Flax Linen", "Fit": "Regular Straight", "Collar": "Regular Point Collar"},
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Natural Flax", "Navy Blue", "Pure White"],
        "images": [
            "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "shirts",
        "name": "Van Heusen Ultra Slim Stretch Dress Shirt",
        "brand": "Van Heusen",
        "original_price": 2799,
        "discounted_price": 1899,
        "stock": 35,
        "rating": 4.3,
        "num_reviews": 62,
        "description": "Dynamic flex fabric moves with your torso for unrestricted mobility throughout long conference meetings.",
        "specifications": {"Stretch": "2-Way Mechanical Stretch", "Fit": "Ultra Slim Tapered", "Fabric": "Cotton-Poly-Elastane"},
        "sizes": ["38", "40", "42", "44"],
        "colors": ["Charcoal Grey", "Steel Blue", "White"],
        "images": [
            "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "shirts",
        "name": "U.S. Polo Assn. Tailored Stripe Casual Shirt",
        "brand": "U.S. Polo Assn.",
        "original_price": 2699,
        "discounted_price": 1699,
        "stock": 44,
        "rating": 4.4,
        "num_reviews": 91,
        "description": "Sporty vertical candy stripe casual shirt featuring contrasting collar lining and double horseman logo embroidery on chest.",
        "specifications": {"Fit": "Custom Casual Fit", "Material": "100% Combed Cotton", "Yarn": "Yarn-Dyed Stripe"},
        "sizes": ["M", "L", "XL", "XXL"],
        "colors": ["Navy & Red Stripe", "Sky Blue Stripe"],
        "images": [
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&auto=format&fit=crop&q=80"
        ]
    },

    # 5. Smartphones (10 products)
    {
        "category_slug": "smartphones",
        "name": "Apple iPhone 16 Pro Max (256 GB)",
        "brand": "Apple",
        "original_price": 144900,
        "discounted_price": 139900,
        "stock": 25,
        "rating": 4.9,
        "num_reviews": 320,
        "description": "Forged in Grade 5 Titanium with stunning 6.9-inch Super Retina XDR display, A18 Pro chip, 48MP Fusion camera system with Camera Control button, and 4K 120 fps Dolby Vision recording.",
        "specifications": {"Display": "6.9-inch Super Retina XDR OLED 120Hz", "Processor": "A18 Pro with 6-core GPU", "Camera": "48MP Main + 48MP Ultra Wide + 12MP 5x Telephoto", "Battery": "Up to 33 hours video playback", "OS": "iOS 18"},
        "sizes": ["128GB", "256GB", "512GB", "1TB"],
        "colors": ["Desert Titanium", "Natural Titanium", "White Titanium", "Black Titanium"],
        "images": [
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&auto=format&fit=crop&q=80"
        ],
        "is_featured": True, "is_trending": True, "is_bestseller": True
    },
    {
        "category_slug": "smartphones",
        "name": "Samsung Galaxy S24 Ultra 5G AI Phone",
        "brand": "Samsung",
        "original_price": 134999,
        "discounted_price": 124999,
        "stock": 30,
        "rating": 4.8,
        "num_reviews": 290,
        "description": "The ultimate Galaxy AI powerhouse with built-in S-Pen, Titanium armor frame, 200MP Quad Telephoto camera with 100x Space Zoom, and Snapdragon 8 Gen 3 for Galaxy.",
        "specifications": {"Display": "6.8-inch Dynamic AMOLED 2X QHD+ 2600 nits", "Processor": "Snapdragon 8 Gen 3", "Camera": "200MP + 50MP + 12MP + 10MP", "Battery": "5000 mAh 45W Fast Charge"},
        "sizes": ["256GB", "512GB", "1TB"],
        "colors": ["Titanium Gray", "Titanium Black", "Titanium Violet"],
        "images": [
            "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "smartphones",
        "name": "Google Pixel 9 Pro with Gemini Nano",
        "brand": "Google",
        "original_price": 109999,
        "discounted_price": 99999,
        "stock": 20,
        "rating": 4.7,
        "num_reviews": 145,
        "description": "Google's most advanced phone featuring the powerful Tensor G4 processor, pro triple camera system with Super Res Zoom up to 30x, and 7 years of Pixel OS updates.",
        "specifications": {"Display": "6.3-inch Super Actua LTPO OLED 120Hz", "Processor": "Google Tensor G4 with Titan M2", "Camera": "50MP Wide + 48MP Ultrawide + 48MP Telephoto", "AI": "Deep Gemini Nano Built-In"},
        "sizes": ["128GB", "256GB", "512GB"],
        "colors": ["Obsidian", "Porcelain", "Hazel", "Rose Quartz"],
        "images": [
            "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "smartphones",
        "name": "OnePlus 12 5G Hasselblad Flagship",
        "brand": "OnePlus",
        "original_price": 64999,
        "discounted_price": 59999,
        "stock": 40,
        "rating": 4.7,
        "num_reviews": 210,
        "description": "Smooth Beyond Belief with Snapdragon 8 Gen 3, 4th Gen Hasselblad Camera System, 5400 mAh Battery with 100W SUPERVOOC charging, and 2K 120Hz ProXDR display.",
        "specifications": {"Display": "6.82-inch 2K 120Hz ProXDR 4500 nits", "Charging": "100W SuperVOOC (1-100% in 26 mins)", "RAM": "16GB LPDDR5X", "Storage": "512GB UFS 4.0"},
        "sizes": ["256GB", "512GB"],
        "colors": ["Flowy Emerald", "Silky Black"],
        "images": [
            "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "smartphones",
        "name": "Xiaomi 14 Ultra Leica Quad Camera",
        "brand": "Xiaomi",
        "original_price": 99999,
        "discounted_price": 89999,
        "stock": 15,
        "rating": 4.8,
        "num_reviews": 84,
        "description": "Pinnacle mobile optics co-engineered with Leica. Features 1-inch LYT-900 image sensor with stepless variable aperture f/1.63-f/4.0 and liquid lenses.",
        "specifications": {"Camera": "Quad 50MP Leica Optics 1-inch sensor", "Processor": "Snapdragon 8 Gen 3", "Body": "High-strength Aluminum & Vegan Leather"},
        "sizes": ["512GB"],
        "colors": ["Black", "White"],
        "images": [
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "smartphones",
        "name": "Nothing Phone (2) Glyph Interface",
        "brand": "Nothing",
        "original_price": 44999,
        "discounted_price": 36999,
        "stock": 35,
        "rating": 4.5,
        "num_reviews": 160,
        "description": "Transparent architectural design with dynamic Glyph LED lighting interface, Snapdragon 8+ Gen 1, dual 50MP Sony sensors, and clean Nothing OS 2.5.",
        "specifications": {"Interface": "Glyph Interface with 33 zones", "Display": "6.7-inch OLED LTPO 120Hz", "Processor": "Snapdragon 8+ Gen 1"},
        "sizes": ["128GB", "256GB", "512GB"],
        "colors": ["Dark Grey", "White"],
        "images": [
            "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "smartphones",
        "name": "Vivo X100 Pro ZEISS Telephoto Sunshot",
        "brand": "Vivo",
        "original_price": 89999,
        "discounted_price": 79999,
        "stock": 20,
        "rating": 4.7,
        "num_reviews": 92,
        "description": "ZEISS APO Floating Telephoto camera with MediaTek Dimensity 9300 flagship chip, V3 imaging chip, and 5400 mAh dual-cell battery with 100W flash charging.",
        "specifications": {"Camera": "50MP 1-inch ZEISS APO Telephoto", "Processor": "MediaTek Dimensity 9300", "Battery": "5400mAh 100W FlashCharge"},
        "sizes": ["512GB"],
        "colors": ["Asteroid Black", "Sunset Orange"],
        "images": [
            "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "smartphones",
        "name": "Realme GT 6 AI Flagship Killer",
        "brand": "Realme",
        "original_price": 40999,
        "discounted_price": 35999,
        "stock": 45,
        "rating": 4.5,
        "num_reviews": 130,
        "description": "Equipped with Snapdragon 8s Gen 3, world's brightest 6000-nit Ultra Display, 50MP Sony LYT-808 OIS main camera, and 120W GaN fast charger in box.",
        "specifications": {"Brightness": "6000 nits Peak Brightness", "Chip": "Snapdragon 8s Gen 3", "Charging": "120W GaN SuperVOOC"},
        "sizes": ["256GB", "512GB"],
        "colors": ["Fluid Silver", "Razor Green"],
        "images": [
            "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "smartphones",
        "name": "Motorola Edge 50 Ultra Pantone Leather",
        "brand": "Motorola",
        "original_price": 59999,
        "discounted_price": 49999,
        "stock": 25,
        "rating": 4.6,
        "num_reviews": 75,
        "description": "Pantone curated natural real wood and vegan suede back finishes. Features 144Hz curved pOLED display, IP68 underwater protection, and 125W TurboPower.",
        "specifications": {"Display": "6.7-inch 144Hz Super HD pOLED", "Back Panel": "Genuine Nordic Wood / Vegan Leather", "Protection": "IP68 Submersible"},
        "sizes": ["512GB"],
        "colors": ["Peach Fuzz", "Nordic Wood", "Forest Grey"],
        "images": [
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "smartphones",
        "name": "Samsung Galaxy Z Fold 6 Slim 5G",
        "brand": "Samsung",
        "original_price": 164999,
        "discounted_price": 154999,
        "stock": 12,
        "rating": 4.8,
        "num_reviews": 115,
        "description": "Slimmer, lighter, and more durable dual-screen foldable tablet phone with Galaxy AI live interpreter, ray-tracing gaming, and Armor Aluminum frame.",
        "specifications": {"Main Screen": "7.6-inch Dynamic AMOLED 2X Infinity Flex", "Cover Screen": "6.3-inch AMOLED 120Hz", "Hinge": "Dual Rail FlexHinge"},
        "sizes": ["256GB", "512GB"],
        "colors": ["Silver Shadow", "Navy", "Pink"],
        "images": [
            "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&auto=format&fit=crop&q=80"
        ]
    },

    # 6. Laptops (10 products)
    {
        "category_slug": "laptops",
        "name": "Apple MacBook Pro 16-inch M3 Max (36GB/1TB)",
        "brand": "Apple",
        "original_price": 349900,
        "discounted_price": 319900,
        "stock": 15,
        "rating": 4.9,
        "num_reviews": 180,
        "description": "Mind-blowing speed with M3 Max 14-core CPU and 30-core GPU, Liquid Retina XDR display with 1600 nits peak HDR brightness, and up to 22 hours of battery life.",
        "specifications": {"Processor": "Apple M3 Max 14-core CPU", "RAM": "36GB Unified Memory", "Storage": "1TB Blazing PCIe SSD", "Display": "16.2-inch Liquid Retina XDR 120Hz ProMotion"},
        "sizes": ["512GB", "1TB", "2TB"],
        "colors": ["Space Black", "Silver"],
        "images": [
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&auto=format&fit=crop&q=80"
        ],
        "is_featured": True, "is_trending": True, "is_bestseller": True
    },
    {
        "category_slug": "laptops",
        "name": "Dell XPS 14 Core Ultra 7 OLED Laptop",
        "brand": "Dell",
        "original_price": 199990,
        "discounted_price": 179990,
        "stock": 18,
        "rating": 4.7,
        "num_reviews": 85,
        "description": "Machined CNC aluminum chassis with seamless glass touchpad and touch function row. Features 3.2K InfinityEdge OLED touchscreen with NVIDIA RTX 4050 graphics.",
        "specifications": {"CPU": "Intel Core Ultra 7 155H with NPU", "GPU": "NVIDIA GeForce RTX 4050 6GB", "Display": "14.5-inch 3.2K OLED 120Hz Touch", "Weight": "1.68 kg"},
        "sizes": ["16GB RAM / 1TB SSD", "32GB RAM / 1TB SSD"],
        "colors": ["Platinum Silver", "Graphite"],
        "images": [
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "laptops",
        "name": "ASUS ROG Zephyrus G16 OLED Gaming Beast",
        "brand": "ASUS",
        "original_price": 239990,
        "discounted_price": 209990,
        "stock": 20,
        "rating": 4.8,
        "num_reviews": 110,
        "description": "Ultra-thin 1.49cm aluminum gaming laptop powered by AMD Ryzen AI 9 and RTX 4080 GPU. Features 2.5K 240Hz ROG Nebula OLED display with G-SYNC.",
        "specifications": {"Processor": "AMD Ryzen 9 8945HS", "Graphics": "NVIDIA RTX 4080 12GB GDDR6", "Display": "16-inch 2.5K 240Hz OLED 0.2ms", "Audio": "6-speaker system with Dolby Atmos"},
        "sizes": ["32GB / 1TB SSD", "32GB / 2TB SSD"],
        "colors": ["Eclipse Gray", "Platinum White"],
        "images": [
            "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "laptops",
        "name": "Apple MacBook Air 13-inch M3 (16GB/512GB)",
        "brand": "Apple",
        "original_price": 134900,
        "discounted_price": 119900,
        "stock": 35,
        "rating": 4.9,
        "num_reviews": 260,
        "description": "Incredibly thin at just 11.3 mm with silent fanless design, up to 18 hours battery life, Liquid Retina display, 1080p FaceTime HD camera, and dual external display support.",
        "specifications": {"Chip": "Apple M3 8-core CPU / 10-core GPU", "Memory": "16GB Unified Memory", "Storage": "512GB SSD", "Weight": "1.24 kg"},
        "sizes": ["256GB", "512GB"],
        "colors": ["Midnight", "Starlight", "Space Grey", "Silver"],
        "images": [
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "laptops",
        "name": "Lenovo ThinkPad X1 Carbon Gen 12",
        "brand": "Lenovo",
        "original_price": 184990,
        "discounted_price": 159990,
        "stock": 22,
        "rating": 4.7,
        "num_reviews": 94,
        "description": "The gold standard for enterprise business executives. Featherlight carbon fiber and magnesium chassis weighing just 1.09 kg with legendary spill-resistant ThinkPad keyboard.",
        "specifications": {"CPU": "Intel Core Ultra 7 165U", "Security": "dTPM 2.0 & Fingerprint reader", "Keyboard": "TrackPoint and glass trackpad", "Weight": "1.09 kg"},
        "sizes": ["16GB / 512GB", "32GB / 1TB"],
        "colors": ["Deep Black Weave"],
        "images": [
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "laptops",
        "name": "HP Spectre x360 2-in-1 14 OLED Touch",
        "brand": "HP",
        "original_price": 169999,
        "discounted_price": 149999,
        "stock": 25,
        "rating": 4.6,
        "num_reviews": 79,
        "description": "Versatile convertible 360-degree hinge with 2.8K IMAX Enhanced OLED touch display, 9MP AI camera with night mode, and magnetic rechargeable MPP2.0 stylus pen.",
        "specifications": {"Design": "Gem-cut CNC 2-in-1 Convertible", "Screen": "14-inch 2.8K OLED 120Hz Touch", "Stylus": "HP Rechargeable MPP2.0 Tilt Pen included"},
        "sizes": ["16GB / 1TB SSD"],
        "colors": ["Nightfall Black", "Slate Blue"],
        "images": [
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "laptops",
        "name": "Lenovo Legion Pro 7i Gen 9 AI Gaming Rig",
        "brand": "Lenovo",
        "original_price": 289990,
        "discounted_price": 254990,
        "stock": 14,
        "rating": 4.8,
        "num_reviews": 98,
        "description": "Brutal gaming muscle featuring Intel Core i9-14900HX, RTX 4090 with 175W TGP, Legion ColdFront vapor chamber cooling, and 240Hz PureSight gaming screen.",
        "specifications": {"CPU": "Intel Core i9-14900HX 24-cores", "GPU": "NVIDIA RTX 4090 16GB (175W TGP)", "Display": "16-inch WQXGA 240Hz 500 nits 100% DCI-P3"},
        "sizes": ["32GB / 2TB SSD"],
        "colors": ["Onyx Grey"],
        "images": [
            "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "laptops",
        "name": "Microsoft Surface Laptop 7 Copilot+ PC",
        "brand": "Microsoft",
        "original_price": 142999,
        "discounted_price": 128999,
        "stock": 28,
        "rating": 4.6,
        "num_reviews": 67,
        "description": "Next-gen AI Copilot+ PC powered by Snapdragon X Elite processor with 45 TOPS NPU, vibrant PixelSense Flow touchscreen, and all-day 20-hour battery life.",
        "specifications": {"Platform": "Snapdragon X Elite 12-core with 45 TOPS NPU", "Display": "13.8-inch PixelSense Flow Touch 120Hz", "Battery": "Up to 20 hours"},
        "sizes": ["16GB / 512GB", "32GB / 1TB"],
        "colors": ["Sapphire Blue", "Dune Gold", "Platinum"],
        "images": [
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "laptops",
        "name": "Acer Predator Helios 16 165Hz Gaming Laptop",
        "brand": "Acer",
        "original_price": 159999,
        "discounted_price": 129999,
        "stock": 30,
        "rating": 4.5,
        "num_reviews": 124,
        "description": "Dominate competitive esports with 14th Gen Intel Core i7, NVIDIA RTX 4070, dual 5th Gen AeroBlade 3D fans with liquid metal thermal grease.",
        "specifications": {"CPU": "Intel Core i7-14700HX", "GPU": "NVIDIA GeForce RTX 4070 8GB", "Thermal": "AeroBlade 3D Fans + Liquid Metal"},
        "sizes": ["16GB / 1TB SSD"],
        "colors": ["Abyssal Black with RGB Lightbar"],
        "images": [
            "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "laptops",
        "name": "ASUS Zenbook S 13 OLED Ultraportable",
        "brand": "ASUS",
        "original_price": 129990,
        "discounted_price": 109990,
        "stock": 25,
        "rating": 4.7,
        "num_reviews": 88,
        "description": "The world's slimmest OLED laptop at merely 1cm thin and 1kg featherlight. Eco-friendly plasma ceramic aluminum chassis with 2.8K ASUS Lumina OLED display.",
        "specifications": {"Weight": "1.00 kg", "Thickness": "1.0 cm", "Display": "13.3-inch 2.8K Lumina OLED 550 nits", "CPU": "Intel Core Ultra 7 155U"},
        "sizes": ["16GB / 1TB SSD"],
        "colors": ["Basalt Grey", "Ponder Blue"],
        "images": [
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&auto=format&fit=crop&q=80"
        ]
    },

    # 7. Electronics (10 products)
    {
        "category_slug": "electronics",
        "name": "Sony Alpha 7 IV Full-Frame Mirrorless Camera",
        "brand": "Sony",
        "original_price": 242990,
        "discounted_price": 209990,
        "stock": 16,
        "rating": 4.9,
        "num_reviews": 175,
        "description": "The benchmark hybrid content creator camera with 33MP Exmor R back-illuminated CMOS sensor, BIONZ XR processing engine, 4K 60p recording, and real-time human/animal eye autofocus.",
        "specifications": {"Sensor": "33MP Full-Frame Exmor R CMOS", "ISO": "50-204800 extended", "Video": "4K 60p 10-bit 4:2:2 All-Intra", "Stabilization": "5-axis In-body Optical (5.5 stops)"},
        "sizes": ["Body Only", "With 28-70mm Lens"],
        "colors": ["Matte Black"],
        "images": [
            "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&auto=format&fit=crop&q=80"
        ],
        "is_featured": True, "is_trending": True, "is_bestseller": True
    },
    {
        "category_slug": "electronics",
        "name": "Samsung 65-inch OLED 4K S95D Smart TV",
        "brand": "Samsung",
        "original_price": 289900,
        "discounted_price": 239900,
        "stock": 12,
        "rating": 4.8,
        "num_reviews": 110,
        "description": "OLED Glare Free technology with NQ4 AI Gen2 Processor, Panton validated color accuracy, Dolby Atmos 70W 4.2.2 channel audio, and 144Hz 4K gaming with FreeSync Premium Pro.",
        "specifications": {"Screen": "65-inch 4K OLED Anti-Glare 144Hz", "Processor": "NQ4 AI Gen2 Processor", "Audio": "70W 4.2.2CH Dolby Atmos", "Ports": "4x HDMI 2.1 48Gbps"},
        "sizes": ["55-inch", "65-inch", "77-inch"],
        "colors": ["Titan Black LaserSlim"],
        "images": [
            "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "electronics",
        "name": "DJI Mini 4 Pro 4K HDR Drone with RC2",
        "brand": "DJI",
        "original_price": 109990,
        "discounted_price": 89990,
        "stock": 20,
        "rating": 4.9,
        "num_reviews": 140,
        "description": "Ultra-lightweight under 249g folding drone with omnidirectional obstacle sensing, 4K/60fps HDR true vertical shooting, 20km FHD O4 video transmission, and 34-min flight time.",
        "specifications": {"Weight": "<249g (No registration needed)", "Camera": "4K/60fps HDR 1/1.3-inch CMOS", "Transmission": "DJI O4 20km Range", "Controller": "DJI RC 2 with 5.5-inch FHD Screen"},
        "sizes": ["Standard RC2", "Fly More Combo Plus"],
        "colors": ["DJI Classic Light Grey"],
        "images": [
            "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "electronics",
        "name": "Apple iPad Pro 11-inch M4 Ultra Retina XDR",
        "brand": "Apple",
        "original_price": 99900,
        "discounted_price": 92900,
        "stock": 30,
        "rating": 4.9,
        "num_reviews": 215,
        "description": "Outrageously thin at 5.3mm with groundbreaking Tandem OLED display, M4 chip with 38 TOPS NPU, Apple Pencil Pro haptic squeeze, and Thunderbolt connectivity.",
        "specifications": {"Display": "11-inch Ultra Retina Tandem OLED 1000 nits", "Chip": "Apple M4 9-core CPU", "Thickness": "5.3 mm", "Pencil Support": "Apple Pencil Pro"},
        "sizes": ["256GB", "512GB", "1TB"],
        "colors": ["Space Black", "Silver"],
        "images": [
            "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "electronics",
        "name": "Sony PlayStation 5 Slim Disc Edition",
        "brand": "Sony Interactive Entertainment",
        "original_price": 54990,
        "discounted_price": 49990,
        "stock": 40,
        "rating": 4.9,
        "num_reviews": 450,
        "description": "Experience lightning-fast loading with custom 1TB ultra-high speed SSD, deeper immersion with haptic feedback, adaptive triggers, and 3D Audio, and 4K-TV 120 fps gaming.",
        "specifications": {"Storage": "1TB Custom PCIe 4.0 NVMe SSD", "Drive": "Ultra HD Blu-ray Disc Drive", "Resolution": "Up to 4K 120Hz with HDR and VRR"},
        "sizes": ["1TB Disc Edition"],
        "colors": ["White Matte with Glossy Accents"],
        "images": [
            "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "electronics",
        "name": "MAHESH BABU (Hero)",
        "brand": "T-shirt",
        "original_price": 449920000,
        "discounted_price": 369200390,
        "stock": 1,
        "rating": 5,
        "num_reviews": 160000000,
        "description": "Ghattamaneni Mahesh Babu (born 9 August 1975) is an Indian actor, producer and philanthropist who works in Telugu cinema.",
        "specifications": {"Name": "Mahesh Babu", "Full Name": "Ghattamaneni Mahesh Babu","Date of Birth": "9 August 1975","Age": 51,"Profession": ["Actor", "Producer"],"Nationality": "Indian","Height": "6 ft 2 in (188 cm)","Spouse": "Namrata Shirodkar", "Children": 2,"Debut Film": "Raja Kumarudu (1999)","Languages": ["Telugu", "English"],},
        "sizes": ["Standard Box", "Creator Edition Kit"],
        "colors": ["Midnight Fleck Black"],
        "images": [
            "https://content.tupaki.com/twdata/2021/0721/news/Mahesh-Babu-Makes-A-Big-Sacrifice-For-Rajamouli-1627181227-181.jpg"
        ]
    },
    {
        "category_slug": "electronics",
        "name": "Anker 737 Power Bank 24,000mAh 140W",
        "brand": "Anker",
        "original_price": 14999,
        "discounted_price": 10999,
        "stock": 50,
        "rating": 4.8,
        "num_reviews": 230,
        "description": "GaNPrime two-way ultra-powerful 140W fast charging battery pack with vibrant smart digital display showing output wattage and battery health in real-time.",
        "specifications": {"Capacity": "24,000 mAh (86.4Wh)", "Max Output": "140W Single Port Power Delivery 3.1", "Screen": "Color Smart Digital Display"},
        "sizes": ["24000mAh"],
        "colors": ["Space Grey"],
        "images": [
            "https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "electronics",
        "name": "Sonos Era 300 Spatial Audio Smart Speaker",
        "brand": "Sonos",
        "original_price": 54999,
        "discounted_price": 44999,
        "stock": 22,
        "rating": 4.7,
        "num_reviews": 88,
        "description": "Revolutionary acoustic architecture featuring six drivers positioned all around to project sound from wall to wall and ceiling to floor with breakthrough Dolby Atmos spatial audio.",
        "specifications": {"Audio": "Dolby Atmos Spatial Audio with 6 drivers", "Connectivity": "Wi-Fi 6, Bluetooth 5.0, AirPlay 2", "Microphone": "Far-field microphone array with Trueplay"},
        "sizes": ["Single Speaker", "Stereo Pair"],
        "colors": ["Matte Black", "Matte White"],
        "images": [
            "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "electronics",
        "name": "Kindle Paperwhite Signature Edition 32GB",
        "brand": "Amazon",
        "original_price": 18999,
        "discounted_price": 14999,
        "stock": 45,
        "rating": 4.8,
        "num_reviews": 310,
        "description": "Glase-free 6.8-inch 300 ppi Paperwhite display with auto-adjusting warm light, Qi wireless charging, IPX8 waterproof design, and weeks of battery on one USB-C charge.",
        "specifications": {"Display": "6.8-inch 300 ppi Glare-Free E-Ink", "Storage": "32GB (Thousands of books)", "Charging": "Qi Wireless + USB-C", "Waterproof": "IPX8 (Submersion in fresh water)"},
        "sizes": ["32GB"],
        "colors": ["Agave Green", "Black", "Denim"],
        "images": [
            "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "electronics",
        "name": "Elgato Stream Deck MK.2 Production Console",
        "brand": "Elgato",
        "original_price": 16990,
        "discounted_price": 13490,
        "stock": 38,
        "rating": 4.8,
        "num_reviews": 195,
        "description": "15 customizable LCD keys to trigger unlimited studio actions. Instant tactile control over streaming, podcasting, coding shortcuts, lighting, and audio plugins.",
        "specifications": {"Keys": "15 Customizable Color LCD Keys", "Interface": "USB 2.0 with detachable angled stand", "Software": "Stream Deck App for Windows and Mac"},
        "sizes": ["15 Keys"],
        "colors": ["Obsidian Black", "White"],
        "images": [
            "https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=800&auto=format&fit=crop&q=80"
        ]
    },

    # 8. Headphones (10 products)
    {
        "category_slug": "headphones",
        "name": "Sony WH-1000XM5 Wireless Noise Cancelling",
        "brand": "Sony",
        "original_price": 34990,
        "discounted_price": 26990,
        "stock": 35,
        "rating": 4.8,
        "num_reviews": 410,
        "description": "Industry-leading noise cancellation powered by two processors and eight microphones. Features Auto NC Optimizer, crystal-clear hands-free calling with 4 beamforming mics, and 30-hour battery.",
        "specifications": {"Driver": "Specially engineered 30mm carbon driver", "Codecs": "LDAC, AAC, SBC", "Battery Life": "30 Hours with ANC on", "Weight": "250g ultra-comfortable fit"},
        "sizes": ["Standard Over-Ear"],
        "colors": ["Silver Champagne", "Midnight Blue", "Matte Black"],
        "images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&auto=format&fit=crop&q=80"
        ],
        "is_featured": True, "is_trending": True, "is_bestseller": True
    },
    {
        "category_slug": "headphones",
        "name": "Apple AirPods Max with Smart Case",
        "brand": "Apple",
        "original_price": 59900,
        "discounted_price": 52900,
        "stock": 20,
        "rating": 4.7,
        "num_reviews": 280,
        "description": "Custom acoustic design with knit-mesh canopy and anodized aluminum ear cups. Computational audio with H1 chips, high-fidelity sound, Active Noise Cancellation with Transparency mode.",
        "specifications": {"Audio": "Apple-designed dynamic driver with dual neodymium magnets", "Sensors": "Optical, position, case-detect, accelerometer, gyroscope", "Connectivity": "Bluetooth 5.0 with automatic device switching"},
        "sizes": ["Over-Ear"],
        "colors": ["Space Grey", "Silver", "Sky Blue", "Pink", "Green"],
        "images": [
            "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "headphones",
        "name": "Bose QuietComfort Ultra Spatial Headphones",
        "brand": "Bose",
        "original_price": 37900,
        "discounted_price": 31900,
        "stock": 25,
        "rating": 4.8,
        "num_reviews": 195,
        "description": "World-class noise cancellation quieter than ever before. Breakthrough Bose Immersive Audio brings content out of your head and onto the virtual stage in front of you.",
        "specifications": {"Audio": "Bose Immersive Audio Spatial Tech", "Battery": "Up to 24 hours (18 with Immersive)", "Comfort": "Luxurious protein leather ear cushions"},
        "sizes": ["Over-Ear"],
        "colors": ["Black", "White Smoke", "Sandstone Gold"],
        "images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "headphones",
        "name": "Apple AirPods Pro (2nd Gen) with USB-C MagSafe",
        "brand": "Apple",
        "original_price": 24900,
        "discounted_price": 21900,
        "stock": 60,
        "rating": 4.9,
        "num_reviews": 560,
        "description": "Powered by Apple H2 headphone chip for up to 2x more Active Noise Cancellation, Adaptive Audio that tailors noise control to your environment, and Personalized Spatial Audio.",
        "specifications": {"Processor": "Apple H2 Headphone Chip", "Water Resistance": "IP54 dust, sweat, and water resistant", "Charging": "USB-C MagSafe Case with Precision Finding speaker"},
        "sizes": ["In-Ear (XS, S, M, L tips included)"],
        "colors": ["Glossy White"],
        "images": [
            "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "headphones",
        "name": "Sennheiser Momentum 4 Wireless Audiophile",
        "brand": "Sennheiser",
        "original_price": 34990,
        "discounted_price": 24990,
        "stock": 28,
        "rating": 4.7,
        "num_reviews": 160,
        "description": "Signature Sennheiser sound powered by 42mm audiophile-inspired transducer system. Unprecedented 60-hour marathon battery life and aptX Adaptive high-res audio codec.",
        "specifications": {"Driver": "42mm Dynamic Audiophile Transducers", "Battery": "Massive 60-Hour Battery Life", "Codecs": "aptX Adaptive, AAC, SBC"},
        "sizes": ["Over-Ear"],
        "colors": ["Black with Copper Accents", "White with Grey Tweed"],
        "images": [
            "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "headphones",
        "name": "Marshall Major IV Wireless On-Ear Bluetooth",
        "brand": "Marshall",
        "original_price": 14999,
        "discounted_price": 11499,
        "stock": 35,
        "rating": 4.6,
        "num_reviews": 210,
        "description": "Iconic rock 'n' roll textured vinyl design delivering roaring bass, smooth mids, and brilliant treble. Features 80+ solid hours of wireless playtime and wireless charging.",
        "specifications": {"Playtime": "80+ Hours Wireless Playtime", "Charging": "Qi Wireless Charging + Quick USB-C (15 min = 15 hrs)", "Knob": "Multi-Directional Control Knob"},
        "sizes": ["On-Ear Folding"],
        "colors": ["Vintage Black", "Classic Brown"],
        "images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "headphones",
        "name": "JBL Tour ONE M2 Adaptive ANC Headphones",
        "brand": "JBL",
        "original_price": 24999,
        "discounted_price": 17999,
        "stock": 30,
        "rating": 4.5,
        "num_reviews": 130,
        "description": "True Adaptive Noise Cancelling technology with 40mm dynamic drivers tuned to JBL Pro Sound, Smart Ambient talk-thru, and 4-mic superior voice call clarity.",
        "specifications": {"Sound": "Hi-Res Audio Certified JBL Pro Sound", "Battery": "Up to 50 hours playtime", "Features": "Personi-Fi 2.0 hearing profile customizer"},
        "sizes": ["Over-Ear"],
        "colors": ["Champagne Gold", "Black"],
        "images": [
            "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "headphones",
        "name": "Beats Studio Pro Premium Wireless Spatial",
        "brand": "Beats",
        "original_price": 37900,
        "discounted_price": 27900,
        "stock": 25,
        "rating": 4.5,
        "num_reviews": 145,
        "description": "Custom acoustic platform with lossless USB-C audio, three distinct built-in sound profiles, fully adaptive active noise cancelling, and one-touch Apple/Android pairing.",
        "specifications": {"Audio": "Lossless Audio via USB-C + Spatial Audio", "Battery": "Up to 40 hours battery life", "Fast Fuel": "10-minute charge gives 4 hours of playback"},
        "sizes": ["Over-Ear"],
        "colors": ["Deep Brown", "Navy", "Sandstone", "Matte Black"],
        "images": [
            "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "headphones",
        "name": "Audio-Technica ATH-M50xBT2 Studio Monitor",
        "brand": "Audio-Technica",
        "original_price": 21990,
        "discounted_price": 16490,
        "stock": 22,
        "rating": 4.8,
        "num_reviews": 310,
        "description": "Critically acclaimed M50x studio monitor sonic performance packed with wireless Bluetooth 5.0, AK4331 advanced audio DAC, and low latency mode for video gaming.",
        "specifications": {"Drivers": "Proprietary 45mm large-aperture drivers", "DAC": "Dedicated AK4331 audio DAC with internal headphone amp", "Battery": "Up to 50 hours continuous use"},
        "sizes": ["Over-Ear Studio"],
        "colors": ["Classic Studio Black", "Deep Blue Limited"],
        "images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "headphones",
        "name": "Nothing Ear (a) High-Res Wireless Earbuds",
        "brand": "Nothing",
        "original_price": 9999,
        "discounted_price": 6999,
        "stock": 55,
        "rating": 4.6,
        "num_reviews": 240,
        "description": "Striking transparent bubble design with punchy bass boost algorithm, up to 45dB Smart Active Noise Cancellation, Hi-Res LDAC audio certification, and ChatGPT integration.",
        "specifications": {"ANC": "Smart Active Noise Cancellation up to 45 dB", "Codec": "LDAC High-Resolution Audio", "Playtime": "Up to 42.5 hours with charging case"},
        "sizes": ["In-Ear (S, M, L)"],
        "colors": ["Vibrant Yellow", "Clean White", "Black"],
        "images": [
            "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=80"
        ]
    },

    # 9. Watches (10 products)
    {
        "category_slug": "watches",
        "name": "Apple Watch Ultra 2 GPS + Cellular 49mm",
        "brand": "Apple",
        "original_price": 89900,
        "discounted_price": 84900,
        "stock": 20,
        "rating": 4.9,
        "num_reviews": 210,
        "description": "The ultimate sports and adventure watch. 49mm corrosion-resistant aerospace titanium case, 3000-nit Always-On display, precision dual-frequency GPS, 100m water resistance, and dive computer certification.",
        "specifications": {"Case": "49mm Grade 5 Titanium", "Display": "Sapphire Crystal 3000 nits OLED", "Water Resistance": "100m / EN13319 scuba certified", "Battery": "Up to 72 hours in low power mode"},
        "sizes": ["49mm (S/M, M/L Loop)"],
        "colors": ["Titanium Natural", "Black Titanium"],
        "images": [
            "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800&auto=format&fit=crop&q=80"
        ],
        "is_featured": True, "is_trending": True, "is_bestseller": True
    },
    {
        "category_slug": "watches",
        "name": "Samsung Galaxy Watch Ultra 47mm LTE",
        "brand": "Samsung",
        "original_price": 59999,
        "discounted_price": 53999,
        "stock": 24,
        "rating": 4.7,
        "num_reviews": 130,
        "description": "Cushion design titanium smartwatch designed for extreme altitudes and ocean swimming. Features BioActive Sensor with FDA-cleared sleep apnea detection and multi-sport quick button.",
        "specifications": {"Body": "Grade 4 Titanium with 10ATM & IP68 resistance", "Screen": "1.5-inch Super AMOLED 3000 nits", "Processor": "3nm Exynos W1000 5-core"},
        "sizes": ["47mm"],
        "colors": ["Titanium Gray", "Titanium White", "Titanium Silver"],
        "images": [
            "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "watches",
        "name": "Fossil Heritage Automatic Stainless Steel Watch",
        "brand": "Fossil",
        "original_price": 24995,
        "discounted_price": 17495,
        "stock": 28,
        "rating": 4.6,
        "num_reviews": 98,
        "description": "Celebrating classic horological craftsmanship with a see-through exhibition caseback showcasing the intricate Japanese automatic self-winding movement. Elegant 3-link solid steel bracelet.",
        "specifications": {"Movement": "Automatic 21-Jewel Self-Winding", "Case Size": "43mm 316L Stainless Steel", "Dial": "Sunray Black with Exhibition Caseback"},
        "sizes": ["43mm Case"],
        "colors": ["Silver/Black Dial", "Two-Tone Gold/Silver"],
        "images": [
            "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "watches",
        "name": "Seiko 5 Sports Automatic Diver Style Watch",
        "brand": "Seiko",
        "original_price": 28500,
        "discounted_price": 22800,
        "stock": 30,
        "rating": 4.8,
        "num_reviews": 175,
        "description": "Legendary Japanese mechanical durability. Caliber 4R36 automatic movement with manual winding capability, unidirectional rotating bezel, day/date display, and 100m water resistance.",
        "specifications": {"Caliber": "Seiko 4R36 Mechanical (41hr reserve)", "Crystal": "Hardlex Mineral Crystal", "Lume": "LumiBrite hands and markers"},
        "sizes": ["42.5mm"],
        "colors": ["Pepsi Bezel (Blue/Red)", "Submariner Black"],
        "images": [
            "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "watches",
        "name": "Tissot PRX Powermatic 80 Swiss Automatic",
        "brand": "Tissot",
        "original_price": 68500,
        "discounted_price": 61650,
        "stock": 15,
        "rating": 4.9,
        "num_reviews": 140,
        "description": "1978 retro luxury revival with integrated brushed stainless steel bracelet, waffle tapisserie dial, and groundbreaking Swiss Powermatic 80 caliber boasting 80-hour power reserve.",
        "specifications": {"Movement": "Swiss Powermatic 80 with Nivachron balance spring", "Case": "40mm Tonneau Shaped 316L Steel", "Glass": "Anti-reflective Scratch-resistant Sapphire"},
        "sizes": ["35mm", "40mm"],
        "colors": ["Ice Blue Waffle", "Navy Blue", "Emerald Green"],
        "images": [
            "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "watches",
        "name": "Casio G-Shock GA-2100 'CasiOak' Octagonal",
        "brand": "Casio",
        "original_price": 9995,
        "discounted_price": 7995,
        "stock": 50,
        "rating": 4.8,
        "num_reviews": 380,
        "description": "Iconic octagonal bezel design reinforced with Carbon Core Guard structure. Super shock-resistant, 200m water resistant, double LED light, and ultra-slim 11.8mm profile.",
        "specifications": {"Structure": "Carbon Core Guard Module 5611", "Water Resistance": "200 meters / 20 Bar", "Battery": "3 years on SR726W"},
        "sizes": ["45.4mm"],
        "colors": ["All Black Stealth", "Navy Blue", "Army Green"],
        "images": [
            "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "watches",
        "name": "Garmin Fenix 7 Pro Solar Multisport GPS",
        "brand": "Garmin",
        "original_price": 94990,
        "discounted_price": 82990,
        "stock": 14,
        "rating": 4.8,
        "num_reviews": 85,
        "description": "Power Glass solar charging lens that harnesses the sun's energy to extend battery up to 37 days. Built-in LED flashlight, topographic TopoActive maps, and endurance metrics.",
        "specifications": {"Glass": "Power Sapphire Solar Charging", "Bezel": "Titanium with DLC coating", "Flashlight": "Multi-LED white and red safety light"},
        "sizes": ["47mm"],
        "colors": ["Carbon Gray DLC Titanium", "Fog Gray"],
        "images": [
            "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "watches",
        "name": "Tommy Hilfiger Bank Multifunction Watch",
        "brand": "Tommy Hilfiger",
        "original_price": 14500,
        "discounted_price": 9995,
        "stock": 35,
        "rating": 4.4,
        "num_reviews": 112,
        "description": "American preppy statement timepiece with 44mm ion-plated case, sunray multi-eye subdials tracking day, date, and 24-hour time, paired with supple genuine leather strap.",
        "specifications": {"Case": "44mm Stainless Steel IP Gray", "Strap": "Brown Italian Calfskin Leather", "Subdials": "Day, Date, 24-Hour Military Time"},
        "sizes": ["44mm"],
        "colors": ["Navy Dial / Brown Leather", "Black Dial / Black Leather"],
        "images": [
            "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "watches",
        "name": "Citizen Eco-Drive Promaster Diver 200M",
        "brand": "Citizen",
        "original_price": 31900,
        "discounted_price": 25500,
        "stock": 26,
        "rating": 4.7,
        "num_reviews": 135,
        "description": "Powered by any natural or artificial light with proprietary Eco-Drive technology — never needs a battery change. Certified ISO compliant for scuba diving to 200 meters.",
        "specifications": {"Technology": "Eco-Drive Light Powered (6-month reserve)", "Certification": "ISO 6425 Divers Standard 200M", "Bezel": "Aluminum 60-minute elapsed time bezel"},
        "sizes": ["44mm"],
        "colors": ["Royal Blue Dial", "Classic Diver Black"],
        "images": [
            "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "watches",
        "name": "Titan Edge Ceramic Ultra Slim Watch",
        "brand": "Titan",
        "original_price": 26995,
        "discounted_price": 21995,
        "stock": 20,
        "rating": 4.6,
        "num_reviews": 72,
        "description": "One of the slimmest ceramic watches in the world at just 4.4mm thin. Hypoallergenic high-tech ceramic case and scratch-resistant sapphire crystal glass.",
        "specifications": {"Thickness": "Ultra-thin 4.4 mm Profile", "Material": "High-Tech High-Gloss Ceramic", "Movement": "In-house Titan Edge 1.15mm Slim Quartz"},
        "sizes": ["Slim 40mm"],
        "colors": ["Midnight Anthracite", "Pristine White Ceramic"],
        "images": [
            "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop&q=80"
        ]
    },

    # 10. Shoes (10 products)
    {
        "category_slug": "shoes",
        "name": "Nike Air Jordan 1 Retro High OG Chicago",
        "brand": "Nike",
        "original_price": 18995,
        "discounted_price": 14995,
        "stock": 20,
        "rating": 4.9,
        "num_reviews": 510,
        "description": "The sneaker that started a global culture. Premium full-grain leather construction in the legendary Chicago red, white, and black colorway with encapsulated Air-Sole cushioning in heel.",
        "specifications": {"Material": "100% Genuine Full-Grain Leather", "Sole": "Durable solid rubber cupsole with pivot circle", "Branding": "Embossed Wings logo on collar"},
        "sizes": ["UK 7", "UK 8", "UK 9", "UK 10", "UK 11"],
        "colors": ["Varsity Red / White / Black"],
        "images": [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1552346154-21d32810aba3?w=800&auto=format&fit=crop&q=80"
        ],
        "is_featured": True, "is_trending": True, "is_bestseller": True
    },
    {
        "category_slug": "shoes",
        "name": "Adidas Ultraboost Light Running Shoes",
        "brand": "Adidas",
        "original_price": 19999,
        "discounted_price": 13999,
        "stock": 35,
        "rating": 4.8,
        "num_reviews": 320,
        "description": "Experience epic energy return with Light BOOST cushioning — 30% lighter BOOST material with primeknit+ upper that hugs your foot with adaptive supportive fit.",
        "specifications": {"Midsole": "Light BOOST with Linear Energy Push", "Outsole": "Continental Better Rubber", "Drop": "10mm (Heel: 30mm / Forefoot: 20mm)"},
        "sizes": ["UK 6", "UK 7", "UK 8", "UK 9", "UK 10", "UK 11"],
        "colors": ["Core Black", "Cloud White", "Solar Red"],
        "images": [
            "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "shoes",
        "name": "New Balance 9060 Chunky Lifestyle Sneaker",
        "brand": "New Balance",
        "original_price": 15999,
        "discounted_price": 12799,
        "stock": 25,
        "rating": 4.8,
        "num_reviews": 185,
        "description": "Futuristic retro-futurism aesthetic drawing inspiration from the iconic 99X series. Dual-density midsole featuring ABZORB and SBS cushioning with diamond outsole pattern.",
        "specifications": {"Upper": "Pigskin Suede and Breathable Mesh", "Cushioning": "ABZORB and SBS Cushioning", "Design": "Y2K Aesthetic Sculpted Midsole"},
        "sizes": ["UK 7", "UK 8", "UK 9", "UK 10"],
        "colors": ["Rain Cloud Grey", "Sea Salt White", "Triple Black"],
        "images": [
            "https://images.unsplash.com/photo-1539185441755-769473a23570?w=800&auto=format&fit=crop&q=80"
        ],
        "is_trending": True
    },
    {
        "category_slug": "shoes",
        "name": "Nike Air Force 1 '07 Triple White",
        "brand": "Nike",
        "original_price": 9695,
        "discounted_price": 8295,
        "stock": 60,
        "rating": 4.9,
        "num_reviews": 680,
        "description": "The legend lives on in the low-cut classic icon. Crisp pristine stitched leather overlays, perforated toe box ventilation, and lightweight Nike Air cushioning.",
        "specifications": {"Profile": "Low-Cut Padded Collar", "Midsole": "Foam Midsole with Nike Air", "Perforations": "Toe Box Perforations"},
        "sizes": ["UK 6", "UK 7", "UK 8", "UK 9", "UK 10", "UK 11"],
        "colors": ["Triple White", "Triple Black"],
        "images": [
            "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "shoes",
        "name": "Puma Suede Classic XXI Low Top Kicks",
        "brand": "Puma",
        "original_price": 6999,
        "discounted_price": 4499,
        "stock": 40,
        "rating": 4.5,
        "num_reviews": 160,
        "description": "Since 1968, the Suede has been worn by icons of every generation. Premium velvety suede upper with full lace closure, synthetic lining, and grippy rubber outsole.",
        "specifications": {"Upper": "100% Genuine Silky Suede", "Branding": "Gold foil Puma Suede callout", "Insole": "Comfort sockliner for instant step-in"},
        "sizes": ["UK 7", "UK 8", "UK 9", "UK 10"],
        "colors": ["Peacoat Navy", "Black / White Formstrip", "Burgundy Red"],
        "images": [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "shoes",
        "name": "Clarks Originals Desert Boot Beeswax Leather",
        "brand": "Clarks",
        "original_price": 14999,
        "discounted_price": 10999,
        "stock": 20,
        "rating": 4.7,
        "num_reviews": 140,
        "description": "Nathan Clark's 1950 design inspired by crepe-soled boots from Cairo. Made from rich beeswax pull-up leather that distresses handsomely with age on natural plantation crepe rubber soles.",
        "specifications": {"Upper": "Beeswax Pull-Up Leather", "Sole": "Sustainable FSC Natural Plantation Crepe", "Laces": "Clean Two-Eyelet Lacing"},
        "sizes": ["UK 7", "UK 8", "UK 9", "UK 10"],
        "colors": ["Beeswax Brown", "Sand Suede"],
        "images": [
            "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "shoes",
        "name": "Vans Old Skool Core Skate Shoes",
        "brand": "Vans",
        "original_price": 5499,
        "discounted_price": 3849,
        "stock": 50,
        "rating": 4.7,
        "num_reviews": 420,
        "description": "The first skate shoe to bare the iconic side jazz stripe. Sturdy canvas and suede uppers, re-enforced toe caps, supported padded collars, and signature rubber waffle outsoles.",
        "specifications": {"Upper": "Suede and Heavy Canvas", "Outsole": "Vulcanized Signature Waffle Rubber", "Collar": "Padded Supportive Ankle Collar"},
        "sizes": ["UK 6", "UK 7", "UK 8", "UK 9", "UK 10", "UK 11"],
        "colors": ["Black / White", "Checkerboard", "Navy"],
        "images": [
            "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=800&auto=format&fit=crop&q=80"
        ],
        "is_bestseller": True
    },
    {
        "category_slug": "shoes",
        "name": "Converse Chuck Taylor All Star 70 High Top",
        "brand": "Converse",
        "original_price": 6499,
        "discounted_price": 4799,
        "stock": 45,
        "rating": 4.8,
        "num_reviews": 390,
        "description": "Built off the original 1970s basketball design with heavier 12oz duck canvas, vintage archival star ankle patch, varnished egret foxing tape, and cushioned OrthoLite insole.",
        "specifications": {"Canvas": "Premium 12oz Heavy Canvas", "Insole": "OrthoLite Cushioning with Arch Support", "Foxing": "Glossy Egret Rubber Sidewall"},
        "sizes": ["UK 6", "UK 7", "UK 8", "UK 9", "UK 10"],
        "colors": ["Parchment Off-White", "Classic Black", "Sunflower Yellow"],
        "images": [
            "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "shoes",
        "name": "Asics Gel-Kayano 31 Stability Running Shoes",
        "brand": "Asics",
        "original_price": 16999,
        "discounted_price": 13599,
        "stock": 25,
        "rating": 4.8,
        "num_reviews": 115,
        "description": "Advanced stability road running with 4D GUIDANCE SYSTEM that adapts to your stride, PureGEL rearfoot cushioning, and lightweight FF BLAST PLUS ECO foam.",
        "specifications": {"Stability": "4D Guidance Adaptive System", "Cushion": "PureGEL technology 65% softer than standard gel", "Drop": "10mm Heel Drop"},
        "sizes": ["UK 7", "UK 8", "UK 9", "UK 10", "UK 11"],
        "colors": ["French Blue / Electric Lime", "Triple Black"],
        "images": [
            "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&auto=format&fit=crop&q=80"
        ]
    },
    {
        "category_slug": "shoes",
        "name": "Woodland Rugged Oiled Leather Trekking Boots",
        "brand": "Woodland",
        "original_price": 7995,
        "discounted_price": 5595,
        "stock": 35,
        "rating": 4.6,
        "num_reviews": 230,
        "description": "Engineered for rough outdoor wilderness expeditions and city grit. Premium oiled nubuck leather, rust-proof brass hardware eyelets, and grooved traction lug rubber outsole.",
        "specifications": {"Upper": "Oiled Water-Resistant Nubuck Leather", "Outsole": "Deep-cleated anti-slip rubber lug sole", "Collar": "Soft padded leather collar"},
        "sizes": ["UK 7", "UK 8", "UK 9", "UK 10"],
        "colors": ["Khaki Camel", "Forest Olive", "Dark Tan Brown"],
        "images": [
            "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&auto=format&fit=crop&q=80"
        ]
    }
]

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from seed.seed_data import seed_database
    seed_database()
