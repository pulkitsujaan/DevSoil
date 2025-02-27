import pandas as pd
import random

def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name="SOIL DATA")
    df.columns = df.columns.str.strip()
    return df

def classify_soil(row):
    sand, clay, silt, om, caco3, fe = row["Sand %"], row["Clay %"], row["Silt %"], row["O.M. %"], row["CACO3 %"], row["Fe ppm"]
    
    if sand > 40 and silt >= 30:
        return "Alluvial"
    elif clay > 30 and caco3 > 2:
        return "Black Soil"
    elif clay > 35 and sand < 40:
        return "Clay Soil"
    elif 20 <= clay <= 40 and fe > 20 and om < 1:
        return "Red Soil"
    else:
        return None

def process_soil_data(df):
    df["Soil Type"] = df.apply(classify_soil, axis=1)
    df_filtered = df.dropna(subset=["Soil Type"])
    
    ideal_ranges = {
        "N_NO3 ppm": (11, 15),
        "P ppm": (15, 25),
        "K ppm": (150, 200),
        "Zn ppm": (1.8, 3.5),
        "O.M. %": (2, 5)
    }
    
    def compare_to_ideal(value, ideal_range):
        if value < ideal_range[0]:
            return "Below Ideal"
        elif value > ideal_range[1]:
            return "Above Ideal"
        else:
            return "Within Ideal"
    
    for nutrient, ideal_range in ideal_ranges.items():
        df_filtered[f"{nutrient} Status"] = df_filtered[nutrient].apply(lambda x: compare_to_ideal(x, ideal_range))
    
    def is_outlier(row):
        if row["Soil Type"] == "Red Soil":
            return False
        statuses = [row[f"{nutrient} Status"] for nutrient in ideal_ranges]
        return statuses.count("Below Ideal") >= 4 or statuses.count("Above Ideal") >= 4
    
    df_filtered = df_filtered[~df_filtered.apply(is_outlier, axis=1)]
    return df_filtered

def suggest_fertilizers(row):
    fertilizers = {
        "N_NO3 ppm": ["Urea - Provides nitrogen essential for leafy growth", "Ammonium Nitrate - Quickly available nitrogen source", "Compost - Organic nitrogen boost", "Blood Meal - High nitrogen content", "Fish Emulsion - Natural nitrogen fertilizer"],
        "P ppm": ["Single Super Phosphate (SSP) - Boosts root development", "Di-Ammonium Phosphate (DAP) - Provides phosphorus and nitrogen", "Bone Meal - Slow-release phosphorus", "Rock Phosphate - Long-lasting phosphorus source", "Poultry Manure - Organic phosphorus source"],
        "K ppm": ["Muriate of Potash (MOP) - Increases plant vigor", "Sulfate of Potash (SOP) - Improves disease resistance", "Wood Ash - Provides potassium naturally", "K-Mag - Contains potassium and magnesium", "Compost Tea - Organic potassium supplement"],
        "Zn ppm": ["Zinc Sulfate - Corrects zinc deficiency", "Chelated Zinc - Easily absorbed zinc source", "Zinc Oxide - Improves plant enzyme function", "Organic Zinc Foliar Sprays - Fast-acting zinc supplementation", "Zinc-Enriched Compost - Provides slow-release zinc"],
        "O.M. %": ["Compost - Improves soil structure and moisture retention", "Manure - Boosts organic matter and nutrients", "Peat Moss - Enhances soil aeration", "Cover Crops - Increases soil fertility", "Biofertilizers - Enhances microbial activity"]
    }
    deficiency = {}
    for nutrient, status in zip(fertilizers.keys(), [row[f"{nutrient} Status"] for nutrient in fertilizers]):
        if status == "Below Ideal":
            deficiency[nutrient] = fertilizers[nutrient]
    return deficiency

def get_soil_info(df_filtered, soil_type):
    subset = df_filtered[df_filtered["Soil Type"] == soil_type]
    if subset.empty:
        return {"message": f"No data available for {soil_type}"}
    
    sample = subset.sample(n=1).iloc[0]
    deficiency = suggest_fertilizers(sample)
    return {
        "Sand %": float(sample["Sand %"]),
        "Clay %": float(sample["Clay %"]),
        "Silt %": float(sample["Silt %"]),
        "Fertilizer Recommendations": deficiency
    }