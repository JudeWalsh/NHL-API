import pandas as pd
from sqlalchemy import create_engine
import json
import unicodedata
import requests
from bs4 import BeautifulSoup

csv_filename = 'NHL Injury Database_data.csv'

df = pd.read_csv(csv_filename, delimiter='\t', encoding='utf-16')
print(df.head(5))

df = df.drop('Chip', axis=1)
df = df.drop('Cap Hit', axis=1)



df = df[~df['Season'].str.contains(r'\(playoffs\+?\)')]

# Extract the starting year from the "Season" column
df['Season'] = df['Season'].str.extract(r'(\d{4})')

# Convert the 'Season' column to datetime objects
df['Season'] = pd.to_datetime(df['Season'], format='%Y')
#
# Filter the DataFrame to include only the past 5 years
current_year = pd.to_datetime('today').year
five_years_ago = current_year - 5
df = df[df['Season'].dt.year >= five_years_ago]

# Convert the 'Season' column to strings
df['Season'] = df['Season'].astype(str)

# Extract the starting year from the "Season" column
df['Season'] = df['Season'].str[:4]

df['Player'] = df['Player'].apply(lambda name: unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8'))

# Split the 'Player' column into first and last names
df[['Last Name', 'First Name']] = df['Player'].str.split(', ', n=1, expand=True)

# Rearrange the columns to get 'First Name Last Name'
df['Player'] = df['First Name'] + ' ' + df['Last Name']

df = df[::-1]
df = df.rename(columns={"Games Missed.1": "Games Missed (Confused)"})
# print(df[df['Games Missed'] != df['Games Missed (Confused)']])

# Group by player name and sum the "Games Missed" column
player_avg_df = df.groupby(['Player', 'Season'])['Games Missed'].sum().reset_index()
# player_avg_df['Games Missed'] /= 5

print(player_avg_df.head(15))

player_total_df = player_avg_df.groupby('Player')['Games Missed'].sum().reset_index()

player_total_df.set_index('Player', inplace=True)
player_games_missed_dict = player_total_df['Games Missed'].to_dict()

# json_str = player_total_df.to_json(orient='records')
# # Convert JSON string to JSON object
# json_obj = json.loads(json_str)
# print(player_games_missed_dict)

# # Write the DataFrame to a new CSV file
# player_avg_df.to_csv('player_games_missed.csv', index=False)


db_username = 'JPWalsh'
db_password = 'Layla724!'
db_host = 'localhost'
db_name = 'spartananalytics'

engine = create_engine(f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}")

# Insert data into MySQL table
player_avg_df.to_sql('injuries', con=engine, if_exists='replace', index=False)

print("sent to database")
