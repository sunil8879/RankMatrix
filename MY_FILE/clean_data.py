import pandas as pd
import json
from datetime import datetime, timedelta

def excel_date_to_str(val):
    if isinstance(val, (int, float, str)) and str(val).replace('.','',1).isdigit():
        try:
            date_val = datetime(1899, 12, 30) + timedelta(days=int(float(val)))
            return date_val.strftime('%d %b %Y')
        except:
            return str(val)
    return str(val)

def process_inconsistent_excel(file_path):
    try:
        df = pd.read_excel(file_path, header=None)
        rows = df[0].astype(str).tolist()
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    all_scholarships = []
    
    def create_new_record():
        return {
            "UNIVERSITY": "Unknown",
            "SCHOLARSHIP": "Unknown",
            "AMOUNT": "Unknown",
            "DEADLINE": "Unknown",
            "LOCATION": "Unknown"
        }

    current_obj = None
    i = 0
    while i < len(rows):
        line = rows[i].strip()
        
        if not line or line == "nan":
            i += 1
            continue

        if "Independent provider" in line or "Provided by university" in line:
            if current_obj is not None:
                all_scholarships.append(current_obj)
            current_obj = create_new_record()
            i += 1
            continue

        if current_obj is None:
            i += 1
            continue

        # Logic for Fields
        if any(curr in line for curr in ["INR", "benefits", "USD", "GBP", "EUR"]):
            current_obj["AMOUNT"] = line
            
        elif line.lower() == "deadline":
            if i + 1 < len(rows):
                current_obj["DEADLINE"] = excel_date_to_str(rows[i+1])
                i += 1
        
        elif "Read more about eligibility" in line:
            # Look ahead for University and Location
            val1 = rows[i+1].strip() if i + 1 < len(rows) else "nan"
            val2 = rows[i+2].strip() if i + 2 < len(rows) else "nan"
            
            current_obj["UNIVERSITY"] = val1
            current_obj["LOCATION"] = val2
            i += 2
            
        elif current_obj["SCHOLARSHIP"] == "Unknown":
            if line not in ["Merit-based", "Need-based", "Grant", "Deadline"]:
                current_obj["SCHOLARSHIP"] = line

        i += 1

    if current_obj is not None:
        all_scholarships.append(current_obj)

    # --- DATA POST-PROCESSING (The Swap Logic) ---
    cleaned_list = []
    for item in all_scholarships:
        # 1. Clean up "nan" strings
        for key in item:
            if item[key].lower() == "nan":
                item[key] = "Unknown"

        # 2. SWAP: If University is unknown but Location has data
        # (This handles the case where the University name fell into the Location field)
        if item["UNIVERSITY"] in ["Unknown", "nan"] and item["LOCATION"] not in ["Unknown", "nan"]:
            item["UNIVERSITY"] = item["LOCATION"]
            item["LOCATION"] = "Not specified"
        
        # 3. Final polish for Location
        if item["LOCATION"] == "Unknown":
            item["LOCATION"] = "Not specified"

        cleaned_list.append(item)

    # Save to JSON
    output_name = 'cleaned_scholarships.json'
    with open(output_name, 'w', encoding='utf-8') as f:
        json.dump(cleaned_list, f, indent=4, ensure_ascii=False)

    print(f"Success! Processed {len(cleaned_list)} records into {output_name}")

process_inconsistent_excel('data.xlsx')