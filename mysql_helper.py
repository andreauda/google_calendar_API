import mysql.connector
from mysql.connector import errorcode
import logging
import sqlalchemy
import sys
import pandas as pd

def mysql_connector(server, port, database, username, password):
    
    config = {
        'user': username,
        'password': password,
        'host': server,
        'database': database,
        'raise_on_warnings': True
    }
    
    try:
        cnx = mysql.connector.connect(**config)
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.exception("Something is wrong with your user name or password")
            raise 
            
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.exception("Database does not exist")
            raise
            
        else:
            logging.exception(err)
            raise
    else:
        return cnx
        
def mysql_engine(server, port, database, username, password):
    
    try: 
        engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.
                                        format(username, password, server, port, database)
                                        , pool_pre_ping=True)
    
    except Exception as ex:
        logging.exception(err)
        raise
        
    else:
        return engine

def create_database(cursor, db_name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        sys.exit()
        
def read_table(query, engine):
    
    try:
        df = pd.read_sql(query, con=engine)
        
        return df
        
    except sqlalchemy.exc.OperationalError as ex:
        logging.info('Error occured while executing a query {}'.format(ex.args))
        logging.exception(ex)
        raise
    
