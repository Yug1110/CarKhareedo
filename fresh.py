import mysql.connector
import difflib
import itertools
import sys

################ Extracting Column names of existing view ######################

# Replace these with your MySQL database details

host = "localhost"
user = "root"
password = "1234"
database = "iia"
f=open("view_name.txt","r")
existing_view=f.read()
f.close()

new_view=existing_view+"1"
f=open("view_name.txt","w");
f.write(new_view)
f.close();

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
        table_name = existing_view
        query = f"DESCRIBE {table_name}"
        cursor.execute(query)

        # Fetch and print the column names
        final_names = [row[0] for row in cursor.fetchall() if (row[0]!="supplier")];
        print("Column names:", final_names)
        print()
        print()
        # Close the cursor and the connection
        cursor.close()

except mysql.connector.Error as error:
    print(f"Error in line 53: {error}")
finally:
    if 'connection' in locals():
        connection.close()
        # print("MySQL connection is closed")

##################### Extracting Column names of new data source ##################33

# # Replace these with your MySQL database details
host = "localhost"
user = "root"
password = "1234"
database = sys.argv[2]
# database = "new_source"

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
        table_name = sys.argv[1]
        # table_name = "new_table"
        query = f"DESCRIBE {table_name}"
        cursor.execute(query)

        # Fetch and print the column names
        new_names = [row[0] for row in cursor.fetchall()]
        # print("Column names:", new_names)

        # Close the cursor and the connection
        cursor.close()

except mysql.connector.Error as error:
    print(f"Error in line 98: {error}")
finally:
    if 'connection' in locals():
        connection.close()
        # print("MySQL connection is closed")

# ###################### Matching and finding out best mapping of the final_names with new_names ###########3

def edit_distance(word1, word2):
    # Calculate the Levenshtein edit distance
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)

    return dp[m][n]

def overlap(s1, s2):
    set1 = set(s1.split())
    set2 = set(s2.split())
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection

    if union == 0:
        return 0
    return intersection / union

def ratcliff_obershelp_similarity(s1, s2):
    matcher = difflib.SequenceMatcher(None, s1, s2)
    return matcher.ratio()

def calculate_composite_score(s1, s2, weights):
    score_edit_distance = edit_distance(s1, s2)
    score_overlap = overlap(s1, s2)
    score_ratcliff_obershelp = ratcliff_obershelp_similarity(s1, s2)

    weighted_score_edit_distance = score_edit_distance * weights["edit_distance"]
    weighted_score_overlap = score_overlap * weights["overlap"]
    weighted_score_ratcliff_obershelp = score_ratcliff_obershelp * weights["ratcliff_obershelp"]

    composite_score = (
        weighted_score_edit_distance +
        weighted_score_overlap +
        weighted_score_ratcliff_obershelp
    )

    return composite_score

# Define weights for similarity algorithms
weights = {
    "edit_distance": -0.4,
    "overlap": 0.3,
    "ratcliff_obershelp": 0.3
}

# Create a dictionary to store the best attribute mapping
# best_mapping = {}

# # Create a list of attribute pairs for matching
attribute_pairs = list(itertools.product(new_names, final_names))


best_reverse_mapping = {}

# Iterate through attribute pairs and find the best reverse mapping
for new_attr, existing_attr in attribute_pairs:
    composite_score = calculate_composite_score(new_attr, existing_attr, weights)

    if existing_attr not in best_reverse_mapping or composite_score > best_reverse_mapping[existing_attr]['score']:
        best_reverse_mapping[existing_attr] = {'new_attr': new_attr, 'score': composite_score}

# Print the best reverse attribute mapping
d={}
final_dict={};
for existing_attr, mapping_info in best_reverse_mapping.items():
    d[mapping_info['new_attr']]=existing_attr;
    print(f"Best mapping for '{existing_attr}' is '{mapping_info['new_attr']}'")
    final_dict[existing_attr]=mapping_info['new_attr']

# print(final_dict)

# ######################Connecting to new_table again and changing the names of the columns according to the mapping ############

# host = "localhost"
# user = "root"
# password = "1234"
# database = "new_source"

# try:
#     # Establish a connection to the MySQL server
#     connection = mysql.connector.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=database
#     )

#     if connection.is_connected():
#         print("Connected to MySQL database")
#         cursor = connection.cursor()
#         table_name = "new_table"
#         for i in d:
#             datatype="varchar"
#             if (d[i]=="car_price") or (d[i]=="manufacturing_year") or (d[i]=="dist_reading"):
#                 datatype="bigint"
#             # print(f"{i}:  {d[i]}");
#             query = f"ALTER TABLE {table_name} CHANGE {i} {d[i]} {datatype}"
#             # print(f"Executing query: {query}")
#             cursor.execute(query)
#         ###########Now Dropping all other columns so that merging becomes easier
#         # for i in new_names:
#         #     if( i not in d.keys()):
#         #         print(i);
#         #         query=f"Alter table new_table drop column {i}";
#         #         cursor.execute(query)
            

# except mysql.connector.Error as error:
#     print(f"Error in line 208: {error}")
# finally:
#     if 'connection' in locals():
#         connection.close()
#         print("MySQL connection is closed")

# ############ Connecting to the original database again and merging both the data ###############
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
        cursor = connection.cursor()
        f=open('supplier_file.txt',"r")
        x=f.read()
        a=int(x)
        x=str(a+1)
        f.close()
        f=open('supplier_file.txt',"w")
        f.write(x)
        f.close()
        query = f"Create VIEW {new_view} AS SELECT * FROM {existing_view} UNION ALL SELECT new_table.{final_dict['car_price']} AS car_price, new_table.{final_dict['manufacturing_year']} AS manufacturing_year, new_table.{final_dict['company']} AS company, new_table.{final_dict['model']} AS model, new_table.{final_dict['car_condition']} AS car_condition ,new_table.{final_dict['fuel']} AS fuel, new_table.{final_dict['dist_reading']} AS dist_reading, new_table.{final_dict['drive']} AS drive, new_table.{final_dict['car_type']} AS car_type, new_table.{final_dict['color']} AS color, {a} AS supplier, new_table.{final_dict['id']} AS id from new_source.new_table"
        cursor.execute(query)
        
        # query=f"Drop view final"
        # cursor.execute(query)

        # query=f"Create view final as select * from updated_view"
        # cursor.execute(query)

        # query=f"Drop view updated_view"
        # cursor.execute(query)

    # connection.commit()


except mysql.connector.Error as error:
    print(f"Error in line 272: {error}")
finally:
    if 'connection' in locals():
        connection.commit()

        connection.close()
        # print("MySQL connection is closed")
