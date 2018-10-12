import requests
from lxml import html
import praw
import scraper

redditInstance = praw.Reddit('dwgBot')

testSub = redditInstance.subreddit('test')

# scraper.main()

print(redditInstance.user.me())

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
