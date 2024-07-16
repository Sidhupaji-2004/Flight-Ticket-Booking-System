import sqlite3
import csv

# Connect to SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Create table schema (if not exists)
create_table_query = '''
CREATE TABLE IF NOT EXISTS "Flight_place" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "airport" varchar(200) NOT NULL,
    "code" varchar(3) NOT NULL,
    "country" varchar(700) NOT NULL,
    "city" varchar(100) NOT NULL
);
'''
cursor.execute(create_table_query)

# Open and read the CSV file
with open('./data/airports.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    # Skip the header row
    next(csvreader)
    
    for row in csvreader:
        # Check if the row has exactly 4 columns
        if len(row) == 4:
            airport, code, country, city = row
            try:
                # Insert data into the table
                cursor.execute('''
                INSERT INTO "Flight_place" ("airport", "code", "country", "city")
                VALUES (?, ?, ?, ?)''', (airport, code, country, city))
            except sqlite3.Error as e:
                print(f"Error inserting row: {row}. Error: {e}")
        else:
            print(f"Skipping row with incorrect number of columns: {row}")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully.")
