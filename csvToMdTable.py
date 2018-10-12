import csv

def main(csvFile, mdFile=None):

    i = 0

    if mdFile == None:
        mdFileName = ('untitledTable.md')
        with open(mdFileName, 'w'):
            pass

    horizontal = '\n---|------|---'

    newFile = csv.reader(open(csvFile, 'r'))

    with open(mdFileName, 'w') as foo:
        for row in newFile:

            if i == 33:
                break

            gameRow = (f'\n{row[0]} | {row[1]} | {row[2]}')

            foo.write(gameRow)

            if i == 0:
                foo.write(horizontal)
            i += 1
