import csv
import requests
from lxml import html


header = { 
    'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}
csvFile = 'csvTable.csv'
trueAchievementsURL = 'https://www.trueachievements.com/game/'

csvRead = csv.reader(open(csvFile, 'r'))

for row in csvRead:

    try:
        if row[0] == 'Content Title':
            pass
        
        elif row[0] == 'Xbox One Table':
            pass

        else:
            gameSplit = row[0].split()
            print(gameSplit)
            gameJoin = '-'.join(gameSplit)
            print(gameJoin)

            if '*' in gameJoin:
                print('yes')
                gameJoin = gameJoin.strip('*')
                # print(gameJoin)

            taURL = trueAchievementsURL + gameJoin
            print(taURL)

            TAreq = requests.get(taURL, headers= header)
            x = html.fromstring(TAreq.content)

            y = x.xpath('//*[@id="sidebar"]/div[2]/div[2]/div[1]/div/div[1]/text()')
            print(y[0])

            foo = x.xpath('//*[@id="sidebar"]/div[2]/div[2]/div[1]/div/div[3]/text()')
            print(foo[0])

            break
    except IndexError:
        print()
        pass
