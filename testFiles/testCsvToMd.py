import csv
import csvToMdTable

csvFile = 'csvTable.csv'
csvRead = csv.reader(open(csvFile, 'r'))
mdFile = 'mdTest.md'

mdOpen = open(mdFile, 'w')

i = 0

for row in csvRead:

    print(row)

mdOpen.close()
# csvRead.close()

# csvToMdTable.main(csvFile)

