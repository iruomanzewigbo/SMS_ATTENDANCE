import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect('attendance.db')  # Create a database file named 'attendance.db'
    c = conn.cursor()
    
    # Create the 'attendance' table
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT,
                    student_name TEXT,
                    timestamp TEXT
                 )''')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()  # Call the function to initialize the database
