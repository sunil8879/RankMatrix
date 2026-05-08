import pandas as pd
import json
from datetime import datetime, timedelta

def excel_date_to_str(val):
    """Converts Excel serial dates (like 46204) to readable strings."""
    if isinstance(val, (int, float, str)) and str(val).isdigit():
        try:
            date_val = datetime(1899, 12, 30) + timedelta(days=int(float(val)))
            return date_val.strftime('%d %b %Y')
        except:
            return str(val)
    return str(val)

def process_inconsistent_excel(file_path):
    try:
        # Load Excel - assumes data is in the first column
        df = pd.read_excel(file_path, header=None)
        rows = df[0].astype(str).tolist()
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    all_scholarships = []
    # Initialize with a helper function to avoid KeyError
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
        
        # SKIP empty rows
        if not line or line == "nan":
            i += 1
            continue

        # TRIGGER: Start a new record
        if "Independent provider" in line or "Provided by university" in line:
            if current_obj is not None:
                all_scholarships.append(current_obj)
            current_obj = create_new_record()
            i += 1
            continue

        # If we haven't found a starting trigger yet, skip this line
        if current_obj is None:
            i += 1
            continue

        # LOGIC: Extract fields based on keywords
        if "INR" in line or "benefits" in line or "USD" in line or "GBP" in line:
            current_obj["AMOUNT"] = line
            
        elif line.lower() == "deadline":
            if i + 1 < len(rows):
                current_obj["DEADLINE"] = excel_date_to_str(rows[i+1])
                i += 1 # skip the date row
        
        elif "Read more about eligibility" in line:
            if i + 1 < len(rows):
                current_obj["UNIVERSITY"] = rows[i+1].strip()
            if i + 2 < len(rows):
                current_obj["LOCATION"] = rows[i+2].strip()
            i += 2 # skip university and location rows
            
        elif current_obj["SCHOLARSHIP"] == "Unknown":
            # If the line isn't a known label, it's likely the scholarship name
            if line not in ["Merit-based", "Need-based", "Grant", "Deadline"]:
                current_obj["SCHOLARSHIP"] = line

        i += 1

    # Append the final record
    if current_obj is not None:
        all_scholarships.append(current_obj)

    # Save to JSON
    output_name = 'cleaned_scholarships.json'
    with open(output_name, 'w', encoding='utf-8') as f:
        json.dump(all_scholarships, f, indent=4, ensure_ascii=False)

    print(f"Success! Processed {len(all_scholarships)} records into {output_name}")

# Run it
process_inconsistent_excel('data.xlsx')