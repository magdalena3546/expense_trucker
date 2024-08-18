import sqlite3

# function for set connection with sqlite
def create_connection(file_db):
    try:
        con = sqlite3.connect(file_db)
        # print(f"Connected with database: {file_db}")
        return con
    
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None
    
# function to create tables
def create_tables(con):
    try: 
        cursor = con.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                    )
                '''
            )

        cursor.execute ('''
            CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    date TEXT NOT NULL
                    )
        '''
            )

        cursor.execute ('''
            CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    category_id INTEGER,
                    FOREIGN KEY(category_id) REFERENCES categories(id)
                    )
        '''
            )
        print("Tables were created.")
    except sqlite3.Error as e:
        print(f"Error: {e}")

def insert_categories(con, categories):
    cursor = con.cursor()
    for category in categories:
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", category)
        except sqlite3.IntegrityError:
            print(f"Category '{category[0]}' already exists")
    con.commit()


# function for get summary from database
def get_summary():
    con = create_connection("expenses_tracker.db")
    cursor = con.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0 

    total = total_income - total_expenses
    
    con.close() 
    return total_expenses, total_income, total

# function for get monthly summary from database 
def get_monthly_summary(month, year):
    con = create_connection("expenses_tracker.db")
    cursor = con.cursor()
    month_str = f"{month:02d}"
    year_str = str(year)
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (month_str, year_str))
    total_monthly_expenses = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM income WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (month_str, year_str))
    total_monthly_income = cursor.fetchone()[0] or 0

    total_monthly = total_monthly_income - total_monthly_expenses

    con.close()
    return total_monthly_expenses, total_monthly_income, total_monthly