# Standard imports
from decouple import config
import psycopg2
from datetime import datetime
import pytz

# Custom imports
from psql.config import Logging

class main:

    def __init__(self):
        # Logger
        self.logger = Logging.Logger(__name__).get()

        self.conn = None
    
    ################################################ FUNCTIONS ################################################
    
    def connect(self, database_name):
        # Close existing connection if any
        if self.conn is not None:
            self.close()
        
        try:
            connection = psycopg2.connect(
                host="postgres",
                user=config('PSQL_DB_USER'),
                password=config('PSQL_DB_PASSWORD'),
                database=database_name
            )
            # self.logger.info(f"Successfully connected to PostgreSQL {database_name}")
            self.conn = connection
        except psycopg2.Error as e:
            self.logger.error(f"Error connecting to PostgreSQL database: {e}")
            raise
        


    ################################################ CLOSING ################################################
    
    def commit(self):
        self.conn.commit()
    
    def close(self):
        self.conn.commit()
        self.conn.close()
    
    