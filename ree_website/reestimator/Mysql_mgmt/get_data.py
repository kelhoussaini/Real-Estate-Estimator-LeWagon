#Load Libraries and Create engine Connection

import pymysql
import pandas as pd
import numpy as np
import sqlalchemy

class Data_loading:
    """
    Load Libraries and Create engine Connection
    """
    def __init__(self,
                 username='Estimators',
                 password='Estimators2021',
                 host='34.77.88.127',
                 port=3306,
                 database='Housing_France'):
        self.conn = self.establish_conn(username, password, host, port, database)


    def establish_conn(self,username, password, host, port, database):
        engine = sqlalchemy.create_engine(
                sqlalchemy.engine.url.URL.create(
                drivername="mysql+pymysql",
                username='Estimators',  # e.g. "my-database-user"1777777777
                password='Estimator2021',  # e.g. "my-database-password"
                host='34.77.88.127',  # e.g. "127.0.0.1"
                port=3306,  # e.g. 3306
                database='Housing_France',  # e.g. "my-database-name"
            ))
        return engine

    def load_data_chunk(self, table_name, chunksize):

        frame = pd.DataFrame()
        for chunk_dataframe in pd.read_sql(f"""Select * from {table_name}""",
                                           self.conn,
                                           chunksize=chunksize):
            print(f"Got dataframe w/{len(chunk_dataframe)} rows")
            frame = frame.append(chunk_dataframe)

        return frame


    def get_random_rows(self, table_name, numrows):

        df = pd.read_sql(
            f"""SELECT * FROM {table_name} dm ORDER BY RAND() LIMIT {numrows};""",
            self.conn)
        return df

    def get_all_rows(self, table_name):
        df = pd.read_sql(f"""SELECT * FROM {table_name} """, self.conn)
        return df

    def get_num_rows(self,table_name, rownums):
        df = pd.read_sql(f"""SELECT * FROM {table_name} Limit {rownums} """,
                         self.conn)
        return df

    def show_tables(self):
        print(self.conn)
        df = pd.read_sql(
        """SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = 'Housing_France'""",
            self.conn)
        return df

    def data_to_sql(self, df, tablename, if_exists):
        """Export Data to Sql, if exists takes one of the two strings :  ['replace','append'] """
        df.to_sql(name=f'{str(tablename)}',
                  con=self.conn,
                  if_exists=f'{if_exists}',
                  index=True)
        return print(f"the table {str(tablename)} was successfully loaded to DB")

    def get_data(self, querystring):
        df = pd.read_sql(querystring, self.conn)
        return df
      