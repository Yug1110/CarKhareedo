import pandas as pd
from sqlalchemy import create_engine

# Set up a connection to your SQL database
db_url = 'mysql://root:1234@localhost/comp2'
engine = create_engine(db_url)

# Load the CSV file into a pandas DataFrame
csv_file = "data2 - Sheet1.csv"
df = pd.read_csv(csv_file)

df['id'] = range(1, len(df) + 1)

# Insert the data into the SQL table
df.to_sql('set2', engine, if_exists='replace', index=False)
