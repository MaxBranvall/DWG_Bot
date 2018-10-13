import csv, scraper

def main():

    xboxOneList = []
    xbox360List = []

    readXboxOne = csv.reader(open(scraper.xboxOneTablePath, 'r'))
    readXbox360 = csv.reader(open(scraper.xbox360TablePath, 'r'))

    for row in readXboxOne:
        xboxOneList.append(row)
    
    for row in readXbox360:
        xbox360List.append(row)

# main()

if __name__ == '__main__':
    main()