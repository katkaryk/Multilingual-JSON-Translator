import json
import os
import pandas as pd

# 🔁 Load translation file (.json or .xlsx)
def load_translation_mapping(file_path):
    if file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            str(item["English"]).strip().lower(): str(item["German"]).strip()
            for item in data
            if "English" in item and "German" in item
        }

    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
        if "English" not in df.columns or "German" not in df.columns:
            raise ValueError("Excel file must contain 'English' and 'German' columns.")
        return {
            str(row["English"]).strip().lower(): str(row["German"]).strip()
            for _, row in df.iterrows()
            if pd.notna(row["English"]) and pd.notna(row["German"])
        }

    else:
        raise ValueError("Unsupported file format. Use .json or .xlsx")

# 🔄 Recursively replace English text with German (case-insensitive)
def translate_node(node, translation_dict):
    if isinstance(node, dict):
        return {k: translate_node(v, translation_dict) for k, v in node.items()}
    elif isinstance(node, list):
        return [translate_node(item, translation_dict) for item in node]
    elif isinstance(node, str):
        lower_node = node.strip().lower()
        return translation_dict.get(lower_node, node.strip())
    return node

# 📂 Main translate file function
def translate_file(source_json_path, translation_map_path, output_path):
    with open(source_json_path, "r", encoding="utf-8") as f:
        source_data = json.load(f)

    translation_dict = load_translation_mapping(translation_map_path)
    translated_data = translate_node(source_data, translation_dict)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Translated file saved to: {output_path}")

# 🚀 Entry point
if __name__ == "__main__":
    # 🔧 Customize these file names if needed
    source_json = "translation.json"                 # Your key-value English JSON
    translation_file = "eng-ger-trans file.xlsx"     # Your translation (JSON or Excel)
    output_json = "translated_output.json"           # Final output file

    # 🔍 Check that files exist before running
    if not os.path.exists(source_json) or not os.path.exists(translation_file):
        print("⚠️ Make sure both translation.json and the mapping file exist.")
    else:
        translate_file(source_json, translation_file, output_json)







# how to use this code
# In source_json ----> keep  (Prefered English Transaltion.json file)
# In translation_file ----> keep the (values of translation file (.xlsx or .json)) which new language you have to add (eng-ger-trans file.json)
#replace --German-- with your new language name contain in you .xlxs or .json exaple: (Turkish, Arabic, Hindi)
# By setting both this file you just have to run the code by "python translate.py"
    # -------> Output file is generated in the same folder