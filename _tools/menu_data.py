# Boston Shawarma menu — transcribed from the Grabull Direct ordering page (Newton, Sept 2026),
# with spelling cleaned up. Each item: (name, price, description, tags)
WRAP_NOTE = ("Wrapped in pita baked fresh daily with lettuce, tomatoes, onion, pickles "
             "and tahini sauce or garlic spread.")
PLATE_NOTE = ("Every plate comes with pita bread, rice, hummus, salad and fries, topped with "
              "sesame tahini or our spicy homemade sauce.")

MENU = [
    ("sandwiches", "Sandwiches", [
        ("Meat Sandwiches", None, [
            ("Chicken Shawarma", "14.49", "Slow-roasted, thinly sliced chicken breast, lightly seasoned.", []),
            ("Beef Shawarma", "14.49", "Slow-roasted, thinly sliced lean beef, lightly seasoned.", ["fav"]),
            ("Lamb Shawarma", "14.49", "Slow-roasted, thinly sliced lamb, lightly seasoned.", []),
            ("Chicken Kebab", "14.49", "Marinated chicken breast grilled over an open burner, delicately spiced.", []),
            ("Kafta Kebab", "14.49", "Ground lean beef with Mediterranean spices, minced onion and parsley, grilled over an open burner.", []),
            ("Shish Kebab", "14.99", "Grilled tender lamb cubes seasoned with Mediterranean spices.", []),
            ("Kibby", "14.49", "Baked, finely ground beef or lamb with cracked wheat, onion, basil, spices and sautéed pine nuts.", []),
            ("Soujok", "14.49", "Hot and spicy marinated ground lamb or beef, served sizzling off the grill.", ["spicy"]),
        ]),
        ("House Special Wraps", WRAP_NOTE, [
            ("Chicken Garlic Mayo", "15.49", "", []),
            ("Lamb & Chicken Mix", "15.49", "", []),
            ("Shawarma & Fresh Avocado", "15.49", "", []),
            ("Shawarma, Cheese & Fries", "15.49", "", []),
            ("Shawarma & Falafel", "15.49", "", []),
            ("Shawarma & Fries", "15.49", "", []),
            ("Shawarma & Rice", "15.49", "", []),
        ]),
    ]),
    ("veggie", "Veggie Sandwiches", [
        ("Classics", None, [
            ("Falafel", "13.99", "Fava beans and chickpeas with parsley, onion, coriander, pepper and cumin, lightly fried.", ["fav"]),
            ("Hummus", "13.99", "Chickpeas blended with tahini, lemon juice, garlic and cumin.", []),
            ("Babaghanoush", "13.99", "Smoked eggplant blended with garlic, tahini and lemon juice.", []),
            ("Stuffed Grape Leaves", "13.99", "Tender baby grape leaves stuffed with seasoned rice, slow-cooked in lemon juice.", []),
            ("Taboule", "13.99", "Finely chopped parsley, diced tomatoes, scallion and cracked wheat with lemon and olive oil.", []),
            ("Hallumi Cheese", "13.99", "Sheep and goat's milk cheese with cucumber, black olives, mint and spices.", []),
            ("Vegetarian Kibby", "13.99", "A baked mix of pumpkin, cracked wheat, sautéed pine nuts, chickpeas and onion.", []),
        ]),
        ("House Special Wraps", WRAP_NOTE, [
            ("Falafel, Hummus & Fries", "14.49", "", ["fav"]),
            ("Falafel, Hummus & Grape Leaves", "14.49", "", []),
            ("Falafel, Hummus, Bean & Rice", "14.49", "", []),
            ("Falafel, Hummus & Cheese Fries", "13.49", "", []),
            ("Falafel, Hummus & Fresh Avocado", "13.49", "", []),
        ]),
    ]),
    ("plates", "Dinner Plates", [
        ("Meat Dinner Plates", PLATE_NOTE, [
            ("Shawarma", "21.49", "", ["fav"]),
            ("Mix It", "21.99", "Lamb and chicken shawarma.", ["fav"]),
            ("Go Combo Shawarma", "25.99", "Lamb, chicken and kafta.", []),
            ("Chicken Kebab", "23.99", "", []),
            ("Shish Kebab", "23.99", "", []),
            ("Kafta Kebab", "21.99", "", []),
            ("Mix Kebab", "25.99", "Lamb, chicken and kafta kebab.", []),
            ("Kibby", "20.49", "", []),
            ("Soujok", "21.99", "", ["spicy"]),
        ]),
    ]),
    ("veg-plates", "Veggie Plates", [
        ("Vegetarian Dinner Plates", PLATE_NOTE, [
            ("Falafel", "18.49", "", []),
            ("Falafel & Fresh Avocado", "19.49", "", []),
            ("Grape Leaves", "18.49", "", []),
            ("Vegetarian Kibby", "18.49", "", []),
            ("Combo Plate", "18.49", "Falafel and grape leaves.", []),
        ]),
    ]),
    ("salads", "Salads", [
        ("Fresh Salads", None, [
            ("Fattoush Salad", "9.49", "A zesty mix of chopped parsley, tomatoes, green peppers and toasted pita with olive oil and savory spices.", ["veg"]),
            ("Falafel Salad", "16.49", "Falafel served with taboule and hummus.", ["veg"]),
            ("Middle Eastern Salad", "15.49", "Stuffed grape leaves, taboule, tomatoes, lettuce, carrots, peppers, black olives, cucumber and feta with tahini dressing.", ["veg", "fav"]),
            ("Shawarma Salad", "18.49", "Fattoush topped with your choice of lamb, chicken or beef shawarma.", []),
        ]),
    ]),
    ("pies-sides", "Pies & Sides", [
        ("Homemade Pies", None, [
            ("Spinach Pie", "4.99", "", ["veg", "fav"]),
            ("Spinach & Feta Pie", "4.00", "", ["veg"]),
            ("Chicken Pie", "4.00", "", []),
            ("Manaish Bil Zaatar", "4.00", "Flatbread with za'atar (Middle Eastern oregano and sesame) and olive oil.", ["veg"]),
            ("Hallumi & Mozzarella Cheese Bread", "4.49", "", ["veg"]),
        ]),
        ("Sides", None, [
            ("Hummus", "5.99", "", []),
            ("Taboule", "6.49", "", []),
            ("Falafel (2 pc)", "4.49", "", []),
            ("Grape Leaves (2 pc)", "4.49", "", []),
            ("French Fries", "4.49", "", []),
            ("Rice", "3.99", "", []),
        ]),
    ]),
    ("drinks", "Drinks & Dessert", [
        ("Drinks", None, [
            ("Mediterranean Yogurt Drink", "3.99", "A bottle of refreshing, lightly salty yogurt drink.", []),
            ("Vimto", "2.50", "", []),
            ("Canned Soda", "1.99", "", []),
            ("Poland Spring Water", "1.50", "", []),
        ]),
        ("Dessert", None, [
            ("Honey Walnut Baklava", "4.49", "Flaky layers of phyllo, walnuts and honey syrup.", ["fav"]),
        ]),
    ]),
]
