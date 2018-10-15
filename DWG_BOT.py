import requests
from lxml import html
import praw
import scraper

def main():

    mdTablePath = 'csvAndMarkDown/markDownFiles/testFinish.md'
    endOfPostPath = 'csvAndMarkDown/markDownFiles/endOfPost.md'

    with open(mdTablePath, 'r') as x:
        mainPost = x.read()

    with open(endOfPostPath, 'r') as x:
        ending = x.read()

    redditInstance = praw.Reddit('dwgBot')

    testSub = redditInstance.subreddit('test')

    testSub.submit('Final Test', selftext= mainPost + ending)
    print('\nSubmitted!')
