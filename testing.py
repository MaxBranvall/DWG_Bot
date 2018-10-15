from lxml import html
from bs4 import BeautifulSoup

mdTablePath = 'csvAndMarkDown/markDownFiles/testFinish.md'
endOfPostPath = 'csvAndMarkDown/markDownFiles/endOfPost.md'

with open(mdTablePath, 'r') as x:
    mainPost = x.read()

with open(endOfPostPath, 'r') as x:
    ending = x.read()

print(mainPost + ending)