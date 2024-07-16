import sqlite3
import csv

# Connect to SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Create table schema (if not exists)
create_table_query = '''
CREATE TABLE IF NOT EXISTS "Flight_flight_depart_day" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "flight_id" bigint NOT NULL REFERENCES "Flight_flight" ("id") DEFERRABLE INITIALLY DEFERRED,
    "week_id" bigint NOT NULL REFERENCES "Flight_week" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX IF NOT EXISTS "Flight_flight_depart_day_flight_id_week_id_a2e3a39b_uniq" 
ON "Flight_flight_depart_day" ("flight_id", "week_id");
CREATE INDEX IF NOT EXISTS "Flight_flight_depart_day_flight_id_3dccd3a9" ON "Flight_flight_depart_day" ("flight_id");
CREATE INDEX IF NOT EXISTS "Flight_flight_depart_day_week_id_0a0fbf41" ON "Flight_flight_depart_day" ("week_id");
'''
cursor.executescript(create_table_query)

# Open and read the CSV file
with open('./data/week.csv', newline='') as csvfile:  # Change the file path as necessary
    csvreader = csv.reader(csvfile)
    # Skip the header row
    next(csvreader)
    
    for row in csvreader:
        # Check if the row has the correct number of columns
        if len(row) == 2:  # Adjust the number based on your CSV structure
            flight_id, week_id = row
            try:
                # Insert data into the table
                cursor.execute('''
                INSERT INTO "Flight_flight_depart_day" ("flight_id", "week_id")
                VALUES (?, ?)''', (flight_id, week_id))
            except sqlite3.Error as e:
                print(f"Error inserting row: {row}. Error: {e}")
        else:
            print(f"Skipping row with incorrect number of columns: {row}")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully.")
