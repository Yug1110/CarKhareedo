import mysql.connector
import difflib
import itertools
import sys

s=int(sys.argv[1])
################ Extracting Column names of existing view ######################

# Replace these with your MySQL database details
host = "localhost"
user = "root"
password = "1234"
database = "iia"

try:
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        # print("Connected to MySQL database")

        # Define a cursor to interact with the database
        cursor = connection.cursor()

        # Execute SQL queries or interact with the table here
        # For example, to select data from a table named 'your_table_name':
        f=open("view_name.txt","r")
        view_name = f.read()
        f.close()

        new_view=view_name+"1"

        f=open("view_name.txt","w")
        f.write(new_view)
        f.close()

        f=open("table_name.txt","r")
        table_name=f.read()
        f.close()

        f=open("table_name.txt","w")
        x=table_name+"1"
        f.write(x)
        f.close()

        # query = f"DESCRIBE {table_name}"
        query=f"Create table {table_name} select * from {view_name}"
        cursor.execute(query)

        query=f"delete from {table_name} where supplier={s}"
        cursor.execute(query)

        query=f"Create view {new_view} as select * from {table_name}"
        cursor.execute(query)

        query=f"Delete from supplier where id={s}"
        cursor.execute(query)
        connection.commit()


        # Fetch and print the column names
        # final_names = [row[0] for row in cursor.fetchall() if (row[0]!="supplier") and (row[0]!="id")];
        # print("Column names:", final_names)

        # Close the cursor and the connection
        cursor.close()

except mysql.connector.Error as error:
    print(f"Error in line 38: {error}")
finally:
    if 'connection' in locals():
        connection.close()
        # print("MySQL connection is closed")
