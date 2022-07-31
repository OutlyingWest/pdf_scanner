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


with open('tree.csv', 'r', encoding='utf-8') as fl:
    for line in fl:
        splitedLine = line.rstrip('\n').replace(' ', '').split(';')
        print(splitedLine)


