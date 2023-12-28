import requests
from bs4 import BeautifulSoup
import csv
import random

# Load proxy list from proxy_list.csv
'''def load_proxies():
    proxies = []
    with open('proxy_list.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            proxies.append({'http': f'http://{row[0]}', 'https': f'https://{row[0]}'})
    return proxies'''

#load proxy list from website
def load_proxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text == 'elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
    return proxies

# Check the validity of proxies by making a request to https://httpbin.org/ip and print working proxies
def check_proxies(proxies):
    working_proxies = []
    for proxy in proxies:
        try:
            response = requests.get('https://httpbin.org/ip', proxies=proxy, timeout=5)
            if response.ok:
                working_proxies.append(proxy)
                print(proxy)
        except:
            pass
    return working_proxies

# Function to scrape Amazon with a random proxy
def scrape_with_proxy(url, headers, working_proxies):
    random_proxy = random.choice(working_proxies)
    try:
        response = requests.get(url, headers=headers, proxies=random_proxy)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# web scraping code to find product title, price and weight.
def scrape_amazon(url, headers):
    html = scrape_with_proxy(url, headers, working_proxies)
    if not html:
        return None

    soup = BeautifulSoup(html, 'html.parser')

    # Extracting product title
    try:
        title = soup.find('span', id='productTitle').get_text(strip=True)
        print("Title:", title)
    except:
        print("Title not found.")

    # Extracting product price
    try:
        price = soup.find("span", class_="a-price-whole").get_text(strip=True)
        print("Price:", price)
    except:
        print("Price not found.")

    # Extracting product weight
    try:
        weight = soup.find('div', id='prodDetails').find(lambda tag: tag.name == 'tr' and 'Item Weight' in tag.text).get_text(strip=True)
        print("Weight:", weight)
    except AttributeError:
        try:
            weight = soup.find('div', id='detailBullets_feature_div').find(lambda tag: tag.name == 'li' and 'Item Weight' in tag.text).get_text(strip=True)
            weight = weight.strip().replace('\n', '').replace(' ', '')
            print("Weight:", weight)
        except:
            print("Weight not found.")

# Main program
url = "https://www.amazon.in/gp/product/B09WQDGZPB/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&th=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}

proxies = load_proxies()
working_proxies = check_proxies(proxies)

if working_proxies:
    scrape_amazon(url, headers)
else:
    print("No working proxies available.")
