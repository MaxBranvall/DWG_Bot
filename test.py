from bs4 import BeautifulSoup
import html5lib
import lxml

url = 'fallout4Store.html'
url = open(url, 'r')

soup = BeautifulSoup(url, 'html5lib')

discountedPrice = soup.find('div', {'class': 'remediation-cta-label'})
discountedPrice = discountedPrice.text.split()

price = soup.find_all('span', {'class': 'price-disclaimer'})

price = [price[0].text]

print(price)