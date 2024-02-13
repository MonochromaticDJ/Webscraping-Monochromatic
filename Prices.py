import requests
from bs4 import BeautifulSoup

baseurl = 'https://www.sklepmuzycznydemo.pl/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

productlinks = set()

for x in range (1,4):
    r = requests.get(f'https://www.cyberport.de/apple-und-zubehoer/apple-iphone.html{x}')
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all('div', class_='product col-xs-12 col-sm-4')
    for product in productlist:
        for link in product.find_all('a', href=True):
            productlinks.add(baseurl+link['href'])
productlinks = list(productlinks)


saxophones_list = []

for link in productlinks: 
    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')

    name = soup.find('h1', itemprop="name").text.strip()
    price = soup.find('span', id="st_product_options-price-brutto").text.strip()

    saxophones = {
        'name': name,
        'price': price,
    }
    saxophones_list.append(saxophones)
    print(saxophones)

 