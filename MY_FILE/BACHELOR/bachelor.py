import pandas as pd
import json
from datetime import datetime, timedelta

def excel_date_to_str(val):
    """Converts 46142 style numbers to readable dates like 01 May 2026."""
    if isinstance(val, (int, float, str)) and str(val).replace('.','',1).isdigit():
        try:
            # Excel serial to Python date
            date_val = datetime(1899, 12, 30) + timedelta(days=int(float(val)))
            return date_val.strftime('%d %b %Y')
        except:
            return str(val)
    return str(val)

def process_scholarships(file_path):
    try:
        # Load the Excel file
        df = pd.read_excel(file_path, header=None)
        rows = df[0].astype(str).tolist()
    except Exception as e:
        print(f"Error: {e}")
        return

    all_data = []
    current_item = None

    i = 0
    while i < len(rows):
        line = rows[i].strip()
        
        # 1. Skip junk
        if not line or line == "nan":
            i += 1
            continue

        # 2. TRIGGER: Start a new scholarship block
        if "Independent provider" in line or "Provided by university" in line:
            if current_item:
                all_data.append(current_item)
            current_item = {
                "UNIVERSITY NAME": "Unknown",
                "SCHOLARSHIP NAME": "Unknown",
                "AMOUNT": "Unknown",
                "DEADLINE": "Unknown",
                "LOCATION": "Unknown"
            }
            i += 1
            continue

        if current_item is None:
            i += 1
            continue

        # 3. LANDMARK: Amount (Finds currency or 'benefits')
        if any(x in line for x in ["INR", "USD", "GBP", "EUR", "benefits"]):
            current_item["AMOUNT"] = line

        # 4. LANDMARK: Deadline
        elif line.lower() == "deadline":
            if i + 1 < len(rows):
                current_item["DEADLINE"] = excel_date_to_str(rows[i+1])
                i += 1

        # 5. LANDMARK: University and Location
        elif "Read more about eligibility" in line:
            if i + 1 < len(rows):
                current_item["UNIVERSITY NAME"] = rows[i+1].strip()
            if i + 2 < len(rows):
                current_item["LOCATION"] = rows[i+2].strip()
            i += 2

        # 6. CATCH-ALL: Scholarship Name
        # If the line isn't a known label, it's likely the scholarship title
        elif current_item["SCHOLARSHIP NAME"] == "Unknown":
            if line not in ["Grant", "Merit-based", "Need-based", "Deadline"]:
                current_item["SCHOLARSHIP NAME"] = line

        i += 1

    # Add the last one
    if current_item:
        all_data.append(current_item)

    # FINAL CLEANUP: Swap logic for missing fields
    final_output = []
    for item in all_data:
        # Swap if University is missing but Location is filled
        if item["UNIVERSITY NAME"] in ["Unknown", "nan"] and item["LOCATION"] not in ["Unknown", "nan"]:
            item["UNIVERSITY NAME"] = item["LOCATION"]
            item["LOCATION"] = "Not specified"
        
        # Standardize "Location not available"
        if "Location not available" in item["LOCATION"] or item["LOCATION"] == "nan":
            item["LOCATION"] = "Not specified"
            
        final_output.append(item)

    # Save to JSON
    with open('scholarship_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    print(f"Success! Processed {len(final_output)} records.")

# To run: make sure your file is named 'data.xlsx'
process_scholarships('data.xlsx')