# Zillow Scraper and GUI Viewer

This project consists of two main components:

### 1. A Web Scraper
Fetch house listings from Zillow.

### 2. A GUI Viewer
Display the scraped data in a user-friendly interface.

---

## Features

### Web Scraper
- Scrapes Zillow's house listings using `requests` and `BeautifulSoup`.
- Handles pagination to gather data from multiple pages.
- Saves the scraped data (title, price, location, and description) into a CSV file.
- Utilizes randomized user-agent headers to avoid detection.

### GUI Viewer
- Reads the saved CSV file and displays the house listings in a GUI format.
- Built with `tkinter` for an intuitive and interactive display.
- Supports scrolling and displays data in a tabular format using `ttk.Treeview`.

---

## Installation

### Prerequisites
- Python 3.8+
- Install the required libraries:
  ```bash
  pip install requests pandas beautifulsoup4
  ```

---

## Usage

### Step 1: Scraping Zillow Listings
1. Update the `url` variable in the `main()` function of the scraper script to match the desired Zillow location. Example:
   ```python
   url = 'https://www.zillow.com/homes/for_sale/Concord-NC'
   ```
2. Run the scraper script:
   ```bash
   python scraper.py
   ```
3. The script will scrape listings and save them to `house_listings_zillow.csv`.

### Step 2: Viewing Listings in the GUI
1. Run the GUI viewer script:
   ```bash
   python viewer.py
   ```
2. The application will open a window displaying the scraped house listings in a table format.

---

## File Structure
- `scraper.py`: Contains the web scraper code.
- `viewer.py`: Contains the GUI viewer code.
- `house_listings_zillow.csv`: The output file where the scraped data is saved.

---

## Notes
- The scraper script uses randomized user-agents for each request to avoid getting blocked by Zillow.
- Ensure you respect Zillow's terms of service and scraping policies.
- Adjust HTML selectors in the scraper as Zillow's website structure may change over time.

---

## Example Output

### Console Output (Scraper)
```
House 1:
  Title: Beautiful 3-Bedroom Home
  Price: $350,000
  Location: Concord, NC
  Description: Spacious home with modern amenities.

Data saved to house_listings_zillow.csv
```

### GUI Viewer
Displays the scraped listings in a neat table with the following columns:
- Title
- Price
- Location
- Description

---

## Future Improvements
- Add filtering and sorting options in the GUI.
- Include more details in the scraped data, such as square footage and number of bedrooms/bathrooms.
- Enhance the scraper to handle CAPTCHA challenges.

---

## License
This project is licensed under the MIT License.

