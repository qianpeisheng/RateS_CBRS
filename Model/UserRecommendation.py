import pandas as pd
import csv
import time
from operator import itemgetter
import ast
import pathlib

# this block constructs the user item dictionary, with some helper functions
def getItem(id, idNameDescription):
    return idNameDescription.loc[idNameDescription['id'] == id].values[0][1]

# Just reads the results out of the dictionary. No real logic here.
def recommend(item_id, num, idNameDescription, itemSimilarityDict):
    #print("Recommending " + str(num) + " products similar to " + getItem(item_id) + "...")
    #print("-------")
    #print(type(itemSimilarityDict[item_id]))
    #print(itemSimilarityDict[item_id][:num])
    recs = itemSimilarityDict[item_id][:num]
    itemList = []
    for rec in recs:
        itemName = getItem(rec[1], idNameDescription)
        #print("Recommended: " + itemName + " (score:" + str(rec[0]) + ")")
        itemList.append([rec[1],itemName])
    return itemList

def createUserItemDict(df):
    arr = df.iloc[:,1:3].values
    dict = {}
    for record in arr:
        if record[0] in dict:
            dict[record[0]].append(record[1])
        else:
            dict[record[0]] = [record[1]]
    return dict

# this block defines the function to get recommendation for a specific user, with some helper functions

def orderByTime(arr, df):
    arrWithTime = []
    for record in arr:
        for item in record:
            row = df.loc[df['id'] == item[0]]
            recordWithTime = item
            recordWithTime.append(row.values[0][1])
            arrWithTime.append(recordWithTime)
    orderedList = list(reversed(sorted(arrWithTime, key=itemgetter(2))))
    return orderedList

# helper function to remove dulplicates in a list, preserving order
# ref: https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

#orderedList: [[id, name, time], []]
def removeDuplicates(itemList, orderedList):
    #first, remove duplicates in the orderedList
    #it is because different items the user likes can have the same similar item in common
    # conversion between list and tuple because list is not hashable
    orderedTuples = []
    for record in orderedList:
        orderedTuples.append(tuple(record))
    orderedTuplesWOD = f7(orderedTuples)
    orderedListWOD = []
    for record in orderedTuplesWOD:
        orderedListWOD.append(list(record))
    #second, one item the user purchases may appear in the similar item list of another item
    #which needs to be removed
    #the assumption is that the user does not want to see items she purchased in the personalized feed
    tempList = []
    duplicateFlag = False
    for record in orderedListWOD:
        for item_id in itemList:
            if item_id == record[0]:
                duplicateFlag = True
                break
        if not duplicateFlag:
            tempList.append(record)
        duplicateFlag = False
    nameList = []
    for record in tempList:
        nameList.append(record[1])
    return nameList

#return num items based on the user browse history and description of items
def getRecommendation(userId, num, userItemDict, dfTime, idNameDescription, itemSimilarityDict):
    itemList = userItemDict[userId]
    arr = []
    for item_id in itemList:
        # the worst case is that all recommendation are repeated for different items
        arr.append(recommend(item_id, num, idNameDescription, itemSimilarityDict))
    orderedList = orderByTime(arr, dfTime)
    return removeDuplicates(itemList, orderedList)

#this block pre-computes recommendation for all users, with some helper functions
#note the list of all users is not available now
#And the placeholders need to change

def hasNoHistory(userId, userItemDict):
    return not userId in userItemDict

def getRecommendationForUserWOHistory(userId):
    #placeholder
    return ['DRYPERS WEE WEE DRY BABY DIAPERS'] * 10

# pre-compute and save the recommendation for each user
# so fectching the result takes shorter time
#return a dictionary where the keys are userIds, and values are recommended item names 
def createRecommendationDict(userItemDict, dfTime, idNameDescription, itemSimilarityDict):
    start_time = time.time()
    
    #maximum number of items recommended
    #use a small number for testing (e.g. 10)
    #use a large number in production (e.g. 100)

    numberOfRecom = 10
    recommendationDict = {}
    
    # currently the list of userId is not available
    #so use the keys of userItemDict instead
    for key, value in userItemDict.items():
        userId = key
        if hasNoHistory(userId, userItemDict):
            #a personalized feed is not available since the user has no purchase history
            #TODO, use categories
            recommendationDict[userId] =  getRecommendationForUserWOHistory(userId)
        else:
            recommendationDict[userId] = getRecommendation(userId, numberOfRecom, userItemDict, dfTime, idNameDescription, itemSimilarityDict)
    print('RecommendationDict constructed. It has ' + str(len(recommendationDict)) + ' entries.')
    print("Constructing recommendation Dictionary takes %s seconds" % (time.time() - start_time))
    return recommendationDict

#result is a dictionary
#key is product id
#value is a list of pair(score, product id)
#save this to csv


def saveModelToCSV(results):
    with open('models/recommendationDict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in results.items():
            writer.writerow([key, value])
    csv_file.close()
    print('recommendataion dictionary saved')

#load files
path = 'models'
with open(path + '/itemSimilarity.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    itemSimilarityDict = dict(reader)
idNameDescription = pd.read_csv('data/idNameDescription.csv')
userProduct = pd.read_csv('data/userProduct.csv')
productTime = pd.read_csv('data/productTime.csv')

# convert string to number
itemSimilarityDict = {int(k):ast.literal_eval(v) for k,v in itemSimilarityDict.items()}

userItemDict = createUserItemDict(userProduct)
recommendationDict = createRecommendationDict(userItemDict, productTime, idNameDescription, itemSimilarityDict)
saveModelToCSV(recommendationDict)
