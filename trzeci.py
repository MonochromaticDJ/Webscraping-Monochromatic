import requests
from bs4 import BeautifulSoup

url = 'https://www.cyberport.de/apple-und-zubehoer/apple-iphone.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

product_articles = soup.find_all('article', class_='productArticle')

for article in product_articles:
    name = article.find('a', class_='productLink').text.strip()
    price = article.find('div', class_='price').text.strip()

    print(f"Name: {name}\nPrice: {price}\n")


 