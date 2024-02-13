import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

baseurl = 'https://www.otto.de/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

productlinks = set()

r = requests.get(f'https://www.otto.de/technik/apple/iphone/')
soup = BeautifulSoup(r.content, 'lxml')
productlist = soup.find_all('article', class_='product js_find_colorChange')
for product in productlist:
    for link in product.find_all('a', href=True):
        productlink = urljoin(baseurl, link['href'])
        productlinks.add(productlink)

productlinks = list(productlinks)

saxophones_list = []

for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    # Find the product name
    name = soup.find('p', class_="find_tile__brand")

    # Find the product price
    price = soup.find('div', class_="pdp_price__price pl_mt100 js_pdp_price__price")
 

    saxophones = {
        'name': name,
        'price': price,
    }
    saxophones_list.append(saxophones)
    print(saxophones)
