import sqlite3
import hashlib


def database_connection():
    '''
    Creating a database connection that holds a table with the player's
    id, username & password
    '''
    
    sql_connection = sqlite3.connect('player_account.db') # creating a connection to the database (the door)
    cursor = sql_connection.cursor() # creating a cursor to execute commands thru the connection (the hand that does the tasks)

    # running commands thru the database with execute()
    # table name --> player_info
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_info (
                   
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
                   
                   )
    """)
    sql_connection.commit() # this commits the changes made in the database

    return sql_connection



def register(username, password):
    """
    If the player's username does not exist in the databse, then they can create an account
    """

    sql_connection = database_connection()
    cursor = sql_connection.cursor()
    cursor.execute("SELECT * FROM player_info WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result is None: # username doesn't exist, add the username to the database
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        insert_query = """
            INSERT  into player_info(username, password)
            VALUES (?, ?);
        """
        cursor.execute(insert_query, (username, hashed_password)) # cursor executes the insert query with username + hashed password
        sql_connection.commit() # saving the changes made to the databse
        sql_connection.close()
        return "Account created successfully"
    else:
        return "Username already taken"
    

def login(username, password):
    """
    Checking player's login credentials
    """

    sql_connection = database_connection()
    cursor = sql_connection.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM player_info WHERE username = ? AND password = ?", (username, hashed_password))
    result = cursor.fetchone()
    

    if result is None: # credentials don't exit in db
        sql_connection.close()
        return "Login failed"
    else:
        sql_connection.close()
        return "Login successful"








