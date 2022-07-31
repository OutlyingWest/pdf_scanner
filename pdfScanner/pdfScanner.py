# -*- coding: utf-8 -*-
import os
import re
import fitz

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
    #pdfToTextConv(pdfDocPath, dataTextPath)
    dictData, incSumPos, expSumPos = dataDictInit(regexPath)
    parserData(dataTextPath, dictData, incSumPos, expSumPos)
    


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
    regexPath = progPath + 'regex.csv'
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
     Regular expressions keeps in the text file named regex.csv.

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

                                   'Grocer' : {'pattern' : '',
                                               'value' : 0},},

                         'Health' : {'pattern' : '',
                                      'value' : 0},  

                         'Sport' : {'Trainings' : {'pattern' : '',
                                                   'value' : 0},

                                    'Equipment' : {'pattern' : '',
                                                    'value' : 0},},

                         'Transport' : {'pattern' : '',
                                        'value' : 0},

                         'Technique' : {'pattern' : '',
                                        'value' : 0},

                         'Clothes' : {'pattern' : '',
                                      'value' : 0},      
                         
                         'Summary' : {'pattern' : '',
                                      'value' : 0},},

            'EndBalance' : {'pattern' : '',
                            'value' : 0},}


	# Find the positions of Base categories
    findSumPosData = ['Summary', 1, 0, 0, []]
    findedSumPosData = keyPosThroughDict(data, findSumPosData)

    # List of 'Summary' key positions
    sumPosList = findedSumPosData[4]

    print('sumPosList = ', sumPosList)

    # Find the Income Summary position
    incSumPosition = sumPosList[0]
    
    # Find the Expense Summary position
    expSumPosition = sumPosList[1]

    print('incSumPosition ', incSumPosition)	
    print('expSumPosition ', expSumPosition)

    try:
        strList = []
        with open(regexPath, 'r', encoding='utf-8') as prgxr:
            for string in prgxr:
                strList.append(string)	
    except:
        print('Cannot open regex.csv to read at first')

    print('\nstrList:\n', *strList)

	# Save open the regex.csv in write mod for includes regex of Base Categories
    try:
        with open(regexPath, 'w', encoding='utf-8') as prgxw:
            for nstr, string in enumerate(strList):
                if nstr == incSumPosition: 
                    prgxw.write('Inc. Summary; ' + '^\+\d*\s?\d+,\d\d$' + '\n') 
                elif nstr == expSumPosition:
                    prgxw.write('Exp. Summary; ' + '^\d*\s?\d+,\d\d$' + '\n')
                else:
                    prgxw.write(strList[nstr])
    except:
        print('Cannot open regex.csv to write')


	# Save open the regex.csv in read mod
    with open(regexPath, 'r', encoding='utf-8') as prgx:
	    # Creation a fixed length list 
        regexTuple = tuple([regLine.rstrip('\n').replace(' ', '').split(';')[1] for regLine in prgx])
        print('\nregexTuple:', *regexTuple, sep='\n')

    # Fill the data dictionary fields for 'pattern' key
    goInputThroughDict(data, 'pattern',  regexTuple)

    return data, incSumPosition, expSumPosition


def regIter(line, regexTupl, findExpr, findValue, incSumPosition, expSumPosition, startPos=0):
    '''
    Function that iterate over regex and compare each of their with a line
    As a result return find flags and stored value of Expr line from last
    step of main Parser loop.
    '''
    # This cycle executes at first after starting, on next step findes the value
    # Iterating over regular expressions
    lineStash = ''
    exprFinded = False
    for numreg, regex in enumerate(regexTupl):
		# If an expression is a special non finded, it should be skipped
        if numreg >= startPos:
            if numreg != incSumPosition and numreg != expSumPosition: 
                exprFinded = re.search(regex, line)

		    # If expression finded, go to summ in 'value' of finded category 	
            if exprFinded:
                print(exprFinded.group())
                findExpr = False
                findValue = True
                lineStash = line
                break
    return findExpr, findValue, numreg, lineStash


def parserData(textPath : str, dictData : dict, incSumPosition : int, expSumPosition : int):
    '''
    This function open txt file with data extracted from PDF
    and allocate this into categories according to regular expressions by file regex.csv
    '''
    


    # Init the regex tuple from dataDict. Each regex presented as simple strings
    regexTupl = tuple(goOutThroughDict(dictData, 'pattern'))
    valueList = [0] * len(regexTupl)

    # Getting keys located with accordance on higher level key - 'Income' and count them
    numIncome = len(dictData['Income'].keys()) - 1

    print("\ndictData['Income']['Summary']['pattern'] = ", dictData['Income']['Summary']['pattern'])
    print("dictData['Expense']['Summary']['pattern'] = ", dictData['Expense']['Summary']['pattern'], end='\n\n')

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

                        # Amount of over incomes
                        valueList[incSumPosition] += numdLine
    
                    elif valueExpenceFinded and numreg >= numIncome:
                        print(valueExpenceFinded.group(), 'Exp')
                        valueList[numreg] += numdLine

                        # Amount of over expenses
                        valueList[expSumPosition] += numdLine

                    elif valueExpenceFinded and numreg < numIncome:
                        # Program can go to this case if some Income regex was finded
                        # but value has not a literal '+' - it means that program will
                        # finde this regex through Expense categories   
                        _, findVl, numregex, _ = regIter(lineStash,
                                                                 regexTupl,
                                                                 findExpr,
                                                                 findValue,
                                                                 incSumPosition, expSumPosition,
                                                                 startPos=numIncome)
                        if findVl:
                            print(valueExpenceFinded.group(), 'Exp')
                            valueList[numregex] += numdLine
                        pass

                    else:
                        print('Impossible find!!!')

            # It is regular expression search if form ("regular expression", "line of text file")
            if findExpr:
                findExpr, findValue, numreg, lineStash = regIter(line,
                                                                 regexTupl,
                                                                 findExpr,
                                                                 findValue,
                                                                 incSumPosition, expSumPosition,
                                                                 startPos=0)


    valueTuple = tuple(valueList)

    print('valueTuple =', valueTuple, end='\n\n')

    # Filling the fields of dictionary 
    goInputThroughDict(dictData, 'value', valueTuple, True)

    dictData['EndBalance']['value'] = dictData['Income']['Summary']['value'] - dictData['Expense']['Summary']['value']

    print("\ndictData['Income']['Summary']['value'] =", dictData['Income']['Summary']['value'])
    print("dictData['Expense']['Summary']['value'] =", dictData['Expense']['Summary']['value'])
    print("dictData['EndBalance']['value'] =", dictData['EndBalance']['value'])


def googleSpreadDrawer():
    '''
    This function send the data to be allocated into categories
    to the google table and drawing itself.
    '''
    pass


# ------- Later may be in an other module --------
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


def keyPosThroughDict(object : dict, findData=['', 0, 0, 0, []]):
    '''
    This function takes a dictionary and a list with the following properties:
    [keyword for find,
     treeLevel - higest branch of this would have a zero level
     treeCurLevel - current level, must have zero value in starting
     position - position number of keyword in chosen treeLevel, must have zero value in starting
     positionList = [] positions of even keywords having a same treeLevel - empty in starting]
    
    (Warning! This function is for use in Python 3.7 and lastest, in eariler version it's behavior is unpredictable)

    :param object: Dictionary for take positions of that
    :param findData: list with initial parameters of find and results of this find

    :return: findData: list
    '''

    # if object is - dictionary, then analyze all values of dictionary for them keys
    if isinstance(object, dict):
        for key in object:
            # Recursive function call to itself. Allows to go through the nested dictionary 
            findData = keyPosThroughDict(object[key], findData)
            
            keyword, treeLevel, treeCurLevel, position, positionList  = findData

            if treeCurLevel == treeLevel:
                if key == keyword:
                    # Add the position number if keyword is finded
                    positionList.append(position)
                position += 1
            
            if key == 'pattern' or key == 'value':
                treeCurLevel = 0
        
        treeCurLevel += 1
        findData[2] = treeCurLevel
        findData[3] = position

    return findData





if __name__ == "__main__":
    main()
