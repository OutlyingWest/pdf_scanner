import os
import fitz
from collections import namedtuple

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
                allText.append(page.get_text().encode("utf8"))
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
    # Income:
    wages = ['Wages', 0] 
    grants = ['Grants', 0]
    otherProfit = ['Other profit', 0]

    Income = namedtuple('Income', ('Wages', 'Grants', 'OtherProfit'))
    income = Income(wages, grants, otherProfit)

    # Expense:
    technique = ['Technique', 0]
    clothes = ['Clothes', 0]

    #   Food:
    restoraunts = ['Restoraunts', 0]
    delivery = ['Delivery', 0]
    grocer = ['Grocer', 0] 

    Food = namedtuple('Food', ('Restoraunts', 'Delivery', 'Grocer'))
    food = Food(restoraunts, delivery, grocer)

    #   Sport:
    trainings = ['Trainings', 0]
    equipment = ['Equipment', 0]

    Sport = namedtuple('Sport', ('Trainings','Equipment'))
    sport = Sport(trainings, equipment)



    # Construct Expense
    Expense = namedtuple('Expense', ('Food', 'Sport', 'Technique', 'Clothes'))
    expense = Expense(food, sport, technique, clothes)


    # Data:
    Data = namedtuple('Data', ('Income', 'Expense'))
    data = Data(income, expense)
    
    print(data.Income)


    pass

def googleSpreadDrawer():
    '''
    This function send the data to be allocated into categories
    to the google table and drawing itself.
    '''
    pass



if __name__ == "__main__":
    main()