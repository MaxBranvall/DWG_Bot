import requests
import praw

def main():

    mdTablePath = 'csvAndMarkDown/markDownFiles/markdownTable.md'
    endOfPostPath = 'csvAndMarkDown/markDownFiles/endOfPost.md'

    with open(mdTablePath, 'r') as x:
        mainPost = x.read()

    with open(endOfPostPath, 'r') as x:
        ending = x.read()

    redditInstance = praw.Reddit('dwgBot')

    testSub = redditInstance.subreddit('Test')

    testSub.submit('This is a test run!', selftext= mainPost + ending)
    print('\nSubmitted!')

if __name__ == '__main__':
    main()