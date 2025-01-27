import requests
import random
import pandas as pd
from bs4 import BeautifulSoup
import time
import logging
import os
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO)

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
        'Referer': 'https://www.google.com/',
        'Origin': 'https://www.zillow.com',
    }

    retries = 3
    for attempt in range(retries):
        try:
            # Simulate a delay between requests to avoid being blocked
            time.sleep(random.uniform(2, 5))  # Random delay between 2 and 5 seconds
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for 4xx or 5xx status codes
            break  # Break out of loop if successful
        except RequestException as e:
            logging.error(f"Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                logging.error("Max retries reached. Exiting.")
                return []

    listings = []
    soup = BeautifulSoup(response.content, 'html.parser')

    # Adjust selectors based on the actual website
    properties = soup.select('.StyledPropertyCardDataWrapper-c11n-8-107-0__sc-hfbvv9-0')
    if not properties:
        logging.error("No properties found on the page. Please check the selectors or page structure.")
        return listings

    for x in range(0, len(properties)):
        obj = {}
        
        try:
            obj["pricing"] = properties[x].find("span", {'data-test': 'property-card-price'}).text
        except AttributeError:
            obj["pricing"] = None

        try:
            size = properties[x].find("ul", {"class": "StyledPropertyCardHomeDetailsList-c11n-8-107-0__sc-1j0som5-0"}).find_all('li')[-1].text
            obj["size"] = size if size else "N/A"
        except AttributeError:
            obj["size"] = "N/A"
        
        try:
            obj["address"] = properties[x].find("address").text
        except AttributeError:
            obj["address"] = None
        
        # Extracting the number of bedrooms and bathrooms
        try:
            details = properties[x].find("ul", {"class": "StyledPropertyCardHomeDetailsList-c11n-8-107-0__sc-1j0som5-0"}).find_all('li')
            obj["bedrooms"] = details[0].text if len(details) > 0 else "N/A"
            obj["bathrooms"] = details[1].text if len(details) > 1 else "N/A"
        except (AttributeError, IndexError):
            obj["bedrooms"] = "N/A"
            obj["bathrooms"] = "N/A"

        listings.append(obj)

    return listings

def save_to_csv(listings, filename: str):
    """
    Save the house listings to a CSV file.
    
    :param listings: List of dictionaries containing house details.
    :param filename: Name of the CSV file to save the data.
    """
    if listings:
        try:
            df = pd.DataFrame(listings)
            if os.path.exists(filename):
                df_existing = pd.read_csv(filename)
                df_combined = pd.concat([df_existing, df], ignore_index=True)
                df_combined.to_csv(filename, index=False)
            else:
                df.to_csv(filename, index=False)
            logging.info(f"Data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving data to CSV: {e}")
    else:
        logging.warning("No listings to save.")

def get_all_listings(base_url, max_pages=5):
    """
    Scrape multiple pages of Zillow listings for Concord, NC.
    
    :param base_url: Base URL for the search results.
    :param max_pages: Maximum number of pages to scrape.
    :return: List of all listings.
    """
    all_listings = []
    for page in range(1, max_pages + 1):
        url = f"{base_url}{page}_p/"
        logging.info(f"Scraping page {page}: {url}")
        listings = fetch_house_listings(url)
        if listings:
            all_listings.extend(listings)
        else:
            logging.warning(f"No listings found on page {page}.")
            break  # Stop if no listings are found on a page (end of results)
    return all_listings

def main():
    base_url = 'https://www.zillow.com/homes/for_sale/Concord-NC/'
    all_listings = get_all_listings(base_url)

    if all_listings:
        for idx, listing in enumerate(all_listings, start=1):
            print(f"House {idx}:")
            print(f"  Pricing: {listing['pricing']}")
            print(f"  Size: {listing['size']}")
            print(f"  Address: {listing['address']}")
            print(f"  Bedrooms: {listing['bedrooms']}")
            print(f"  Bathrooms: {listing['bathrooms']}")
            print()
        
        save_to_csv(all_listings, 'house_listings_concord_nc.csv')
    else:
        logging.error("No listings found.")

if __name__ == "__main__":
    main()
