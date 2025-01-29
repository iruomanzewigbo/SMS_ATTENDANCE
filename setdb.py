import sqlite3

# This will ensure the database is set up correctly
def setup_database():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    # Check if the student_name column exists in the attendance table
    c.execute("PRAGMA table_info(attendance);")
    columns = [column[1] for column in c.fetchall()]

    # If student_name column doesn't exist, add it
    if 'student_name' not in columns:
        c.execute("ALTER TABLE attendance ADD COLUMN student_name TEXT;")
        conn.commit()

    conn.close()

# Call the function to set up the database
setup_database()

print("Database setup completed!")
