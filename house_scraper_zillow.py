import requests
import random
import pandas as pd
from bs4 import BeautifulSoup
import time

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
]

def fetch_house_listings(url: str):
    """
    Fetch house listings from Zillow.
    
    :param url: URL of the Zillow page to scrape.
    :return: List of dictionaries containing house details.
    """
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/'
    }

    listings = []
    page = 1

    while True:
        response = requests.get(f"{url}/{page}_p/", headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            break

        # Print the HTML content to a file for debugging
        with open(f'zillow_output_page_{page}.html', 'w', encoding='utf-8') as file:
            file.write(response.text)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Adjust selectors based on the actual website
        page_listings = soup.select('.StyledPropertyCardDataWrapper-c11n-8-107-0__sc-hfbvv9-0')
        if not page_listings:
            break

        for listing in page_listings:
            title_element = listing.select_one('.bJtJNq')
            price_element = listing.select_one('.eLqtVY')
            location_element = listing.select_one('.iwOFcv')
            description_element = listing.select_one('.bziRDw')

            title = title_element.get_text(strip=True) if title_element else 'N/A'
            price = price_element.get_text(strip=True) if price_element else 'N/A'
            location = location_element.get_text(strip=True) if location_element else 'N/A'
            description = description_element.get_text(strip=True) if description_element else 'N/A'
            
            # Debug print to check location
            print(f"Title: {title}, Price: {price}, Location: {location}, Description: {description}")

            listings.append({
                'title': title,
                'price': price,
                'location': location,
                'description': description
            })

        page += 1
        time.sleep(1)  # Be polite and avoid hitting the server too hard

    return listings

def save_to_csv(listings, filename: str):
    """
    Save the house listings to a CSV file.
    
    :param listings: List of dictionaries containing house details.
    :param filename: Name of the CSV file to save the data.
    """
    if listings:
        df = pd.DataFrame(listings)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No listings to save.")

def main():
    url = 'https://www.zillow.com/homes/for_sale/Concord-NC'
    listings = fetch_house_listings(url)

    if listings:
        for idx, listing in enumerate(listings, start=1):
            print(f"House {idx}:")
            print(f"  Title: {listing['title']}")
            print(f"  Price: {listing['price']}")
            print(f"  Location: {listing['location']}")
            print(f"  Description: {listing['description']}")
            print()
        
        save_to_csv(listings, 'house_listings_zillow.csv')
    else:
        print("No listings found.")

if __name__ == "__main__":
    main()