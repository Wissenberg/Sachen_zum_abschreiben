import sqlite3
import pandas as pd

class DBMapper:
    def __init__(self):
        self.open_db_connection()

    def open_db_connection(self):
        try:
            self.con = sqlite3.connect('test.db')
            self.cur = self.con.cursor()
        except ConnectionError:
            self.open_db_connection()   

    def toCSV(self):
        sql_query = pd.read_sql_query('SELECT * FROM test;', self.con)
        sql_query.to_csv('test.csv', index = False, line_terminator = '\n',sep=";")

if __name__ == '__main__':
    db = DBMapper()
    db.toCSV()