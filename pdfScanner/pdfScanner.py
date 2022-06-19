# -*- coding: utf-8 -*-
import os
import fitz
import re

def main():
    pdfDocPath, dataTextPath = getPath()
    pdfToTextConv(pdfDocPath, dataTextPath)
    parserData(dataTextPath)
    


def getPath():
    '''
    Getting the full path to the PDF file to parse
    and to the txt file which contains the data of PDF
    Return tuple:
    :return: pdfDocPath, dataTextPath
    '''
    # Gets the path to script file
    progName = os.path.basename(__file__)
    progPath = os.path.abspath(__file__).replace(progName, '')
    # path to PDF file (in the same with the script directory)
    pdfDocPath = progPath + 'Document-2022-05-16-192805.pdf'
    # path to txt file (in the same with the script directory)
    dataTextPath = progPath + 'dataText.txt'
    return pdfDocPath, dataTextPath


def pdfToTextConv(pdfPath : str ,textPath : str):
    '''
    This function gets the two path. 
    First path - to the PDF file which to be converted
    Second path - to the txt file wich contains the data from PDF
    '''
    try:
        # Saved open the PDF
        with fitz.open(pdfPath) as pdf: 
            # Open txt file to writing
            txtHandle = open(textPath, "wb")
            # List of data from PDF
            allText = []
            # Circule of getting the data
            for numPage in range(len(pdf)):
                page = pdf.load_page(numPage)
                allText.append(page.get_text().encode('utf-8'))
                txtHandle.write(allText[numPage])
    except:
        print('Oh no! PDF to txt conversion is failed.')
    
    else:
        print('Sucssesful! PDF to txt conversion completed.')


def parserData(textPath : str):
    '''
    This function open txt file with data extracted from PDF
    and allocate this into categories.
    Income:
        Wages
        Grants
        Other profit
    Expense:
        Food:
            Restoraunts
            Delivery
            Grocer
        Sport:
            Trainings
            Equipment
        Technique:
        Clothes:
    '''
    data = {'Income' : {'Wages' : {'pattern' : '',
                                   'value' : 0},

                        'Grants' : {'pattern' : '',
                                    'value' : 0},

                        'OtherProfit' : {'pattern' : '',
                                         'value' : 0},

                        'Summary' : {'pattern' : '',
                                     'value' : 0},},

            'Expense' : {'Food' : {'Restoraunts' : {'pattern' : '',
                                                    'value' : 0},

                                   'Delivery' : {'pattern' : '',
                                                 'value' : 0},

                                   'Grocer' : {'pattern' : '',
                                               'value' : 0},},

                         'Sport' : {'Trainings' : {'pattern' : '',
                                                   'value' : 0},

                                    'Equipment' : {'pattern' : '',
                                                    'value' : 0},},

                         'Technique' : {'pattern' : '',
                                        'value' : 0},

                         'Clothes' : {'pattern' : '',
                                      'value' : 0},      
                         
                         'Summary' : {'pattern' : '',
                                      'value' : 0},},

            'EndBalance' : {'pattern' : '',
                            'value' : 0},}

    with open(textPath, 'r', encoding='utf-8') as ptxt:
        nextStep = False
        for line in ptxt:
            # It is regular expression search if form ("regular expression", "line of text file")
            finded = re.search('\+\d+\S\d+', line)
            # Logic of allign for going to line with money operation 
            if finded:
                print(finded.group())
                nextStep = True
            elif nextStep == True:
                print(line)
                nextStep = False


    
        
    pass

def googleSpreadDrawer():
    '''
    This function send the data to be allocated into categories
    to the google table and drawing itself.
    '''
    pass



if __name__ == "__main__":
    main()