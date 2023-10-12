# Trip Santai Tour Data Scraper

This Python script is a web scraper designed to extract and collect information about tours from the [Trip Santai](https://www.tripsantai.com/) website. It utilizes the `requests` library to fetch web pages, `BeautifulSoup` for parsing HTML, and writes the collected data to a CSV file.

## Prerequisites

Before using this script, make sure you have the following Python libraries installed:

- `requests`
- `BeautifulSoup`

You can install these libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Usage

1. Clone this repository to your local machine.

2. Modify the `BASE_URL` in the script to the specific URL of the tours you want to scrape on the Trip Santai website.

3. Run the script:

```bash
python trip_santai_scraper.py
```

4. The script will fetch tour data, including tour name, category, destination, duration, pricing, itinerary, and inclusions/exclusions.

5. The collected data will be written to a CSV file named `data_tour_tripsantai.csv`.

## Code Structure

- `constants.py`: Contains constants like `BASE_URL` and `TIMEOUT`.
- `utils.py`: Contains utility functions for extracting and cleaning text from HTML elements.
- `trip_santai_scraper.py`: The main script for scraping tour data.
- `requirements.txt`: Lists the required Python libraries.

## Contact

If you have any questions or suggestions, please feel free to contact us.

Happy web scraping!
