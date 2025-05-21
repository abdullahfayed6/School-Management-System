import pyodbc

class DatabaseConnection:
    def __init__(self):
        self.SERVER_NAME = 'Abdallah'
        self.DATABASE_NAME = 'school'
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            drivers = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
            if not drivers:
                print("No SQL Server drivers found. Please install the SQL Server ODBC driver.")
                return False
            
            driver = drivers[0]
            print(f"Using SQL Server driver: {driver}")
            
            conn_str = (
                f'DRIVER={{{driver}}};'
                f'SERVER={self.SERVER_NAME};'
                f'DATABASE={self.DATABASE_NAME};'
                'Trusted_Connection=yes;'
                'TrustServerCertificate=yes;'
            )
            
            print(f"Attempting to connect to {self.SERVER_NAME}...")
            self.connection = pyodbc.connect(conn_str)
            self.cursor = self.connection.cursor()
            print(f"Successfully connected to {self.DATABASE_NAME} on {self.SERVER_NAME}")
            return True
            
        except pyodbc.Error as e:
            print(f"Error connecting to SQL Server: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return False

    def disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
                print("Database connection closed")
        except Exception as e:
            print(f"Error disconnecting from database: {str(e)}")
        finally:
            self.connection = None
            self.cursor = None

    def get_cursor(self):
        if not self.connection or not self.cursor:
            if not self.connect():
                return None
        return self.cursor

    def execute_query(self, query, params=None):
        try:
            cursor = self.get_cursor()
            if cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.connection.commit()
                return True
        except pyodbc.Error as e:
            print(f"Database error: {str(e)}")
            return False
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return False

    def fetch_all(self, query, params=None):
        try:
            cursor = self.get_cursor()
            if cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Database error: {str(e)}")
            return []
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return []

    def fetch_one(self, query, params=None):
        try:
            cursor = self.get_cursor()
            if cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchone()
        except pyodbc.Error as e:
            print(f"Database error: {str(e)}")
            return None
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None 