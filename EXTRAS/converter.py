import json
import re

def clean_data():
    input_file = 'data.txt'
    output_json = 'rankings.json'
    
    final_data = []
    current_subject = ""

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 1. Skip empty lines
            if not line:
                continue
            
            # 2. Identify the Subject (All Caps lines like ACOUSTICS)
            # This regex looks for lines that don't start with quotes/numbers
            if re.match(r'^[A-Z\s&]{3,}$', line):
                current_subject = line
                continue
            
            # 3. Skip the Header rows
            if "World Rank" in line:
                continue
                
            # 4. Process Data Rows
            # Remove surrounding quotes and clean up spaces before commas
            clean_line = line.replace('"', '').replace(' ,', ',').strip()
            
            # Ensure it's an actual data row (starts with a number)
            if re.match(r'^\d+,', clean_line):
                parts = clean_line.split(',')
                
                # Check if we have enough parts (Rank, Country, Institution, Score)
                if len(parts) >= 4:
                    entry = {
                        "Subject": current_subject,
                        "World Rank": int(parts[0]),
                        "Country": parts[1].strip(),
                        # The institution might contain commas (like UC San Diego)
                        # so we join all parts between the country and the score
                        "Institution": ",".join(parts[2:-1]).strip(),
                        "Score": float(parts[-1])
                    }
                    final_data.append(entry)

    # Save to JSON file
    with open(output_json, 'w', encoding='utf-8') as jf:
        json.dump(final_data, jf, indent=4)
        
    print(f"Success! Processed {len(final_data)} rows into rankings.json")

if __name__ == "__main__":
    clean_data()