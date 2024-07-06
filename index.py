import subprocess
import mysql.connector
import difflib
import itertools

#####################################  Printing Intro ################################33

print("Hi! How Are you?")
print("Select the usertype from below:->")
print("1.Admin")
print("2.User")
user= int(input())

################################### Entering as an Admin ################################3

if(user==1):
    print("Which option from the following would you like?")
    print("1.Add a new data source")
    print("2.Remove an existing data source")

    mode = int(input())

    if(mode == 1):
        ####################### Adding a Data Source ####################################
        table= input("Enter the name of table: ")
        database= input("Enter the name of the database in which your table exists: ")

        subprocess.run(['python' , 'fresh.py' , table , database])

        name=input("Enter the name of the supplier: ")
        phone=int(input("Enter the contact of supplier: "))
        address=input("Enter the address of the supplier: ")
        email=input("Enter the Email of the supplier: ")

        host = "localhost"
        user = "root"
        password = "1234"
        database = "iia"

        f=open("supplier_file.txt")
        id=f.read()
        id=int(id)

        id =id-1
        f.close()

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

                query= f"insert into supplier values({id},{name},{address},{email})"
                cursor.execute(query)
                connection.commit()


                # Execute SQL queries or interact with the table here
                # For example, to select data from a table named 'your_table_name':
                
        except mysql.connector.Error as error:
            print(f"Error in line 38: {error}")
        finally:
            if 'connection' in locals():
                connection.close()
                # print("MySQL connection is closed")
    

    
    if(mode == 2):
        ####################### Removing a Data Source ######################
        supplier = int(input("Enter the supplier id you want to remove "))
        subprocess.run(['python' , 'remove.py' ,str(supplier)])
    
#################################### Entering as an user ##############################
elif(user==2):
    print("Hi sir! I expect you are here because you want to know the best deal suited for you")

    print("I am gonna ask you about you some details you wish to see in your next car please mention anything you like related to that: Also if you don't want to answer any query just press N there and move on:")
    print()
    price_lower= input("Enter the lowest price of your car you want to buy ")
    if(price_lower != 'N'):
        price_lower=int(price_lower)
    
    price_upper = input("Enter the highest price of your car you want to buy ")
    if(price_upper != 'N'):
        prince_upper=int(price_upper)
    year = input("Your car can be how much older(like you don't want a model older thatn 20XX) ")
    if(year != 'N'):
        year= int(year)
    company = input("Any prefferd company? ")
    model = input("Any preffered model;(If you mentioned company above pease give the the model of the same company) ")
    fuel = input("Any prefference for fuel type? ")
    dist = input("Your car should not have travelled more than how many Kms? ")
    # print(dist)
    if(dist != 'N'):
        dist = int(dist)
    car_type = input("Any preffered type as in sedan, etc.? ")
    color = input("Any prefferd colour of your car? ")

    ############################### Selecting the best suited vehicles for the user #######################
    host = "localhost"
    user = "root"
    password = "1234"
    database = "iia"

    rows=[]

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
            existing_view=f.read()
            f.close()

            table_name = existing_view
            
            query = f"Select * from {table_name} where "
            if(price_lower != 'N'):
                query += f"car_price >= {price_lower} and "

            if(price_upper != 'N'):
                query += f"car_price <= {price_upper} and "

            if(year != 'N'):
                query += f"manufacturing_year >= {year} and "
            
            if(company != 'N'):
                query += f"company = '{company}' and "
            
            if(model != 'N'):
                query += f"model like '*{model}*' and "

            if(fuel != 'N'):
                query += f"fuel = '{fuel}' and "

            if(dist != 'N'):
                query += f"dist_reading >= {dist} and "

            if(car_type != 'N'):
                query += f"car_type = '{car_type}' and "
            if(color != 'N'):
                query += f"color = '{color}' and "
            
            if(query[-4:] == "and "):
                query= query[0:-4]
            
            query+=" order by car_price asc"
            
            print(query)
            cursor.execute(query)
            rows=cursor.fetchall()

            # print(rows[0])
            for i in range(len(rows)):
                print(f"option {i+1}")
                (price, year, company, model, condition, fuel_type, distance_travelled, drive, car_type, color, supplier,id) = rows[i];
                print(f"Price: {price}")
                print(f"Manufacturing_year {year}")
                print(f"Company {company}")
                print(f"Model {model}")
                print(f"Condition {condition}")
                print(f"Type of Fuel {fuel_type}")
                print(f"Distance Travelled: {distance_travelled}Km")
                print(f"Drive: {drive}")
                print(f"Type of Car: {car_type}")
                print(f"Color: {color}")
                print(f"Supplier Id: {supplier}")
                print("\n")
 

    except mysql.connector.Error as error:
        print(f"Error in line 38: {error}")
    finally:
        if 'connection' in locals():
            connection.close()
            # print("MySQL connection is closed")
    
    print("Do you want to buy any car?")
    print("1. Yes, i would like to buy a car")
    print("2. No i want to talk to the owner first")
    n=int(input())

    if(n==1):
        car = int(input("Enter the serial number of the car you want to buy from the above list"))
        if(car > len(rows)):
            print("You have entered a serial number out of bounds!")
        else:

            # buy ka program  likhna h ab
            (price, year, company, model, condition, fuel_type, distance_travelled, drive, car_type, color, supplier, id) = rows[car-1];
            database=f"comp{supplier}"
            table=f"set{supplier}"
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
                    query = f"Delete from {table} where id={id}"

                    # Execute SQL queries or interact with the table here
                    # For example, to select data from a table named 'your_table_name':
 

            except mysql.connector.Error as error:
                print(f"Error in line 38: {error}")
            finally:
                if 'connection' in locals():
                    connection.close()
                    # print("MySQL connection is closed")

                    
    elif(n==2):
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
                query = f"Select * from supplier"
                cursor.execute(query)
                rows=cursor.fetchall()
                for i in range(len(rows)):
                    print(f"supplier {i+1}")
                    (id, contact, address, email) = rows[i];
                    print(f"Id: {id}")
                    print(f"Contact {year}")
                    print(f"Address {company}")
                    print(f"Email {model}")

                    print("\n")


                # Execute SQL queries or interact with the table here
                # For example, to select data from a table named 'your_table_name':
 

        except mysql.connector.Error as error:
            print(f"Error in line 38: {error}")
        finally:
            if 'connection' in locals():
                connection.close()
                # print("MySQL connection is closed")