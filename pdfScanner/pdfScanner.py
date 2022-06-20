# -*- coding: utf-8 -*-
import os
import fitz
import re

def main():
    pdfDocPath, dataTextPath, regexPath = getPath()
    pdfToTextConv(pdfDocPath, dataTextPath)
    dictData = dataDictInit(regexPath)
    parserData(dataTextPath, dictData)
    


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
    regexPath = progPath + 'regex.txt'
    return pdfDocPath, dataTextPath, regexPath


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


def dataDictInit(regexPath : str):
    '''
     This function of initialisation of data dictionary.
     Initialisation comprise regular expressions for all categories.
     Regular expressions keeps in the text file named regex.txt.

     Structure of the data dictionary:
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
    # Saved open the PDF
    try:
        with open(regexPath, 'r', encoding='utf-8') as prgx:
            # Creation a fixed length list 
            regexList = tuple([regLine.rstrip('\n') for regLine in prgx])
            print(regexList)
            #for nline, regLine in enumerate(prgx):
            #    regexList[nline] = regLine
    except:
        print('regex.txt is not found')

    return data


def parserData(textPath : str, dictData : dict):
    '''
    This function open txt file with data extracted from PDF
    and allocate this into categories according to regular expressions by file regex.txt..
    '''

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


# ------- Later may be in other module --------
def goThroughDict(object : dict, keyword : str, inputData : tuple, isPrint=False, lengthData=None):
    '''
    This function accepts a dictionary, a keyword of this dictionary and a tuple of data
    that must be filling in accordance with this keyword. In the tuple of data
    may be wrided several values, that will allocated in order of tuple's structure
    (Warning! This function is for use in Python 3.7 and lastest, in eariler version it's behavior is unpredictable)

    :param object: Dictionary for fill in that
    :param keyword: The keyword that is being searched for 
    :param inputData: Data posted in accordance with keyword
    :param isPrint: Allow printing the changes in dictionary if True, else False by default
    :param lengthData: There is no need to enter. Calculates automatically! Beeng utilized for internal needs

    :return: lengthData It's not filled with meaning. Beeng utilized for internal needs
    '''
    if lengthData == None:
        lengthData = len(inputData)
    # if object is - dictionary, then analyze all values of dictionary for them keys
    if isinstance(object, dict):
        for key in object:
            if isPrint:
                print(key, '-> ', end='')
            # Recursive function call to itself. Allows to go through the nested dictionary 
            lengthData = goThroughDict(object[key], keyword, inputData, isPrint, lengthData)

            if key == keyword:
                # Reverse the tuple in order to fill values in right order (:
                revInputData = tuple(reversed(inputData))
                # Decrement lengthData to go through the inputData tuple
                lengthData -= 1
                if lengthData < 0:
                    print('Incorrect param: lengthData = ', lengthData, ' Error: out of range')
                    exit()
                # Filling the values of dictionary
                object[key] = revInputData[lengthData]
                if isPrint:
                    print(object[key])
    # Returns length of tuple that contains data for fill the values of dict 
    return lengthData


if __name__ == "__main__":
    main()