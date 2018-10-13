import csv
import os

csvFile = 'csvAndMarkDown/csvFiles/xboxOneTable.csv'
x360File = 'csvAndMarkDown/csvFiles/xbox360Table.csv'

# csvPath = os.path.dirname(csvFile)
# print(csvPath)

openCsv = csv.reader(open(csvFile, 'r'))
openx360 = csv.reader(open(x360File, 'r'))

newList = []

i = 0

for row in openCsv:
    newList.append(row)
    
# print(newList)

newList1 = []

i = 0

for row in openx360:
    newList1.append(row)


# newList1[2:] = sorted(newList1[2:])

# newList[2:] = sorted(newList[2:])

# testCsv = csv.writer(open('testFile.csv', 'w'))

# for item in newList:
#     testCsv.writerow(item)

# for item in newList1:
#     testCsv.writerow(item)


# testList = ['shadow of the tomb raider', 'black mirror', 'assassins creed', 'rocket league']

# shadowList = ['Shadow of the Tomb Raider*', 'Xbox One X Enhanced', '25%']
# blackList = ['Black Mirror*', 'Xbox One Game', '80%']
# unravelList = ['Unravel Yarny Bundle*', 'Xbox One X Enhanced', '35%']
# nbaList = ['NBA LIVE 19*', 'Xbox One X Enhanced', '33%']
# robocraftList = ['Robocraft Infinity*', 'Xbox One X Enhanced', '60%']

# newList = [shadowList, blackList, unravelList, nbaList, robocraftList]

# newList.sort()

# print(newList)

# FILE = open(csvFile, 'r') # %IN_PATH% would be the path to the file you want to open
# lines = FILE.readlines() #takes the lines from the file and puts each line as its own list object
# FILE.close() #closes the file to prevent corruption
# ordered_lines = sorted(lines) #sorts the lines alphanumerically
# FILE = open("testTest.csv", 'w') #opens file to output sorted version to
# for i in range(len(ordered_lines)):
#     FILE.write(ordered_lines[i])
# FILE.close()