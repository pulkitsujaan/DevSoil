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
        return "Alluvial Soil"
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
        "N_NO3 ppm": ["Urea", "Ammonium Nitrate", "Compost", "Blood Meal", "Fish Emulsion"],
        "P ppm": ["Single Super Phosphate (SSP)", "Di-Ammonium Phosphate (DAP)", "Bone Meal", "Rock Phosphate", "Poultry Manure"],
        "K ppm": ["Muriate of Potash (MOP)", "Sulfate of Potash (SOP)", "Wood Ash", "K-Mag", "Compost Tea"],
        "Zn ppm": ["Zinc Sulfate", "Chelated Zinc", "Zinc Oxide", "Organic Zinc Foliar Sprays", "Zinc-Enriched Compost"],
        "O.M. %": ["Compost", "Manure", "Peat Moss", "Cover Crops", "Biofertilizers"]
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

if __name__ == "__main__":
    file_path = "dataset/fertilizer/data.xlsx"  # Update with actual file path
    df = load_data(file_path)
    df_filtered = process_soil_data(df)
    
    soil_type_input = input("Enter soil type (Alluvial, Black Soil, Clay Soil, Red Soil): ")
    soil_info = get_soil_info(df_filtered, soil_type_input)
    print(soil_info)
