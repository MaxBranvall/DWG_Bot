import requests, csv, csvHandler, csvToMdTable
from collections import OrderedDict
from bs4 import BeautifulSoup
from lxml import html

# Games now get put in a dictionary with the key being the title and value being the href. Get hrefs from there

headerList = []
gameDataList = []
priceRetrievedXboxOne = []
priceRetrievedXbox360 = []
priceList = []
removeFromPrice = ['with', 'Xbox', 'Live', 'Gold']

breakLoop = 0

xboxOneDictionary = {}
xbox360Dictionary = {}

gameRetrieved = False
xboxOneTablePath = 'csvAndMarkDown/csvFiles/xboxOneTable.csv'
xbox360TablePath = 'csvAndMarkDown/csvFiles/xbox360Table.csv'

header = { 
    'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}

testHeader = {
    'USER-AGENT' : 'TestBot'
}

majNelsonURL = 'https://majornelson.com/2018/10/08/this-weeks-deals-with-gold-and-spotlight-sale-135/'
trueAchievementsURL = 'https://www.trueachievements.com/game/'

class Utility:

    def clearFile(filePath):
        with open(filePath, 'w') as foo:
            pass

    def getGamePrice():

        x = open('rawhtml.html', 'r') #TODO use this to test without making requests
        # x = requests.get(majNelsonURL, headers= {'USER-AGENT': 'Mozilla 5.0'})
        # print(f'Status Code: {x}')
        nelsonSoup = BeautifulSoup(x, 'html.parser')

        i = 0

        for item in nelsonSoup.find_all(['tr', 'td', 'a'], {'rel': 'noopener'}):

            if i == 100:
                break

            if item.text == '':
                pass
            else:
                if item.text not in xboxOneDictionary.keys():
                    xboxOneDictionary[item.text] = item['href']
                else:
                    pass

        for k, v in xboxOneDictionary.items():
            if 'microsoft' not in v:
                gameRetrieved = False
                xbox360Dictionary[k] = v

        for k in xbox360Dictionary.keys():
            if k in xboxOneDictionary:
                del xboxOneDictionary[k]
                
        sortedXboxOneDict = OrderedDict(sorted(xboxOneDictionary.items()))
        sortedXbox360Dict = OrderedDict(sorted(xbox360Dictionary.items()))

        breakLoop = 0
        iterationNumber = 0

        for game, href in sortedXboxOneDict.items():

            if breakLoop == 1:
                break
            
            getStorePage = requests.get(href, headers= header)
            storePageSoup = BeautifulSoup(getStorePage.text, 'html.parser')

            try:
                discountedPrice = storePageSoup.find('div', {'class': 'remediation-cta-label'})
                discountedPrice = discountedPrice.text.split()

            except AttributeError:
                discountedPrice = storePageSoup.find('span', {'class': 'price-disclaimer'})
                discountedPrice = discountedPrice.find('span').text.split()

            for keyword in removeFromPrice:
                if keyword in discountedPrice:
                    discountedPrice.remove(keyword) 

            priceList.append(discountedPrice[0])
            print(f'Retrieved price: {iterationNumber}!')

            iterationNumber += 1
            breakLoop += 1

        print(priceList)

class MajorNelsonScrape(Utility):

    def __init__(self):

        Utility.clearFile(xboxOneTablePath)
        Utility.clearFile(xbox360TablePath)

        x = open('rawhtml.html', 'r') #TODO use this to test without making requests
        # x = requests.get(majNelsonURL, headers= header)
        # print(f'Status Code: {x}')
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
        
        # csvHandler.main()

class TrueAchievementsScrape:
    pass

class HowLongToBeatScrape:
    pass

if __name__ == '__main__':
    MajorNelsonScrape()
    csvHandler.main()
    print('Success!')
