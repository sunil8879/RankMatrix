import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_the_unijobs(pages_to_scrape=5):
    base_url = "https://www.timeshighereducation.com/unijobs/listings/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    all_data = []
    
    print(f"Starting scrape for {pages_to_scrape} pages...")

    for page in range(1, pages_to_scrape + 1):
        # Construct URL for pagination
        url = f"{base_url}?page={page}"
        print(f"Scraping Page {page}: {url}")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to retrieve page {page}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all job listing containers
            job_listings = soup.find_all('div', class_='listing-item__details')
            
            for job in job_listings:
                # 1. Institute Name
                inst_elem = job.find('li', class_='listing-item__info--institution')
                institute = inst_elem.text.strip() if inst_elem else "N/A"
                
                # 2. Country (Usually at the end of the location string)
                loc_elem = job.find('li', class_='listing-item__info--location')
                location = loc_elem.text.strip() if loc_elem else "N/A"
                country = location.split(',')[-1].strip() if ',' in location else location
                
                # 3. Course Name (Job Title)
                title_elem = job.find('h3', class_='listing-item__title')
                job_title = title_elem.text.strip() if title_elem else "N/A"
                
                # 4. Salary Offered
                salary_elem = job.find('li', class_='listing-item__info--salary')
                salary = salary_elem.text.strip() if salary_elem else "Competitive/Not Disclosed"

                all_data.append({
                    "Institute name": institute,
                    "name of country": country,
                    "course name": job_title,
                    "salary offered": salary
                })
            
            # Brief pause to be respectful to the server
            time.sleep(1)
            
        except Exception as e:
            print(f"Error on page {page}: {e}")

    # Create DataFrame and Save
    df = pd.DataFrame(all_data)
    df.to_csv("THE_Unijobs_Data.csv", index=False)
    print(f"Success! Saved {len(df)} rows to 'THE_Unijobs_Data.csv'")

# Run the function (Adjust number of pages as needed)
scrape_the_unijobs(pages_to_scrape=1000)