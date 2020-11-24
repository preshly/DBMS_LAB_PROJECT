
import mysql.connector

class Usedatabase:
    """
    class to maintain the database connections.
    define the connection configurations
    create the connection
    create cursor
    use the cursor to work with the database
    commit the changes done
    close the cursor
    close  the connection
    """
    def __init__(self, config: dict) -> None:
        self.configuration = config
    
    def __enter__(self) -> 'cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()