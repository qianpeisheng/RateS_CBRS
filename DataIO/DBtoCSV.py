import psycopg2
import pandas as pd
import pathlib

def connectToDB():
    connect_str = "dbname='rates_prod' user='postgres' host='localhost' " + \
                "password='postgres'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    return conn

#this block loads dataframes from csv files and extract relevant data
def saveToCSV(conn, addr):
    # create dataframe (id, description)
    df = pd.read_sql_query('select * from "products"',con=conn)
    df1temp1 = df.iloc[:,0:2]
    df1temp2 = df.iloc[:,3:4]
    df1 = pd.concat([df1temp1.T, df1temp2.T]).T
    df2temp1 = df1.iloc[:,0:1]
    df2temp2 = df1.iloc[:,2:3]
    df2 = pd.concat([df2temp1.T, df2temp2.T]).T

    # building the table of users and the items they like
    # only for identified users and products with pid (with description)
    df3 = pd.read_sql_query('select * from "listings_users"',con=conn)
    df4 = pd.read_sql_query('select * from "listings"',con=conn)
    df4 = df4.iloc[:,0:2]
    df4 = df4.dropna()
    df3 = df3.iloc[:,1:3]
    df3.columns = ['id', 'user_id']
    df3 = df3.dropna()
    # preference among all products visited is not considered here
    # this can be added later
    df5 = pd.merge(df3, df4, on='id')
    df5 = df5.drop_duplicates()
    df5[['user_id', 'product_id']] = df5[['user_id', 'product_id']].astype(int)

    # create dfTime to rank items
    df = df[['id','last_created']]
    
    #this block saves data to local storage as csv files
    pathlib.Path('data').mkdir(parents=True, exist_ok=True) 
    df.to_csv(addr + '/productTime.csv', index=False)
    df1.to_csv(addr + '/idNameDescription.csv', index=False)
    df2.to_csv(addr + '/description.csv', index=False)
    df5.to_csv(addr + '/userProduct.csv', index=False)


