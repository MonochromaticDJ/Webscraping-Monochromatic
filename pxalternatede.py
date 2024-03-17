import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

baseurl = 'https://www.alternate.de'
product_links = set()
total_pages = 10

# Dictionary to store product details with links
products_data = []

# Iterate through pages to collect product links
for x in range(1, total_pages + 1):
    url = f'https://www.alternate.de/Apple-Smartphone?page={x}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all("div", class_="grid-container listing")
    for product in productlist:
        for link in product.find_all('a', href=True):
            product_links.add(link['href'])
            
            
# Iterate through product links and fetch product details
for link in product_links:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    name = soup.find('div', class_="product-name").text.strip()
    price = soup.find('div', class_="col-12 col-md-auto").text.replace('\\', '').replace('\n', '').strip()

    # Add product details to the list of dictionaries
    product_info = {
        'name': name,
        'price': price,
        'link': link  # Include the link if needed
    }
    products_data.append(product_info)

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(products_data)

# Save DataFrame to Excel file
df.to_excel('iphonessalternate1.xlsx', index=False)
