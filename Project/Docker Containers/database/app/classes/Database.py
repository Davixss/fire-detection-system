import mysql.connector
from mysql.connector import Error


class Database:
    host = "mysql"
    user = "root"
    password = "smartcity"
    database = "smartcity"
    connection = None
    
    def __init__(self):
        pass
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                collation='utf8mb4_general_ci'
            )
            if self.connection.is_connected():
                print(">> Database connection established.")
            else:
                print(">> Connection failed.")
        except Error as e:
            print(f">> Error database connection: {e}")
            self.connection = None
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def query(self, query):
        cursor = None
        results = None
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query)

            # Controllo se la query è una SELECT
            if query.strip().lower().startswith("select"):
                # Ottieni i nomi delle colonne
                colnames = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                results = [dict(zip(colnames, row)) for row in rows]
            else:
                # Per INSERT, UPDATE, DELETE, restituisci il numero di righe modificate
                self.connection.commit()  
                results = cursor.rowcount  

        except Error as e:
            print(f"Error: '{e}'")
            results = None  
        finally:
            if cursor:
                cursor.close()
            self.disconnect()

        return results

