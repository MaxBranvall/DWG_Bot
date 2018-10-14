import requests, csv, csvHandler, csvToMdTable
from bs4 import BeautifulSoup
from lxml import html

headerList = []
gameDataList = []
priceRetrieved = []
priceList = []
removeFromPrice = ['with', 'Xbox', 'Live', 'Gold']

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

        # x = open('rawhtml.html', 'r') #TODO use this to test without making requests
        x = requests.get(majNelsonURL, headers= header)
        print(f'Status Code: {x}')
        nelsonSoup = BeautifulSoup(x.text, 'html.parser')

        i = 0

        for item in nelsonSoup.find_all('a', {'rel': 'noopener'}):

            if i == 3:
                break

            x = item['href']

            if x not in priceRetrieved:
                gameRetrieved = False
                priceRetrieved.append(x)
                print(x)

            else:
                gameRetrieved = True
                pass

            if 'microsoft' not in x:
                if i >= 1:
                    print(True)
                else:
                    print('\n')
                    print(True)
                
                i += 1

            if gameRetrieved == False:

                getBuyPage = requests.get(x, headers= testHeader) #TODO Not testing
                buyPageSoup = BeautifulSoup(getBuyPage.text, 'html.parser') #TODO Not testing

                # x = open('buyHtml.html', 'r')#TODO testing
                # buyPageSoup = BeautifulSoup(x, 'html.parser') #TODO testing

                try:
                    discountedPrice = buyPageSoup.find('div', {'class': 'remediation-cta-label'})
                    discountedPrice = discountedPrice.text.split()

                except AttributeError: #This block is executed if the landing page is different
                    discountedPrice = buyPageSoup.find('span', {'class': 'price-disclaimer'})
                    discountedPrice = discountedPrice.find('span').text.split()

                for item in removeFromPrice:
                    if item in discountedPrice:
                        discountedPrice.remove(item)

                priceList.append(discountedPrice[0])

            else:
                pass

            i += 1

            print(priceList)
            print(priceRetrieved)

        # for item in csv.reader(open(xboxOneTablePath, 'r')):
        #     print(item)


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

class TrueAchievementsScrape:
    pass

class HowLongToBeatScrape:
    pass

if __name__ == '__main__':
    MajorNelsonScrape()
    csvHandler.main()
    csvToMdTable
    print('Success!')


# def getGamePrice(self):

#         i = 0

#         for item in self.nelsonSoup.find_all('a', {'rel': 'noopener'}):

#             if i == 8:
#                 break

#             x = (item['href'])

#             if x not in priceRetrieved:
#                 gameRetrieved = False
#                 priceRetrieved.append(x)
#                 print(x)

#             else:
#                 gameRetrieved = True
#                 pass

#             if 'microsoft' not in x:
#                 if i >= 1:
#                     print(True)
#                 else:
#                     print('\n')
#                     print(True)
                
#                 i += 1
            
#             if gameRetrieved == False:

#                 getBuyPage = requests.get(x, headers= testHeader) #TODO Not testing
#                 buyPageSoup = BeautifulSoup(getBuyPage.text, 'html.parser') #TODO Not testing

#                 # x = open('buyHtml.html', 'r')#TODO testing
#                 # buyPageSoup = BeautifulSoup(x, 'html.parser') #TODO testing

#                 try:
#                     discountedPrice = buyPageSoup.find('div', {'class': 'remediation-cta-label'})
#                     discountedPrice = discountedPrice.text.split()

#                 except AttributeError: #This block is executed if the landing page is different
#                     discountedPrice = buyPageSoup.find('span', {'class': 'price-disclaimer'})
#                     discountedPrice = discountedPrice.find('span').text.split()

#                 for item in removeFromPrice:
#                     if item in discountedPrice:
#                         discountedPrice.remove(item)

#                 print(discountedPrice[0])

#             else:
#                 pass

#             i += 1
