# -*- coding: utf-8 -*-
import os
# import fitz
import re

def main():
    '''
    TODO: User may init the tree of find through categories by create his own categories with corresponding regular expressions
    To start, creates a basic dictionary with simple categories like: 
    Income:
    Expense:
    Balance:
    New subcategories can be added in dicrionary.
    End result may be presented in table with drop-down lists of detailed incomes and expenses
    '''
    pdfDocPath, dataTextPath, regexPath = getPath()
    # pdfToTextConv(pdfDocPath, dataTextPath)
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
     Balance:   
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


	# Find the positions of Base categories
    incSumAbsPosition = None
    for num,category in enumerate(data['Income']):
        if category == 'Summary':
            # Find the Income Summary position
            incSumAbsPosition = num
    
    expSumPosition = None
    for num, category in enumerate(data['Expense']):
        if category == 'Summary':
            # Find the Expense Summary position
            expSumPosition = num

    if  incSumAbsPosition and expSumPosition:
        expSumAbsPosition = incSumAbsPosition + expSumPosition + 1

    else:
        expSumAbsPosition = None
        print('Summary category is not finded')

    print('incSumAbsPosition ', incSumAbsPosition)	
    print('expSumAbsPosition ', expSumAbsPosition)

    try:
        strList = []
        with open(regexPath, 'r', encoding='utf-8') as prgxr:
            for string in prgxr:
                strList.append(string)	
    except:
        print('Cannot open regex.txt to read at first')

    print('strList = ', strList)

	# Save open the regex.txt in write mod for includes regex of Base Categories
    with open(regexPath, 'w', encoding='utf-8') as prgxw:
        for nstr, string in enumerate(strList):
            if nstr == incSumAbsPosition: 
                prgxw.write('^\+\d*\s?\d+,\d\d$' + '\n') 
            elif nstr == expSumAbsPosition:
                prgxw.write('^\d*\s?\d+,\d\d$' + '\n')
            else:
                prgxw.write(strList[nstr])


	# Save open the regex.txt in read mod
    with open(regexPath, 'r', encoding='utf-8') as prgx:
	    # Creation a fixed length list 
        regexTuple = tuple([regLine.rstrip('\n') for regLine in prgx])
        print('regexTuple = ', regexTuple)

    # Fill the data dictionary fields for 'pattern' key
    goInputThroughDict(data, 'pattern',  regexTuple)

    return data


def parserData(textPath : str, dictData : dict):
    '''
    This function open txt file with data extracted from PDF
    and allocate this into categories according to regular expressions by file regex.txt
    '''
    #TODO: Make a function of first cleaning 
    


    # Init the regex tuple from dataDict. Each regex presented as simple strings
    regexTupl = tuple(goOutThroughDict(dictData, 'pattern'))
    valueList = [0] * len(regexTupl)

    # Getting keys located with accordance on higher level key - 'Income' and count them
    numIncome = len(dictData['Income'].keys())
	
    # Init the regex BaseGroup. Regexes in a BaseGroup will not findes as categories
    exprBaseGroup = (dictData['Income']['Summary']['pattern'],
					 dictData['Expense']['Summary']['pattern'],)

    with open(textPath, 'r', encoding='utf-8') as ptxt:
        findExpr = True
        findValue = False
        for line in ptxt:
            # This condition is met when regular expression is finded (under this condition)  
            if findValue:
                valueIncomeFinded = re.search(dictData['Income']['Summary']['pattern'], line)
                valueExpenceFinded = re.search(dictData['Expense']['Summary']['pattern'], line)

                if valueIncomeFinded or valueExpenceFinded:
                    findExpr = True
                    findValue = False
                    # Regex for exclude non numberic values
                    numdLine = re.sub('[\+]|[\s]', '', line)

                    # Regex for replace "," to "."
                    numdLine = re.sub(',', '.', numdLine)
                    numdLine = float(numdLine)

                    if valueIncomeFinded and numreg < numIncome:
                        print(valueIncomeFinded.group(), 'Inc')

                        # Summ values according order of regex 
                        valueList[numreg] += numdLine
    
                    elif valueExpenceFinded and numreg >= numIncome:
                        print(valueExpenceFinded.group(), 'Exp')
                        valueList[numreg] += numdLine

                    else:
                        print('Impossible find!!!')

		    # This cycle executes at first after starting, on next step findes the value
            # Iterating over regular expressions 
            for numreg, regex in enumerate(regexTupl):

                # It is regular expression search if form ("regular expression", "line of text file")
                if findExpr:
				
    				# Checking is the current regex includes in the BaseGroup
                    for exprBaseRegex in exprBaseGroup:
                        exprBaseFinded = re.search(exprBaseRegex, line)
                        if exprBaseFinded:
                            break
					
					# If Base expression is not finded, find the other expressions
                    if not exprBaseFinded: 
                        exprFinded = re.search(regex, line)

                    exprBaseFinded = False

					# If expression finded, go to summ in 'value' of finded category 	
                    if exprFinded:
                        print(exprFinded.group())
                        findExpr = False
                        findValue = True
                        break
    print(valueList)


def googleSpreadDrawer():
    '''
    This function send the data to be allocated into categories
    to the google table and drawing itself.
    '''
    pass


# ------- Later may be in other module --------
def goInputThroughDict(object : dict, keyword : str, inputData : tuple, isPrint=False, lengthData=None):
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
            lengthData = goInputThroughDict(object[key], keyword, inputData, isPrint, lengthData)

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


def goOutThroughDict(object : dict, keyword : str, isPrint=False, outputData=[]):
    '''
    This function accepts a dictionary, a keyword of this dictionary and returns list of data
    that filling in accordance with accepted keyword.
    (Warning! This function is for use in Python 3.7 and lastest, in eariler version it's behavior is unpredictable)

    :param object: Dictionary for read of that
    :param keyword: The keyword that is being searched for 
    :param isPrint: Allow printing the changes in dictionary if True, else False by default
    :param outputData: List in wich data reads in accordance with keyword (shouldn't set!) Beeng utilized for internal needs.

    :return: outputData list
    '''
    
    # if object is - dictionary, then analyze all values of dictionary for them keys
    if isinstance(object, dict):
        for key in object:
            if isPrint:
                print(key, '-> ', end='')
            # Recursive function call to itself. Allows to go through the nested dictionary 
            outputData = goOutThroughDict(object[key], keyword, isPrint, outputData)

            if key == keyword:
                # Filling the values of dictionary
                outputData.append(object[key])
                if isPrint:
                    print(object[key])
    # Returns list that contains data allocated in accordance with accepted keyword.
    return outputData




if __name__ == "__main__":
    main()
