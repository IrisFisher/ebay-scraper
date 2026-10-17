import argparse
import requests
import json
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
parser.add_argument('search')
parser.add_argument('--pages_dir')
args = parser.parse_args()


def download_page(pg_num):
        # build url
        url = 'https://www.ebay.com/sch/i.html?_nkw=' + args.search + '&_sacat=0&_from=R40&_pgn=' + str(pg_num)
        
        response = requests.get(url, timeout=10)
        print('status: ', response.status_code)
        return response.text


def select_texts(html, selector):
    result = None
    soup = BeautifulSoup(html, 'html.parser')
    for selected in soup.select(selector):
        result = selected.text
    return result


def extract_prices_cents(html, selector):
    soup = BeautifulSoup(html, 'html.parser')
    price = None
    for selected in soup.select(selector):
        if selected.text == 'Free shipping':
             price = 0
        else:
            if selected.text.find('$') != -1:
                if selected.text.find(' ') != -1:
                    price = selected.text[1:selected.text.find(' ')]
                else:
                    price = selected.text[1:]
                try:
                    price = int(float(price)*100)
                except ValueError:
                    print('incorrectly formatted input, skipping value, listing price as None')
                    return price
    return price


def free_returns(html):
    result = None
    soup = BeautifulSoup(html, 'html.parser')
    for selected in soup.select('.s-item__free-returns'):
        if selected.text == 'Free returns':
             result = True
        if selected.text == 'Buyer pays return shipping':
             result = False
    return result

def extract_items_sold(html):
    soup = BeautifulSoup(html, 'html.parser')
    price = None
    for selected in soup.select('.s-item__hotness'):
        price = selected.text[0:selected.text.find(' ')]
        price = int(price)
    return price

def process_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    result = []

    for item in soup.select('.s-item'):
        item=str(item)
        result.append({'name': (select_texts(item,'.s-item__title')), 
                       'price': (extract_prices_cents(item, '.s-item__price')),
                       'status': (select_texts(item,'.SECONDARY_INFO')),
                       'shipping': (extract_prices_cents(item, '.s-item__shipping')),
                       'free_returns': (free_returns(item)),
                       'items_sold': (extract_items_sold(item))})
    return result

listings=[]

for pg_num in range(1, 11):
    if args.pages_dir:
        file = 'practice-pages/page-' + str(pg_num) + '.html'
        with open (file, encoding='utf-8') as f:
            html = f.read()
    else:
        html = download_page(pg_num)
        print(html)
    listings = listings + process_html(html)

with open(args.search + '.json', 'w', encoding='utf-8') as f:
    json.dump(listings, f, indent=2)
    print('Saved ' + args.search + '.json')

