import pandas as pd #<--- Pandas muss vorher installiert werden
import sqlite3

conn = sqlite3.connect("File.db")
db_df = pd.read_sql_query("SELECT * FROM error_log", conn)
db_df.to_csv('database.csv', index=False, header=True,line_terminator="\n",encoding='utf-8',sep=';')