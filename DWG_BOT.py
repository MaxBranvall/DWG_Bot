import requests
from lxml import html
import praw

majNelsonURL = 'https://majornelson.com/2018/10/08/this-weeks-deals-with-gold-and-spotlight-sale-135/'

header = { 
    'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}

redditInstance = praw.Reddit('dwgBot')

testSub = redditInstance.subreddit('test')

# testSub.submit('FormatTest2', selftext= '**This is bold**, *These are italics*,\
# `this is inline code`,\
# Col1 | Col2\n\
# ---|---\n\
# row | row')

# for sub in testSub.stream.submissions():
#     if sub.title == 'FormatTest2':
#         sub.reply('col1 | col2\n\
# ---|---\n\
# row | row')
#         break

# majorNelsonSite = requests.get(majNelsonURL, headers= header)
# majorNelsonSiteContent = html.fromstring(majorNelsonSite.content)

# title = majorNelsonSiteContent.xpath('//*[@id="post-36186"]/header/div[1]/h1/text()')

# print(title[0])

print(redditInstance.user.me())
# print(redditInstance.read_only)
