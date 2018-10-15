import requests
from lxml import html
import praw
import scraper

def main():

    markdownPath = 'csvAndMarkDown/markDownFiles/testFinish.md'

    with open(markdownPath, 'r') as x:
        content = x.read()

    redditInstance = praw.Reddit('dwgBot')

    testSub = redditInstance.subreddit('test')

    # scraper.main()

    print(redditInstance.user.me())

    testSub.submit('TestPost', selftext= content)

# main()
