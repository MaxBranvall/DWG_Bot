import csv
from datetime import datetime

def main(mdFile=None):

    xboxOneTablePath = 'csvAndMarkDown/csvFiles/xboxOneTable.csv'
    xbox360TablePath = 'csvAndMarkDown/csvFiles/xbox360Table.csv'

    readXboxOne = csv.reader(open(xboxOneTablePath, 'r'))
    readXbox360 = csv.reader(open(xbox360TablePath, 'r'))
    now = datetime.now()

    # Create a markDown file if none is specified
    if mdFile == None:
        mdFileName = (f'{now.hour - 12}:{now.minute}.{now.second}.md')
        mdFilePath = (f'csvAndMarkDown/markDownFiles/{mdFileName}')
        with open(mdFilePath, 'w'):
            pass

    i = 0

    horizontal = '---|------|---\n'

    with open(mdFilePath, 'w') as foo:
        for row in readXboxOne:

            try:
                foo.write(f'{row[0]} | {row[1]} | {row[2]}\n')

                if i == 1:
                    foo.write(horizontal)
            
            except IndexError:
                foo.write(f'{row[0]}\n\n')

            i += 1
        
        i = 0

        for row in readXbox360:

            try:
                foo.write(f'{row[0]} | {row[1]} | {row[2]}\n')

                if i == 1:
                    foo.write(horizontal)
            
            except IndexError:
                foo.write(f'{row[0]}\n\n')

            i += 1
            

main()