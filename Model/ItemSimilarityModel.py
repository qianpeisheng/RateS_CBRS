import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import time
import csv
import pathlib
from pathlib import Path

#this block trains the model
def train(df):
    start_time = time.time()
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df['description'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    results = {}
    for idx, row in df.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], df['id'][i]) for i in similar_indices]
    
        # First item is the item itself, so remove it.
        # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, item_id)
        results[row['id']] = similar_items[1:]
    print("Training completed. It takes %s seconds" % ('%.3f'%(time.time() - start_time)))
    return results

#result is a dictionary
#key is product id
#value is a list of pair(score, product id)
#save this to csv
def saveModelToCSV(results, addr):
    with open(addr + '/itemSimilarity.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in results.items():
            writer.writerow([key, value])
    csv_file.close()

def checkSimilarityModel(addr):
    return Path(addr + '/itemSimilarity.csv').is_file()

path = 'models'
if (not checkSimilarityModel(path)):
    df = pd.read_csv('data/description.csv')
    results = train(df)
    Path(path).mkdir(parents=True, exist_ok=True)
    saveModelToCSV(results, path)
else:
    print('Item silimarity model already exists')