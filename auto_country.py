import json
import re

def fully_automated_mapping():
    input_file = 'webometrics.json'
    output_file = 'webometrics_with_country.json'

    # --- MASSIVE COUNTRY MAP (50+ KEYWORDS PER MAJOR COUNTRY) ---
    country_map = {
        "United States": ["Harvard", "Stanford", "MIT", "California", "Yale", "Princeton", "Columbia", "Chicago", "Pennsylvania", "Cornell", "Johns Hopkins", "Washington", "Texas", "Michigan", "Northwestern", "Duke", "Wisconsin", "Purdue", "NYU", "UCLA", "Berkeley", "Maryland", "Minnesota", "Ohio State", "Georgia", "Florida", "Arizona", "Colorado", "Utah", "Virginia", "Illinois", "Indiana", "Iowa", "Kansas", "Louisiana", "Massachusetts", "Missouri", "Nebraska", "Carolina", "Oregon", "Tennessee", "Pittsburgh", "Rochester", "Emory", "Vanderbilt", "Rice", "Dartmouth", "Georgetown", "Carnegie Mellon", "Irvine", "Davis", "Santa Barbara", "San Diego", "Houston", "States", "USA"],
        "United Kingdom": ["Oxford", "Cambridge", "UCL", "Imperial College", "Edinburgh", "King's College", "Manchester", "London", "Warwick", "Bristol", "Glasgow", "Sheffield", "Nottingham", "Southampton", "Birmingham", "Leeds", "Liverpool", "Cardiff", "Newcastle", "Aberdeen", "Exeter", "Dundee", "Belfast", "Leicester", "Sussex", "St Andrews", "Durham", "Lancaster", "York", "Bath", "Loughborough", "Surrey", "Reading", "Strathclyde", "Swansea", "Queen Mary", "Birkbeck", "City University", "Brunel", "Plymouth", "Portsmouth", "Heriot-Watt", "Brighton", "Keele", "Essex", "Stirling", "Ulster", "Hull", "Aston", "Kingdom", "UK"],
        "China": ["Tsinghua", "Peking", "Zhejiang", "Shanghai Jiao Tong", "Fudan", "Sun Yat-sen", "Huazhong", "Nanjing", "Wuhan", "Sichuan", "Xi'an", "Harbin", "Dalian", "Jilin", "Nankai", "Xiamen", "Shandong", "Tongji", "Tianjin", "Hunan", "Beijing", "Guangdong", "Chongqing", "Soochow", "Lanzhou", "Southeast University", "Beihang", "Renmin", "East China", "Shenzhen", "Xian Jiaotong", "Zhengzhou", "Ocean University", "South China", "Jinan", "Yunnan", "Hefei", "China"],
        "Canada": ["Toronto", "British Columbia", "McGill", "McMaster", "Montreal", "Alberta", "Waterloo", "Calgary", "Ottawa", "Western Ontario", "Victoria", "Manitoba", "Dalhousie", "Laval", "Simon Fraser", "York University", "Saskatchewan", "Guelph", "Concordia", "Sherbrooke", "Quebec", "Carleton", "Windsor", "New Brunswick", "Memorial University", "Ryerson", "Brock", "Wilfrid Laurier", "Regina", "Trent", "Lakehead", "Ontario", "Nova Scotia", "Winnipeg", "Lethbridge", "Canada"],
        "Australia": ["Melbourne", "Queensland", "Sydney", "New South Wales", "Monash", "Western Australia", "Adelaide", "Curtin", "Macquarie", "Tasmania", "Wollongong", "Deakin", "Griffith", "James Cook", "La Trobe", "Flinders", "Newcastle Australia", "South Australia", "RMIT", "Swinburne", "UTS", "QUT", "Murdoch", "Canberra", "Southern Cross", "Charles Sturt", "Sunshine Coast", "Western Sydney", "Victoria University Australia", "Bond", "Edith Cowan", "Australia"],
        "Japan": ["Tokyo", "Kyoto", "Osaka", "Nagoya", "Tohoku", "Kyushu", "Hokkaido", "Tsukuba", "Keio", "Waseda", "Hiroshima", "Kobe", "Okayama", "Chiba", "Kanazawa", "Kumamoto", "Tokushima", "Nagasaki", "Niigata", "Gifu", "Yokohama", "Japan"],
        "Germany": ["Munich", "Heidelberg", "Bonn", "Freiburg", "Tubingen", "Gottingen", "Frankfurt", "Karlsruhe", "Dresden", "Aachen", "Mainz", "Kiel", "Leipzig", "Stuttgart", "Ulm", "Erlangen", "Wurzburg", "Hamburg", "Cologne", "Münster", "Düsseldorf", "Bremen", "Hannover", "Dortmund", "Darmstadt", "Konstanz", "Regensburg", "Jena", "Germany", "Technische"],
        "France": ["Sorbonne", "Paris", "Saclay", "PSL", "Grenoble", "Strasbourg", "Montpellier", "Bordeaux", "Marseille", "Lyon", "Toulouse", "Nice", "Rennes", "Nantes", "Lille", "Clermont", "Lorraine", "Angers", "Versailles", "France"],
        "United Arab Emirates": ["Emirates", "Dubai", "Sharjah", "Abu Dhabi", "Khalifa", "Zayed", "UAE"],
        "New Zealand": ["Auckland", "Otago", "Canterbury", "Victoria University of Wellington", "Massey", "Waikato", "Zealand"],
        "Sweden": ["Lund", "Uppsala", "Karolinska", "Stockholm", "Gothenburg", "KTH", "Chalmers", "Sweden"],
        "Belgium": ["Leuven", "Ghent", "Louvain", "Brussels", "Liege", "Antwerp", "Belgium"],
        "Norway": ["Oslo", "Bergen", "NTNU", "Tromso", "Norway"],
        "Saudi Arabia": ["King Saud", "King Abdulaziz", "KAUST", "KFUPM", "Riyadh", "Saudi"],
        "Qatar": ["Doha", "Qatar"],
        "Kuwait": ["Kuwait"],
        "Bahrain": ["Bahrain"],
        "Oman": ["Sultan Qaboos", "Oman"],
        "Russia": ["Moscow", "Saint Petersburg", "Novosibirsk", "Lomonosov", "Tomsk", "Russia"],
        "South Africa": ["Cape Town", "Witwatersrand", "Stellenbosch", "Johannesburg", "Pretoria", "South Africa"],
        "Hong Kong": ["HKU", "HKUST", "CUHK", "Hong Kong"],
        "South Korea": ["Seoul", "Yonsei", "KAIST", "Sungkyunkwan", "Korea University", "Pohang", "Hanyang", "Korea"],
        "Singapore": ["National University of Singapore", "Nanyang", "Singapore"],
        "Malaysia": ["Malaya", "Putra", "Kebangsaan", "Sains", "Malaysia"],
        "Italy": ["Bologna", "Sapienza", "Padua", "Milan", "Pisa", "Florence", "Italy"],
        "Netherlands": ["Utrecht", "Leiden", "Amsterdam", "Delft", "Eindhoven", "Netherlands"],
        "Luxembourg": ["Luxembourg"],
        "Romania": ["Bucharest", "Babes-Bolyai", "Romania"],
        "Poland": ["Warsaw", "Jagiellonian", "Krakow", "Poland"]
    }

    print("--- Starting Automated Mapping ---")

    try:
        # 1. READ & REPAIR MALFORMED JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            raw = f.read()
        
        # Regex to fix common trailing commas before brackets like ,] or ,}
        clean_json = re.sub(r',\s*([\]}])', r'\1', raw)
        data = json.loads(clean_json)

        # 2. MATCH AND INJECT
        processed = 0
        unknown = 0

        for item in data:
            # Handle key variations and trailing spaces
            uni_name = item.get("University", item.get("Institution", "")).strip()
            item["University"] = uni_name # Cleanup original name
            
            assigned = "Unknown"
            for country, keywords in country_map.items():
                if any(k.lower() in uni_name.lower() for k in keywords):
                    assigned = country
                    break
            
            item["Country"] = assigned
            processed += 1
            if assigned == "Unknown": unknown += 1

        # 3. SAVE CLEAN OUTPUT
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"SUCCESS: Processed {processed} records.")
        print(f"MATCHED: {processed - unknown}")
        print(f"UNKNOWN: {unknown} (Check these and add keywords to script if needed)")
        print(f"File Saved: {output_file}")

    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    fully_automated_mapping()