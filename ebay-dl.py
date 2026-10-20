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
        
        html = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'}, timeout=10)
        print('status: ', html.status_code)
        with open (args.search + str(pg_num) + '.html', 'wb') as f:
            f.write(html.content)
        print('Saved', args.search + str(pg_num) + '.html')


def select_texts(html, selector):
    result = None
    soup = BeautifulSoup(html, 'html.parser')
    for selected in soup.select(selector):
        result = selected.text
    return result


def extract_prices_cents(html, selector):
    soup = BeautifulSoup(html, 'html.parser')
    price = ''
    for selected in soup.select(selector):
        print('\ninput str:', selected.text)
        if selected.text == 'Free shipping':
             price = 0
             print('free returns price:', 0)
             return price
        elif selected.text.find(' ') != -1:
                text = selected.text[:selected.text.find(' ')]
                print('sliced text:', text)
        else:
                text = selected.text

        for char in 'qwertyuiopasdfghjklzxcvbnm,$+-= ':
            text = text.replace(char, '')
        price = text
        #if type(text) == str:
            #for char in text:
                #if char in '.1234567890':
                    #price += char
            #print('price str:', price)
        #else:
            #price = text
        try:
            price = int(float(price) * 100)
            print('price int:', price)
        except ValueError:
            print('incorrectly formatted input')
            return('input: ', selected.text ,' output: ', price)
        if price:
            return price
    price = None
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
    else:
        download_page(pg_num)
        file = args.search + str(pg_num) + '.html'
    with open (file, encoding='utf-8') as f:
        html = f.read()
    listings = listings + process_html(html)

with open(args.search + '.json', 'w', encoding='utf-8') as f:
    json.dump(listings, f, indent=2)
    print('Saved ' + args.search + '.json')

