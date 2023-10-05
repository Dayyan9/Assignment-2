import pandas as pd
import sqlite3

def create_database(csv_file, db_file):
    # Read CSV file
    df = pd.read_csv(csv_file)

    # Create SQLite connection and cursor
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get column names and types from the DataFrame
    columns = ', '.join([f'{col} TEXT' for col in df.columns])

    # Create table with columns from the CSV
    create_table_query = f'CREATE TABLE IF NOT EXISTS data ({columns});'
    cursor.execute(create_table_query)

    # Insert data into the table
    insert_data_query = f'INSERT INTO data ({", ".join(df.columns)}) VALUES ({", ".join(["?" for _ in df.columns])});'
    cursor.executemany(insert_data_query, df.values.tolist())

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    csv_file_path = "listings_dec18.csv"
    db_file_path = "listings_dec18.sqlite"

    create_database(csv_file_path, db_file_path)
