import csv
import scraper
from datetime import datetime

def main(mdFile=None):

    readXboxOne = csv.reader(open(scraper.finalXboxOneTablePath, 'r'))
    readXbox360 = csv.reader(open(scraper.finalXbox360TablePath, 'r'))
    now = datetime.now()

    # Create a markDown file if none is specified
    if mdFile == 'createNew':

        mdFileName = (f'{now.hour - 12}:{now.minute}.{now.second}.md')
        mdFilePath = (f'csvAndMarkDown/markDownFiles/testFinish.md')
        with open(mdFilePath, 'w'):
            pass
    
    else:
        mdFileName = ('markdownTable.md')
        mdFilePath = (f'csvAndMarkDown/markDownFiles/{mdFileName}')
        with open(mdFilePath, 'w'):
            pass

    horizontal = '---|------|---\n'

    with open(mdFilePath, 'w') as mdTable:

        line = 0
    
        for row in readXboxOne:

            try:
                mdTable.write(f'{row[0]} | {row[1]} | {row[2]}\n')

                if line == 1:
                    mdTable.write(horizontal)
            
            # This will be run for the title of the table
            except IndexError:
                mdTable.write(f'\n{row[0]}\n\n')

            line += 1
        
        line = 0

        for row in readXbox360:

            if line == 0:
                mdTable.write('-')

            try:
                mdTable.write(f'{row[0]} | {row[1]} | {row[2]}\n')

                if line == 1:
                    mdTable.write(horizontal)
            
            # Run for the title of the table
            except IndexError:
                mdTable.write(f'\n{row[0]}\n\n')

            line += 1

if __name__ == '__main__':
    main()