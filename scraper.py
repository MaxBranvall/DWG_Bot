import requests, csv
import csvHandler, DWG_BOT
from collections import OrderedDict
from time import time
from bs4 import BeautifulSoup

startTime = time()

date = '2018/10/15'
saleNumber = '136'

xboxOneDictionary = {}
xbox360Dictionary = {}

headerList = []
gameDataList = []
xboxOnePriceList = []
xbox360PriceList = []
removeFromPrice = ['with', 'Xbox', 'Live', 'Gold']

xboxOneTablePath = 'csvAndMarkDown/csvFiles/xboxOneTable.csv'
xbox360TablePath = 'csvAndMarkDown/csvFiles/xbox360Table.csv'
finalXboxOneTablePath = 'csvAndMarkDown/csvFiles/finalXboxOneTable.csv'
finalXbox360TablePath = 'csvAndMarkDown/csvFiles/finalXbox360Table.csv'

header = {'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
testHeader = {'USER-AGENT': 'TestBot'}

majNelsonURL = (f'https://majornelson.com/{date}/this-weeks-deals-with-gold-and-spotlight-sale-{saleNumber}/')
trueAchievementsURL = 'https://www.trueachievements.com/game/'
testUrl = 'html/week3.html'

# Debugging
breakForDebug = 500
debugMode = True


class Utility:

    def clearFile(filePath):
        with open(filePath, 'w'):
            pass

    def requestWebPage(mode=None, href=None):

        if mode == 'getPrice':
            getStorePage = requests.get(href, headers= header)
            storePageSoup = BeautifulSoup(getStorePage.text, 'html5lib')
            return storePageSoup

        else:
            if debugMode == True:
                x = open(testUrl, 'r')
                nelsonSoup = BeautifulSoup(x, 'html5lib')
                return nelsonSoup

            else:
                x = requests.get(majNelsonURL, headers={'USER-AGENT': 'Mozilla 5.0'})
                print(f'Status Code: {x}')
                nelsonSoup = BeautifulSoup(x.text, 'html5lib')
                return nelsonSoup

    def getGamePrice():

        nelsonSoup = Utility.requestWebPage()

        Utility.processAnchorTags(nelsonSoup)
        xboxOneDict, xbox360Dict = Utility.sortDictionaries()

        Utility.getXboxOnePrices(xboxOneDict)
        Utility.getXbox360Prices(xbox360Dict)

        openXboxOne, writeToXboxOne, readFromXboxOne = Utility.xboxOneFiles()
        openXbox360, writeToXbox360, readFromXbox360 = Utility.xbox360Files()

        Utility.addPricesToXboxOneTable(readFromXboxOne, writeToXboxOne)
        Utility.addPricesToXbox360Table(readFromXbox360, writeToXbox360)

        openXboxOne.close()
        openXbox360.close()

    def processAnchorTags(nelsonSoup):

        for anchorTag in nelsonSoup.find_all(['tr', 'td', 'a'], {'rel': 'noopener'}):

            # First few a tags have no text, this skips those
            if anchorTag.text == '':
                pass

            # if the text has been added to the dict, pass, if not, add the game name with its href
            else:

                try:
                    if 'microsoft' in anchorTag['href']:

                        if anchorTag.text not in xboxOneDictionary.keys():

                            try:
                                xboxOneDictionary[anchorTag.text] = anchorTag['href']

                            except KeyError:
                                pass

                    elif 'microsoft' not in anchorTag['href']:

                        if anchorTag.text not in xbox360Dictionary.keys():

                            try:
                                xbox360Dictionary[anchorTag.text] = anchorTag['href']

                            except KeyError:
                                pass

                    else:
                        pass

                # If there is no href for the entry, set it's price to null
                except KeyError:
                    xboxOneDictionary[anchorTag.text] = 'null'

    def sortDictionaries():

        sortedXboxOneDict = OrderedDict(sorted(xboxOneDictionary.items()))
        sortedXbox360Dict = OrderedDict(sorted(xbox360Dictionary.items()))

        return sortedXboxOneDict, sortedXbox360Dict

    def getXboxOnePrices(xboxOneDict):

        debugLoopBreak = 0
        priceIterationNumber = 0

        for game, href in xboxOneDict.items():

            if debugLoopBreak == breakForDebug:
                break

            if href == 'null':
                xboxOnePriceList.append('null')
                print(f'(X1) Retrieved price: {priceIterationNumber}!')

            else:

                storePageSoup = Utility.requestWebPage(mode='getPrice', href=href)

                try:
                    discountedPrice = storePageSoup.find('div', {'class': 'remediation-cta-label'})
                    discountedPrice = discountedPrice.text.split()

                except AttributeError:

                    try:
                        discountedPrice = storePageSoup.find('span', {'class': 'price-disclaimer'})
                        discountedPrice = discountedPrice.find('span').text.split()

                    except AttributeError:
                        discountedPrice = storePageSoup.find('div', {'class': 'pi-price-text'})
                        discountedPrice = discountedPrice.find('span').text.split()

                for keyword in removeFromPrice:
                    if keyword in discountedPrice:
                        discountedPrice.remove(keyword)

                if discountedPrice[0] == 'Included':
                    discountedPrice = storePageSoup.find_all('span', {'class': 'price-disclaimer'})
                    discountedPrice = [discountedPrice[0].text]

                elif discountedPrice[0] == 'Free':
                    try:
                        discountedPrice = storePageSoup.find('div', {'class': 'pi-price-text'})
                        discountedPrice = discountedPrice.find('span').text.split()

                        if discountedPrice == []:
                            raise AttributeError

                    except AttributeError:
                        discountedPrice = storePageSoup.find('span', {'class': 'price-disclaimer'})
                        discountedPrice = discountedPrice.find('span').text.split()

                xboxOnePriceList.append(f'[{discountedPrice[0]}]({href})')
                print(f'(X1) Retrieved price: {priceIterationNumber}!')

            priceIterationNumber += 1
            debugLoopBreak += 1

    def getXbox360Prices(xbox360Dict):

        debugLoopBreak = 0
        priceIterationNumber = 0

        for game, href in xbox360Dict.items():

            if debugLoopBreak == breakForDebug:
                break

            storePageSoup = Utility.requestWebPage(mode='getPrice', href=href)

            try:
                discountedPrice = storePageSoup.find('span', {'class': 'GoldPrice ProductPrice'})
                discountedPrice = discountedPrice.text

            except AttributeError:
                discountedPrice = storePageSoup.find('span', {'class': 'SilverPrice ProductPrice'})
                discountedPrice = discountedPrice.text

            xbox360PriceList.append(f'[{discountedPrice}]({href})')
            print(f'(X360) Retrieved price: {priceIterationNumber}!')

            priceIterationNumber += 1
            debugLoopBreak += 1

    def xboxOneFiles():

        openXboxOne = open(finalXboxOneTablePath, 'w')
        writeToXboxOne = csv.writer(openXboxOne)
        readFromXboxOne = csv.reader(open(xboxOneTablePath, 'r'))

        return openXboxOne, writeToXboxOne, readFromXboxOne

    def xbox360Files():

        openXbox360 = open(finalXbox360TablePath, 'w')
        writeToXbox360 = csv.writer(openXbox360)
        readFromXbox360 = csv.reader(open(xbox360TablePath, 'r'))

        return openXbox360, writeToXbox360, readFromXbox360

    def addPricesToXboxOneTable(readFromXboxOne, writeToXboxOne):

        debugLoopBreak = 0
        lineNumber = 0
        priceIndexNumber = 0

        for line in readFromXboxOne:

            if debugLoopBreak == breakForDebug:
                break

            if lineNumber == 0 or lineNumber == 1: # Skip the first two lines
                pass

            else:
                # For each price in the priceList, assign price to last index of each line
                if xboxOnePriceList[priceIndexNumber] == 'null':
                    pass

                else:
                    line[-1] = xboxOnePriceList[priceIndexNumber]

                priceIndexNumber += 1

            lineNumber += 1
            debugLoopBreak += 1

            writeToXboxOne.writerow(line)

    def addPricesToXbox360Table(readFromXbox360, writeToXbox360):

        debugLoopBreak = 0
        lineNumber = 0
        priceIndexNumber = 0

        for line in readFromXbox360:

            if debugLoopBreak == breakForDebug:
                break

            if lineNumber == 0 or lineNumber == 1:
                pass

            else:
                # For each price in the priceList, assign price to last index of each line
                try:
                    line[-1] = xbox360PriceList[priceIndexNumber]

                except IndexError:
                    break

                priceIndexNumber += 1
            lineNumber += 1
            debugLoopBreak += 1

            writeToXbox360.writerow(line)


class MajorNelsonScrape:

    def __init__(self):

        # Clear files
        Utility.clearFile(xboxOneTablePath)
        Utility.clearFile(xbox360TablePath)

        # Send a request.get to major nelson post
        self.nelsonSoup = Utility.requestWebPage()

        self.writeToXboxOneTable = csv.writer(open(xboxOneTablePath, 'a'))
        self.writeToXbox360Table = csv.writer(open(xbox360TablePath, 'a'))

        self.currentTable = 'Xbox-One'

        self.getTableHeaders()

    def getTableHeaders(self):

        headerNumber = 0

        for row in self.nelsonSoup.find_all('tr'):

            headerList.clear()
            tableHeaders = row.find_all('th')

            for header in tableHeaders:

                # Stops 'Notes' header from being added to the table
                if headerNumber == 3:
                    break

                else:
                    if header.text == 'Discount':
                        headerList.append('Price (USD)')
                    else:
                        headerList.append(header.text)

                headerNumber += 1
            break

        self.getTableContents()

    def getTableContents(self):

        # Initialize xbox one table
        self.writeToXboxOneTable.writerow(['Xbox One Table'])
        self.writeToXboxOneTable.writerow(headerList)

        for row in self.nelsonSoup.find_all('tr')[1:]:

            # Clear list on each iteration to prevent dupe writing
            gameDataList.clear()

            gameData = row.find_all('td')

            # Detects when XboxOne table ends
            if gameData == []:

                self.currentTable = 'Xbox-360'

                self.writeToXboxOneTable.writerow([])

                # Initialize xbox 360 table
                self.writeToXbox360Table.writerow(['Xbox 360 Table'])
                self.writeToXbox360Table.writerow(headerList)

            else:

                itemNumber = 0
                for item in gameData:

                    # Breaks before writing 'Notes' column to list
                    if itemNumber == 3:
                        break

                    else:
                        gameDataList.append(item.text)
                    itemNumber += 1

            self.writeToTable(gameDataList)

    def writeToTable(self, gameData):

        if self.currentTable == 'Xbox-One':
            self.writeToXboxOneTable.writerow(gameData)

        else:
            self.writeToXbox360Table.writerow(gameData)


class TrueAchievementsScrape:
    pass


class HowLongToBeatScrape:
    pass

if __name__ == '__main__':
    MajorNelsonScrape()
    csvHandler.main()
    DWG_BOT.main()
    print(f'\nTime elapsed: {time() - startTime}')
    print('Success!')
