import pandas as pd
import requests
from bs4 import BeautifulSoup

csv_filename = 'injuries_db.csv'

df = pd.read_csv(csv_filename)

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

# Split the 'Player' column into first and last names
df[['Last Name', 'First Name']] = df['Player'].str.split(', ', n=1, expand=True)

# Rearrange the columns to get 'First Name Last Name'
df['Player'] = df['First Name'] + ' ' + df['Last Name']

df = df[::-1]
df = df.rename(columns={"Games Missed.1": "Games Missed (Confused)"})
print(df[df['Games Missed'] != df['Games Missed (Confused)']])

# Group by player name and sum the "Games Missed" column
player_sum_df = df.groupby('Player')['Games Missed'].sum().reset_index()

# Print the resulting DataFrame
print(player_sum_df)
