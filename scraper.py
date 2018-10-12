import requests, csv
from bs4 import BeautifulSoup
from lxml import html

headerList = []
gameDataList = []
xboxOneTablePath = 'xboxOneTable.csv'
xbox360TablePath = 'xbox360Table.csv'

header = { 
    'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}

testHeader = {
    'USER-AGENT' : 'TestBot'
}

majNelsonURL = 'https://majornelson.com/2018/10/08/this-weeks-deals-with-gold-and-spotlight-sale-135/'
trueAchievementsURL = 'https://www.trueachievements.com/game/'

class Utility:

    def clearFile(self, filePath):
        with open(filePath, 'w') as foo:
            pass

class MajorNelsonScrape(Utility):

    def __init__(self):

        self.clearFile(xboxOneTablePath)
        self.clearFile(xbox360TablePath)

        x = open('rawhtml.html', 'r')
        self.nelsonSoup = BeautifulSoup(x, 'html.parser')
        tableTitles = self.nelsonSoup.find_all('h4')

        self.writeToXboxOneTable = csv.writer(open(xboxOneTablePath, 'a'))
        self.writeToXbox360Table = csv.writer(open(xbox360TablePath, 'a'))
        self.xOneTableTitle = tableTitles[0].text
        self.x360TableTitle = tableTitles[1].text

        self.getTableHeaders()

    def getTableHeaders(self):
        
        for data in self.nelsonSoup.find_all('tr'):

            headerList.clear()
            tableHeader = data.find_all('th')

            if tableHeader == []:
                continue

            else:

                i = 0
                for item in tableHeader:

                    if i == 3:
                        break
                    else:
                        headerList.append(item.text)
                    i += 1
            break

        self.getTableContents()

    def getTableContents(self):

        num = 0
        currentTable = 'Xbox-One'

        self.writeToXboxOneTable.writerow(['Xbox One Table'])
        self.writeToXboxOneTable.writerow(headerList)
        
        for data in self.nelsonSoup.find_all('tr')[1:]:

            try:
                if num == 100:
                    break

            except IndexError:
                break

            gameDataList.clear()

            gameData = data.find_all('td')

            if gameData == []:
                print('End of Xbox One Deals')
                self.writeToXboxOneTable.writerow([])

                self.writeToXbox360Table.writerow(['Xbox 360 Table'])
                self.writeToXbox360Table.writerow(headerList)
                currentTable = 'Xbox-360'

            else:

                i = 0
                for item in gameData:

                    if i == 3:
                        break
                    else:
                        gameDataList.append(item.text)
                    i += 1
            
            if gameDataList == []:
                continue

            else:
                if currentTable == 'Xbox-One':
                    self.writeToXboxOneTable.writerow(gameDataList)
                
                elif currentTable == 'Xbox-360':
                    self.writeToXbox360Table.writerow(gameDataList)

            num += 1

class TrueAchievementsScrape:
    pass

class HowLongToBeatScrape:
    pass

if __name__ == '__main__':
    MajorNelsonScrape()
    print('Success!')
