# Standard imports
from typing import List, Dict, Any, Optional
import psycopg2

# Custom imports
from psql.config import Logging

class main:
    def __init__(self, psql_connection):
        self.logger = Logging.Logger(__name__).get()
        self.psql_connection = psql_connection

    
    ################################################ GENERAL ################################################

    def execute(self, query: str, queryData: List[Any] = None, suppress_logging: bool = False):
        try:
            cursor = self.psql_connection.cursor()
            if queryData:
                cursor.execute(query, queryData)
            else:
                cursor.execute(query)
        except psycopg2.Error as e:
            if not suppress_logging:
                self.logger.error(f"Failed to execute query: {query}")
                self.logger.error(f"Error: {e}")
            self.psql_connection.rollback()
            raise
        finally:
            try:
                if cursor.description:  # Check if description exists
                    columns = [desc[0] for desc in cursor.description]  # Get column names
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert to dict
                else:
                    results = []  # No results returned
            except psycopg2.ProgrammingError:
                results = []
            
            self.psql_connection.commit()
            cursor.close()
            return results
            
    ################################################ BASIC FUNCTIONS ################################################
    
    def select(self, query: str, suppress_logging: bool = False):
        return self.execute(query, suppress_logging)
    
    def selectOne(self, query: str, queryData: List[Any] = None, suppress_logging: bool = False):
        results = self.execute(query, queryData, suppress_logging)
        if results:
            return results[0]
            
        return results

    def insert(self, sql: str, sqlData: List[Any] = None, suppress_logging: bool = False):
        return self.execute(sql, sqlData, suppress_logging)
    

    def delete(self, sql: str, sqlData: List[Any] = None, suppress_logging: bool = False):
        try:
            cursor = self.psql_connection.cursor()
            if sqlData:
                cursor.execute(sql, sqlData)
            else:
                cursor.execute(sql)

        except psycopg2.Error as e:
            if not suppress_logging:
                self.logger.error(f"Failed to execute query: {sql}")
                self.logger.error(f"Error: {e}")
            self.psql_connection.rollback()
            raise
        finally:
            self.psql_connection.commit()
            cursor.close()
            return True
        

    ################################################ CUSTOM FUNCTIONS ################################################

    def show_tables(self, suppress_logging: bool = False):
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """
        return self.execute(query, suppress_logging)
