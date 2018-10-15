from lxml import html
from bs4 import BeautifulSoup

qwer = 'x360store.html'

url = open('x360store.html', 'r')

x = BeautifulSoup(url, 'html.parser')

# foo = x.xpath('//*[@id="gameDetails"]/h1/text()')

foo = x.find('span', {'class': 'GoldPrice ProductPrice'})

print(foo)

# openUrl.close()