import requests, csv
import csvHandler, DWG_BOT
from collections import OrderedDict
from time import time
from bs4 import BeautifulSoup

startTime = time()

bundle = False

date = '2018/11/05'
saleNumber = '138'

xboxOneDictionary = {}
xboxOneBundledDict = {}
xbox360Dictionary = {}

headerList = []
gameDataList = []
xboxOnePriceList = []
xbox360PriceList = []
removeFromPrice = ['with', 'Xbox', 'Live', 'Gold']

xboxOneBundleTablePath = 'csvAndMarkDown/csvFiles/xboxOneBundleTable.csv'
# xbox360BundleTablePath = 'csvAndMarkDown/csvFiles/xbox360BundleTable.csv'

xboxOneTablePath = 'csvAndMarkDown/csvFiles/xboxOneTable.csv'
xbox360TablePath = 'csvAndMarkDown/csvFiles/xbox360Table.csv'

finalXboxOneTablePath = 'csvAndMarkDown/csvFiles/finalXboxOneTable.csv'
finalXbox360TablePath = 'csvAndMarkDown/csvFiles/finalXbox360Table.csv'

header = {'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
testHeader = {'USER-AGENT': 'TestBot'}

majNelsonURL = (f'https://majornelson.com/{date}/this-weeks-deals-with-gold-and-spotlight-sale-{saleNumber}/')
trueAchievementsURL = 'https://www.trueachievements.com/game/'
testUrl = 'html/week5.html'

# Debugging
breakForDebug = 10
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

        openXboxOne, writeToXboxOne, readFromXboxOne, readFromBundledXboxOne = Utility.xboxOneFiles()
        openXbox360, writeToXbox360, readFromXbox360 = Utility.xbox360Files()

        xboxOneBundledDict = Utility.handleXboxOneBundle(readFromXboxOne, xboxOneDict)

        Utility.getXboxOnePrices(xboxOneBundledDict)
        Utility.getXbox360Prices(xbox360Dict)

        Utility.addPricesToXboxOneTable(readFromBundledXboxOne, writeToXboxOne)
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

        print('Xbox One')
        print(len(sortedXboxOneDict.keys()))
        print('Xbox 360')
        print(len(sortedXbox360Dict.keys()))

        return sortedXboxOneDict, sortedXbox360Dict

    def checkIfBundle(soup):

        headings = soup.find_all('h2', {'class': 'c-heading-4'})

        n = 0

        for head in headings:
            if (head.text.split() == ['In', 'this', 'bundle']):
                print('bundle')
                return True
            elif(n > 2 and head.text.split() != ['In', 'this', 'bundle']):
                return False

            n += 1

    def handleXboxOneBundle(readFromXboxOne, xboxOneDict):

        lines = list(readFromXboxOne)
        openBTable = open(xboxOneBundleTablePath, 'w')
        writeToBundleTable = csv.writer(openBTable)
        lineNumber = 2
        debugLoopBreak = 0
        xboxOneBundledDict = {}

        writeToBundleTable.writerow(lines[0])
        writeToBundleTable.writerow(lines[1])

        for game, href in xboxOneDict.items():

            if debugLoopBreak == breakForDebug:
                break

            getStorePage = requests.get(href, headers=header)
            storePageSoup = BeautifulSoup(getStorePage.content, 'html5lib')

            bundle = Utility.checkIfBundle(storePageSoup)

            if bundle == True:
                writeToBundleTable.writerow([f'{game} ~ Bundle includes: ', f'{lines[lineNumber][1]}', f'{lines[lineNumber][2]}'])
                xboxOneBundledDict[game] = href

                for num in range(1000): # this gets all the bundled titles

                    try:
                        y = storePageSoup.find_all('div', {'id': f'pdpbundleparts_{num}'})

                        try:
                            title = y[0].find_all('h3')[0].text
                            writeToBundleTable.writerow([f'~ {title}', 'Bundled', 'null'])

                            if (f'~ {title}' in xboxOneBundledDict.keys()):
                                xboxOneBundledDict[f'~~ {title}'] = 'bundled'
                            else:
                                xboxOneBundledDict[f'~ {title}'] = 'bundled'

                        except IndexError:
                            break

                    except KeyError:
                        break

            else:
                writeToBundleTable.writerow([f'{game}', f'{lines[lineNumber][1]}', f'{lines[lineNumber][2]}'])
                xboxOneBundledDict[game] = href

            print(lineNumber, game)
            debugLoopBreak += 1
            lineNumber += 1

        openBTable.close()
        return xboxOneBundledDict

    def getXboxOnePrices(xboxOneDict):

        debugLoopBreak = 0
        priceIterationNumber = 0

        for game, href in xboxOneDict.items():

            if debugLoopBreak == breakForDebug:
                break

            if href == 'null':
                xboxOnePriceList.append('null')
                print(f'(X1) Retrieved price: {priceIterationNumber}!')

            elif href == 'bundled':
                xboxOnePriceList.append('bundled')
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
            print(discountedPrice)
            print(f'(X360) Retrieved price: {priceIterationNumber}!')

            priceIterationNumber += 1
            debugLoopBreak += 1

    def xboxOneFiles():

        openXboxOne = open(finalXboxOneTablePath, 'w')
        writeToXboxOne = csv.writer(openXboxOne)
        readFromXboxOne = csv.reader(open(xboxOneTablePath, 'r'))
        readFromBundledXboxOne = csv.reader(open(xboxOneBundleTablePath, 'r'))

        return openXboxOne, writeToXboxOne, readFromXboxOne, readFromBundledXboxOne

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
                if xboxOnePriceList[priceIndexNumber] == 'null' or xboxOnePriceList[priceIndexNumber] == 'bundled':
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

class MetaCriticScrape:
    pass

if __name__ == '__main__':
    MajorNelsonScrape()
    csvHandler.main()
    # DWG_BOT.main()
    endTime = time()
    endTime = (float(f'{(endTime - startTime) / 60}'))
    print(f'\nTime elapsed: {endTime:.2f}')
    print('Success!')
