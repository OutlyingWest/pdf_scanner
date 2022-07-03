def goOutThroughDict(object : dict, keyword : str, treeLevel, curTreeLevel=0, outputData=[]):
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
    outputData = [keyword, 
                  treeLevel, 
                  curTreeLevel,
                  positionList]
    # if object is - dictionary, then analyze all values of dictionary for them keys
    if isinstance(object, dict):
        position = 0
        for key in object:
            # Recursive function call to itself. Allows to go through the nested dictionary 
            outputData = goOutThroughDict(object[key], outputData)
            
            keyword, treeLevel, curTreeLevel, positionList  = outputData

            if curTreeLevel == treeLevel:
                if key == keyword:
                    # Add the position number if keyword is finded
                    outputData.append(position)
                position += 1
    # Returns list that contains data allocated in accordance with accepted keyword.
    return outputData





#goOutThroughDict()
keyword = 'pat'
treeLevel = 1
curTreeLevel = 0
positionList = []

outputData = [keyword, 
              treeLevel, 
              curTreeLevel,
              positionList]

keyword, treeLevel, curTreeLevel, positionList  = outputData

positionList.append(1) 

print(positionList) 

positionList.append(2) 

print(positionList) 

