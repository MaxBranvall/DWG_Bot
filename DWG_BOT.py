import requests
from lxml import html
import praw
import scraper

def main():

    mdTablePath = 'csvAndMarkDown/markDownFiles/markdownTable.md'
    endOfPostPath = 'csvAndMarkDown/markDownFiles/endOfPost.md'

    with open(mdTablePath, 'r') as x:
        mainPost = x.read()

    with open(endOfPostPath, 'r') as x:
        ending = x.read()

    redditInstance = praw.Reddit('dwgBot')

    testSub = redditInstance.subreddit('XboxOne')

    testSub.submit('This Weeks Deals with Gold and Spotlight Sale! Formatted for Easy Reading!', selftext= mainPost + ending)
    print('\nSubmitted!')

if __name__ == '__main__':
    main()