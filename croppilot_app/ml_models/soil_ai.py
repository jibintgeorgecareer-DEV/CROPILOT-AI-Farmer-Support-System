def predict_soil_ai(crop, weather):

    crop = crop.lower()
    weather = weather.lower()
    
    rules = {

        ("rice", "rainy"): {
            "soil": "Clay Soil",
            "ph": "5.5 - 6.5",
            "reason": "Retains water well for paddy farming."
        },

        ("tomato", "sunny"): {
            "soil": "Loamy Soil",
            "ph": "6.0 - 6.8",
            "reason": "Good drainage and rich nutrients."
        },

        ("potato", "cold"): {
            "soil": "Sandy Loam Soil",
            "ph": "5.0 - 6.5",
            "reason": "Loose soil helps tuber growth."
        },

        ("banana", "humid"): {
            "soil": "Alluvial Soil",
            "ph": "6.0 - 7.5",
            "reason": "High fertility and moisture retention."
        }

    }

    result = rules.get((crop, weather))
    print("soil RESULT:",result)

    if result:
        return result

    return {
        "soil": "No Recommendation Available",
        "ph": "Nill",
        "reason": "Nill"
    }