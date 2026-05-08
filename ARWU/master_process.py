import re
import json

def process_greedy():
    input_file = 'input_data.txt'
    output_file = 'final_rankings.json'

    # --- YOUR EXTENDED COUNTRY MAP ---
    country_map = {
        "United States": ["Harvard", "Stanford", "MIT", "California", "Yale", "Princeton", "Columbia", "Chicago", "Pennsylvania", "Cornell", "Johns Hopkins", "Washington", "Texas", "Michigan", "Northwestern", "Duke", "Wisconsin", "Purdue", "States", "NYU", "UCLA", "Berkeley", "Maryland", "Minnesota", "Ohio State", "Georgia", "Florida", "Arizona", "Colorado", "Utah", "Virginia", "Illinois", "Indiana", "Iowa", "Kansas", "Louisiana", "Massachusetts", "Missouri", "Nebraska", "Carolina", "Oregon", "Tennessee", "Pittsburgh", "Rochester", "Emory", "Vanderbilt", "Rice", "Dartmouth", "Georgetown", "Carnegie Mellon", "Irvine", "Davis", "Santa Barbara", "San Diego", "Houston", "Phoenix", "Philadelphia", "San Antonio", "Dallas", "San Jose"],
        "United Kingdom": ["Oxford", "Cambridge", "UCL", "Imperial College", "Edinburgh", "King's College", "Manchester", "London", "Warwick", "Bristol", "Glasgow", "Sheffield", "Kingdom", "Nottingham", "Southampton", "Birmingham", "Leeds", "Liverpool", "Cardiff", "Newcastle", "Aberdeen", "Exeter", "Dundee", "Belfast", "Leicester", "Sussex", "St Andrews", "Durham", "Lancaster", "York", "Bath", "Loughborough", "Surrey", "Reading", "Strathclyde", "Swansea", "Queen Mary", "Birkbeck", "City University", "Brunel", "Plymouth", "Portsmouth", "Heriot-Watt", "Brighton", "Keele", "Essex", "Stirling", "Ulster", "Hull", "Aston"],
        "United Arab Emirates": ["Emirates", "Dubai", "Sharjah", "Abu Dhabi", "Khalifa", "Zayed", "Ajman", "Al Ain", "American University in Dubai", "Gulf Medical", "Hamdan Bin Mohammed", "British University in Dubai", "Middlesex Dubai", "Rochester Institute Dubai", "Sorbonne Abu Dhabi", "NYU Abu Dhabi", "Canadian University Dubai", "Heriot-Watt Dubai", "Skyline University", "Fujairah", "Ras Al Khaimah", "Higher Colleges of Technology", "UAEU", "Petroleum Institute", "Masdar"],
        "Canada": ["Toronto", "British Columbia", "McGill", "McMaster", "Montreal", "Alberta", "Waterloo", "Canada", "Calgary", "Ottawa", "Western Ontario", "Victoria", "Manitoba", "Dalhousie", "Laval", "Simon Fraser", "York University", "Saskatchewan", "Guelph", "Concordia", "Sherbrooke", "Quebec", "Carleton", "Windsor", "New Brunswick", "Memorial University", "Ryerson", "Brock", "Wilfrid Laurier", "Regina", "Trent", "Lakehead", "Ontario", "Nova Scotia", "Winnipeg", "Lethbridge"],
        "Australia": ["Melbourne", "Queensland", "Sydney", "New South Wales", "Monash", "Western Australia", "Australia", "Adelaide", "Curtin", "Macquarie", "Tasmania", "Wollongong", "Deakin", "Griffith", "James Cook", "La Trobe", "Flinders", "Newcastle Australia", "South Australia", "RMIT", "Swinburne", "UTS", "QUT", "Murdoch", "Canberra", "Southern Cross", "Charles Sturt", "Sunshine Coast", "Western Sydney", "Victoria University Australia", "Bond", "Edith Cowan"],
        "China": ["Tsinghua", "Peking", "Zhejiang", "Shanghai Jiao Tong", "Fudan", "Sun Yat-sen", "Huazhong", "Nanjing", "Wuhan", "China", "Sichuan", "Xi'an", "Harbin", "Dalian", "Jilin", "Nankai", "Xiamen", "Shandong", "Tongji", "Tianjin", "Hunan", "Beijing", "Guangdong", "Chongqing", "Soochow", "Lanzhou", "Southeast University", "Beihang", "Renmin", "East China", "Shenzhen", "Xian Jiaotong", "Zhengzhou", "Ocean University", "South China", "Jinan", "Yunnan", "Hefei"],
        "Japan": ["Tokyo", "Kyoto", "Osaka", "Nagoya", "Tohoku", "Kyushu", "Hokkaido", "Tsukuba", "Keio", "Waseda", "Hiroshima", "Japan", "Kobe", "Okayama", "Chiba", "Kanazawa", "Kumamoto", "Tokushima", "Nagasaki", "Niigata", "Gifu", "Yokohama"]
    }


    final_list = []
    current_subject = "Unknown"
    current_item = {}

    print("Reading file...")
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue

            # 1. Detect Subject Header (All CAPS words on their own line)
            # This looks for lines like "AEROSPACE" or "AGRICULTURAL SCIENCES"
            if re.match(r'^[A-Z\s&]{3,25}$', line) and "Rank" not in line:
                current_subject = line
                continue

            # 2. Detect start of a university record
            if line.startswith('{'):
                current_item = {"Subject": current_subject}
                continue

            # 3. Extract any "Key": "Value" pairs using Regex
            # This works even if the JSON is malformed
            match = re.search(r'"([^"]+)":\s*"([^"]*)"', line)
            if match:
                key, val = match.group(1), match.group(2)
                current_item[key] = val
                
                # If we just found the Institution, also assign the Country
                if key == "Institution":
                    assigned_country = "Unknown"
                    for country, keywords in country_map.items():
                        if any(k.lower() in val.lower() for k in keywords):
                            assigned_country = country
                            break
                    current_item["Country"] = assigned_country

            # 4. Detect end of record and save it
            if line.startswith('}') or line.startswith('},'):
                if "Institution" in current_item:
                    final_list.append(current_item)
                current_item = {}

    # Save to clean JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=3)

    print(f"SUCCESS! Processed {len(final_list)} rows.")
    print(f"File saved as: {output_file}")

if __name__ == "__main__":
    process_greedy()