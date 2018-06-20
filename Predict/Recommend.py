import pandas as pd
import csv
import ast

#load files
with open('models/recommendationDict.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    recommendationDict = dict(reader)
recommendationDict = {int(k):ast.literal_eval(v) for k,v in recommendationDict.items()}

'''
work flow
the user request a personalized feed
Is the user in the recommendDictionary?
    Yes ---- Is it up to date? ---- need to comapre 2 states of db (purchases between t1 and t2)
        Yes ---- Show
        No ---- update it; then show
    No ---- does the user have preferred categories?
        Yes ---- show according to the categories
        No ---- show default
'''
def hasHistory(userId, recommendationDict):
    return userId in recommendationDict

# the data component retrieves the user product table
# and compare with the existing table
# if the user has bought anything inbetween, return false
# else return true
def isHistoryUpdated(userId):    
    return True

#load the userItemDictionary
#update it, and save it

#################################
#There is a concurrency issue
#################################
def updateHistory(userId):
    return True

# load and read the userCategory table
def hasCategories(userId):
    return True

def recommendByCategories(userId):
    return ["?"]

def recommendDefault():
    return ["test"]
#API to create a personal feed
#need to provide a userId, the recommendationDict argument should be recommendationDict
#which is constructed in the model component and loaded in the block above

def getRecommendationList(userId, recommendationDict, num, pageNumber):
    if hasHistory(userId,recommendationDict):
        if isHistoryUpdated(userId):
            return recommendationDict[userId][(pageNumber - 1)* num : pageNumber * num]
        else:
            updateHistory(userId)
            return recommendationDict[userId]
    elif hasCategories(userId):
        return recommendByCategories(userId)
    else:
        return recommendDefault()

#example usage
#getRecommendationList(771, recommendationDict,10, 3)
