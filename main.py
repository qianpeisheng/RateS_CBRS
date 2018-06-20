import psycopg2
import pandas as pd
import pathlib
from DataIO.DBtoCSV import *
conn = connectToDB()
saveToCSV(conn, 'data')
print('Data read from DB and saved to CSV.')