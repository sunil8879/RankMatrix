import re

def fix_and_add_country():
    input_file = 'universities.json'
    output_file = 'universities_with_country.json'
    
    # --- START OF COUNTRY MAP ---
    country_map = {
        "United States": [
            "Harvard", "Stanford", "MIT", "California", "Yale", "Princeton", "Columbia", "Chicago", "Pennsylvania", "Cornell", 
            "Johns Hopkins", "Washington", "Texas", "Michigan", "Northwestern", "Duke", "Wisconsin", "Purdue", "States", "NYU", 
            "UCLA", "Berkeley", "Maryland", "Minnesota", "Ohio State", "Georgia", "Florida", "Arizona", "Colorado", "Utah", 
            "Virginia", "Illinois", "Indiana", "Iowa", "Kansas", "Louisiana", "Massachusetts", "Missouri", "Nebraska", "Carolina", 
            "Oregon", "Tennessee", "Pittsburgh", "Rochester", "Emory", "Vanderbilt", "Rice", "Dartmouth", "Georgetown", "Carnegie Mellon", 
            "Irvine", "Davis", "Santa Barbara", "San Diego", "Houston", "Phoenix", "Philadelphia", "San Antonio", "Dallas", "San Jose"
        ],
        "United Kingdom": [
            "Oxford", "Cambridge", "UCL", "Imperial College", "Edinburgh", "King's College", "Manchester", "London", "Warwick", "Bristol", 
            "Glasgow", "Sheffield", "Kingdom", "Nottingham", "Southampton", "Birmingham", "Leeds", "Liverpool", "Cardiff", "Newcastle", 
            "Aberdeen", "Exeter", "Dundee", "Belfast", "Leicester", "Sussex", "St Andrews", "Durham", "Lancaster", "York", 
            "Bath", "Loughborough", "Surrey", "Reading", "Strathclyde", "Swansea", "Queen Mary", "Birkbeck", "City University", "Brunel", 
            "Plymouth", "Portsmouth", "Heriot-Watt", "Brighton", "Keele", "Essex", "Stirling", "Ulster", "Hull", "Aston"
        ],
        "United Arab Emirates": [
            "Emirates", "Dubai", "Sharjah", "Abu Dhabi", "Khalifa", "Zayed", "Ajman", "Al Ain", "American University in Dubai", 
            "Gulf Medical", "Hamdan Bin Mohammed", "British University in Dubai", "Middlesex Dubai", "Rochester Institute Dubai", 
            "Sorbonne Abu Dhabi", "NYU Abu Dhabi", "Canadian University Dubai", "Heriot-Watt Dubai", "Skyline University", 
            "Fujairah", "Ras Al Khaimah", "Higher Colleges of Technology", "UAEU", "Petroleum Institute", "Masdar"
        ],
        "Canada": [
            "Toronto", "British Columbia", "McGill", "McMaster", "Montreal", "Alberta", "Waterloo", "Canada", "Calgary", "Ottawa", 
            "Western Ontario", "Victoria", "Manitoba", "Dalhousie", "Laval", "Simon Fraser", "York University", "Saskatchewan", 
            "Guelph", "Concordia", "Sherbrooke", "Quebec", "Carleton", "Windsor", "New Brunswick", "Memorial University", "Ryerson", 
            "Brock", "Wilfrid Laurier", "Regina", "Trent", "Lakehead", "Ontario", "Nova Scotia", "Winnipeg", "Lethbridge"
        ],
        "Australia": [
            "Melbourne", "Queensland", "Sydney", "New South Wales", "Monash", "Western Australia", "Australia", "Adelaide", "Curtin", 
            "Macquarie", "Tasmania", "Wollongong", "Deakin", "Griffith", "James Cook", "La Trobe", "Flinders", "Newcastle Australia", 
            "South Australia", "RMIT", "Swinburne", "UTS", "QUT", "Murdoch", "Canberra", "Southern Cross", "Charles Sturt", 
            "Sunshine Coast", "Western Sydney", "Victoria University Australia", "Bond", "Edith Cowan"
        ],
        "New Zealand": [
            "Auckland", "Otago", "Canterbury", "Victoria University of Wellington", "Massey", "Waikato", "Lincoln University", 
            "AUT", "Auckland University of Technology", "Zealand", "Manukau", "Unitec", "Whitireia", "Otago Polytechnic"
        ],
        "Sweden": [
            "Lund", "Uppsala", "Karolinska", "Stockholm", "Gothenburg", "KTH", "Chalmers", "Sweden", "Umea", "Linkoping", 
            "Jonkoping", "Orebro", "Malmo", "Lulea", "Linnaeus", "Karlstad", "Halmstad", "Borås", "Skovde", "Södertörn"
        ],
        "Belgium": [
            "Leuven", "Ghent", "Louvain", "Brussels", "Liege", "Antwerp", "Vrije", "Katholieke", "Belgium", "Hasselt", "Mons", 
            "Namur", "Gembloux", "Kortrijk", "Bruges", "Wallonie"
        ],
        "Norway": [
            "Oslo", "Bergen", "NTNU", "Tromso", "Stavanger", "Norway", "Norwegian University of Life Sciences", "Agder", 
            "Nord University", "South-Eastern Norway", "Svalbard", "Ostfold", "Volda"
        ],
        "Saudi Arabia": [
            "King Saud", "King Abdulaziz", "KAUST", "KFUPM", "Riyadh", "Jeddah", "Dammam", "Saudi", "King Khalid", "King Faisal", 
            "Umm Al-Qura", "Princess Nourah", "Alfaisal", "Taibah", "Qassim", "Taif", "Najran", "Tabuk", "Al Jouf", "Jazan"
        ],
        "Qatar": [
            "Doha", "Qatar", "Hamad Bin Khalifa", "Weill Cornell Qatar", "Texas A&M Qatar", "Georgetown Qatar", "Northwestern Qatar"
        ],
        "Kuwait": [
            "Kuwait", "Gulf University for Science", "American University of Kuwait"
        ],
        "Bahrain": [
            "Bahrain", "Arabian Gulf University", "Ahlia", "Applied Science University Bahrain"
        ],
        "Oman": [
            "Sultan Qaboos", "Muscat", "Oman", "Dhofar", "Nizwa", "Sohar"
        ],
        "China": [
            "Tsinghua", "Peking", "Zhejiang", "Shanghai Jiao Tong", "Fudan", "Sun Yat-sen", "Huazhong", "Nanjing", "Wuhan", "China", 
            "Sichuan", "Xi'an", "Harbin", "Dalian", "Jilin", "Nankai", "Xiamen", "Shandong", "Tongji", "Tianjin", "Hunan", "Beijing", 
            "Guangdong", "Chongqing", "Soochow", "Lanzhou", "Southeast University", "Beihang", "Renmin", "East China", "Shenzhen", 
            "Xian Jiaotong", "Zhengzhou", "Ocean University", "South China", "Jinan", "Yunnan", "Hefei"
        ],
        "Russia": [
            "Moscow", "Saint Petersburg", "Novosibirsk", "Lomonosov", "Tomsk", "Ural", "Kazan", "Russia", "Sechenov", "MEPhI", 
            "Bauman", "MGIMO", "Skoltech", "Peter the Great", "RUDN", "Polytechnic Saint Petersburg", "ITMO", "Siberian", "Far Eastern"
        ],
        "South Africa": [
            "Cape Town", "Witwatersrand", "Stellenbosch", "KwaZulu-Natal", "Pretoria", "Johannesburg", "South Africa", "Western Cape", 
            "North-West University", "Rhodes University", "Free State", "Nelson Mandela", "Fort Hare", "Limpopo", "Venda"
        ],
        "Japan": [
            "Tokyo", "Kyoto", "Osaka", "Nagoya", "Tohoku", "Kyushu", "Hokkaido", "Tsukuba", "Keio", "Waseda", "Hiroshima", "Japan", 
            "Kobe", "Titus", "Okayama", "Chiba", "Kanazawa", "Kumamoto", "Tokushima", "Nagasaki", "Niigata", "Gifu", "Yokohama"
        ],
        "Hong Kong": [
            "HKU", "HKUST", "CUHK", "Hong Kong Polytechnic", "City University of Hong Kong", "Baptist University Hong Kong", "Lingnan", "Education University of Hong Kong"
        ],
        "South Korea": [
            "Seoul", "Yonsei", "KAIST", "Sungkyunkwan", "Korea University", "Pohang", "Hanyang", "Kyungpook", "Pusan", "Korea", 
            "Chonnam", "Chonbuk", "Konkuk", "Ewha", "Chung-Ang", "Gwangju", "Ajou", "Ulsan", "Sejong", "Inha", "Kyung Hee"
        ],
        "Singapore": [
            "National University of Singapore", "Nanyang Technological", "Singapore Management", "SUTD", "SIT Singapore"
        ],
        "Malaysia": [
            "Malaya", "Putra", "Kebangsaan", "Sains", "Teknologi Malaysia", "Taylor's", "UCSI", "Petronas", "Malaysia", "UiTM", 
            "Multimedia University", "Sunway", "Tenaga", "Utara", "Pahang", "Perlis", "Terengganu"
        ],
        "Germany": [
            "Munich", "Heidelberg", "Bonn", "Freiburg", "Tubingen", "Gottingen", "Frankfurt", "Germany", "Technische Universität", 
            "Karlsruhe", "Dresden", "Aachen", "Mainz", "Kiel", "Leipzig", "Stuttgart", "Ulm", "Erlangen", "Wurzburg", "Hamburg", 
            "Cologne", "Münster", "Düsseldorf", "Bremen", "Hannover", "Dortmund", "Darmstadt", "Konstanz", "Regensburg", "Jena"
        ],
        "France": [
            "Sorbonne", "Paris", "Saclay", "PSL", "France", "Grenoble", "Strasbourg", "Montpellier", "Bordeaux", "Marseille", "Lyon", 
            "Toulouse", "Nice", "Rennes", "Nantes", "Lille", "Clermont", "Lorraine", "Angers", "Versailles"
        ],
        "Italy": [
            "Bologna", "Sapienza", "Padua", "Milan", "Pisa", "Florence", "Italy", "Turin", "Naples", "Genoa", "Rome", "Trento", 
            "Pavia", "Verona", "Bari", "Palermo", "Trieste", "Siena", "Catania", "Ferrara", "Perugia", "Brescia", "Modena"
        ],
        "Netherlands": [
            "Utrecht", "Leiden", "Amsterdam", "Delft", "Eindhoven", "Wageningen", "Groningen", "Erasmus", "Radboud", "Twente", 
            "Maastricht", "Tilburg", "Netherlands", "Vrije Universiteit Amsterdam"
        ],
        "Luxembourg": [
            "Luxembourg"
        ],
        "Romania": [
            "Bucharest", "Babes-Bolyai", "Cluj", "Iasi", "Timisoara", "Romania", "Transilvania", "Craiova"
        ],
        "Poland": [
            "Warsaw", "Jagiellonian", "Krakow", "Wroclaw", "AGH", "Poland", "Adam Mickiewicz", "Lodz", "Gdansk", "Silesia", 
            "Nicolaus Copernicus", "Poznan"
        ]
    }
    # --- END OF COUNTRY MAP ---

    print("Starting country injection for 4,000 rows...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    processed_count = 0

    for line in lines:
        new_lines.append(line)
        
        # Look for the Institution line
        match = re.search(r'"Institution":\s*"([^"]+)"', line)
        
        if match:
            inst_name = match.group(1).strip()
            assigned_country = "Unknown"
            
            for country, keywords in country_map.items():
                if any(k.lower() in inst_name.lower() for k in keywords):
                    assigned_country = country
                    break
            
            # Inject Country line
            new_lines.append(f'   "Country": "{assigned_country}",\n')
            processed_count += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"DONE! Processed {processed_count} rows. Check {output_file}.")

if __name__ == "__main__":
    fix_and_add_country()