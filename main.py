import psycopg2
import pandas as pd
import pathlib
from DataIO.DBtoCSV import *
from Model.ItemSimilarityModel import *
from Model.UserRecommendation import *
from Predict.Recommend import *
import random

def printListOfItems(listOfItem):
    for item in listOfItem:
        print(str(listOfItem.index(item) + 1) + '. ' + item + '\n')

validUsers = list(recommendationDict.keys())
userProductNameDict = loadUserProductNameDict()

while(True):
    print('Press ctrl + c or cmd + c to quit')
    print('\nTry userID ' + str(random.choice(validUsers)) + '\n')
    userId = int(input('Enter a user ID: '))
    print('\nUser ' + str(userId) + ' has purchased:\n')
    printListOfItems(getUserProductNames(userId, userProductNameDict))
    print('\nUser ' + str(userId) + ' will see:\n')
    printListOfItems(getRecommendationList(userId, recommendationDict, 10, 1))
    print('\n')


