import psycopg2
import pandas as pd
import pathlib
from DataIO.DBtoCSV import *
from Model.ItemSimilarityModel import *
from Model.UserRecommendation import *
from Predict.Recommend import *

while(True):
    userId = input('Enter a user ID: ')
    print(getRecommendationList(int(userId), recommendationDict, 10, 1))

