import csv, scraper, csvToMdTable

openXboxOne = open(scraper.xboxOneTablePath, 'w')
openXbox360 = open(scraper.xbox360TablePath, 'w')

writeToXboxOne = csv.writer(openXboxOne)
writeToXbox360 = csv.writer(openXbox360)

def main():

    xboxOneList = []
    xbox360List = []

    readXboxOne = csv.reader(open(scraper.xboxOneTablePath, 'r'))
    readXbox360 = csv.reader(open(scraper.xbox360TablePath, 'r'))

    for row in readXboxOne:
        xboxOneList.append(row)
    
    for row in readXbox360:
        xbox360List.append(row)

    scraper.Utility.getGamePrice()
    sortLists(xboxOneList, xbox360List)

def sortLists(xOneList, x360List):

    xOneList[2:] = sorted(xOneList[2:])
    x360List[2:] = sorted(x360List[2:])

    scraper.Utility.clearFile(scraper.xboxOneTablePath)
    scraper.Utility.clearFile(scraper.xbox360TablePath)

    for line in xOneList:
        if line == []:
            pass
        else:
            writeToXboxOne.writerow(line)

    for line in x360List:
        if line == []:
            pass
        else:
            writeToXbox360.writerow(line)

    openXboxOne.close()
    openXbox360.close()

    csvToMdTable.main()
    # scraper.MajorNelsonScrape.getGamePrice()

if __name__ == '__main__':
    main()