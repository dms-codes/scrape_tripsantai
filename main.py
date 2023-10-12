import requests
from bs4 import BeautifulSoup as bs
import csv

# Constants
BASE_URL = "https://www.tripsantai.com/tour-search-result/"
TIMEOUT = 30
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
}

# Function to extract and clean text from an element
def extract_text(element):
    return element.text.strip() if element else ''

def extract_harpil(table, soup):
    try:
        harpil_data = [' '.join([td.text.strip() for td in tr.find_all('td')]) for tr in table.find_all('tr')]
    except:
        harpil_data = [soup.find('div', class_='b4div').text]
    return '\n'.join(harpil_data)

def extract_price_includes_and_excludes(itinerary_div):
    includes = None
    excludes = None
    text = itinerary_div.text
    separators = ['Harga Termasuk', 'Harga Tidak Termasuk', 'Note :', 'INCLUDE', 'EXCLUDE', 'Harga Paket Termasuk', 'Harga Paket Tidak Termasuk', 'Harga termasuk :', 'Harga Tidak Termasuk :']

    for separator in separators:
        if separator in text:
            parts = text.split(separator)
            if includes is None:
                includes = parts[1]
            else:
                excludes = parts[1]

    return includes, excludes

def fetch_details(session, url):
    data_tour = {
        'Nama': '',
        'URL': url,
        'Kategori': '',
        'Destinasi': '',
        'Durasi': '',
        'Harga': '',
        'Itinerari': '',
        'Harga Termasuk': '',
        'Harga Tidak Termasuk': '',
    }

    html = session.get(url, timeout=TIMEOUT, headers=HEADERS).content
    soup = bs(html, 'html.parser')

    data_tour['Nama'] = extract_text(soup.find('div', class_='tourbox').find('h1'))
    data_tour['URL'] = url

    kategori, destinasi, durasi = [e.text for e in soup.find('p', class_='medium').find_all('a', href=True)]
    data_tour['Kategori'], data_tour['Destinasi'], data_tour['Durasi'] = kategori, destinasi, durasi

    harpil_table = soup.find('table', class_='harpil')
    data_tour['Harga'] = extract_harpil(harpil_table, soup)

    itinerary_div = soup.find('div', {'id': 'itinerary'})
    data_tour['Itinerari'] = '\n'.join([e.text for e in itinerary_div.find_all('p', class_='p1')])

    data_tour['Harga Termasuk'], data_tour['Harga Tidak Termasuk'] = extract_price_includes_and_excludes(itinerary_div)

    return data_tour

def main():
    session = requests.Session()
    with open('data_tour_tripsantai.csv', 'w', newline='') as f:
        fieldnames = ['Nama', 'URL', 'Kategori', 'Destinasi', 'Durasi', 'Harga', 'Itinerari', 'Harga Termasuk', 'Harga Tidak Termasuk']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        url = f"{BASE_URL}"
        html = session.get(url, timeout=TIMEOUT, headers=HEADERS).content
        soup = bs(html, 'html.parser')

        for tour_grid in soup.find_all('div', class_='grid'):
            url_ = tour_grid.find('a', href=True)['href']
            try:
                data_tour = fetch_details(session, url_)
                writer.writerow(data_tour)
                f.flush()
            except:
                pass

if __name__ == '__main__':
    main()
