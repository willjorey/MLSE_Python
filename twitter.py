import sqlite3
import pandas as pd
from requests_oauthlib import OAuth1Session
from pandas.io.json import json_normalize

# Create connection to Sqlite db and create table
conn = sqlite3.connect('trends.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS trends (name text,url text,promoted_content text, query text, tweet_volume "
               "text)")

# Authentication for Twitter Api
twitter = OAuth1Session(client_key='89AmoS4q6XsvVORHwyOQx54Ob',
                        client_secret='9j98zcDoCmSIdEEt2qNqSxY5QjZMCWEMUXxP0TNpFX9IwIkOov',
                        resource_owner_key='1113108031531696128-1lxNFc2RLGYz5iSaLdAXT1HR2scagY',
                        resource_owner_secret='3edc21tIyzgf6tXpULOdLDdF2GkiWZv7Vlsuj02TDqwuV')
url = 'https://api.twitter.com/1.1/trends/available.json'

# Fetch the Available Trends, return as JSON
response = twitter.get(url)
response = response.json()

# Create dataframe for the JSON, normalize the nested objects
df = pd.DataFrame.from_dict(json_normalize(response), orient='columns')

# Save the data frame into 'raw.txt' file
file = open("logs/raw.txt", "w+", encoding="utf-8")
file.write(df.to_string())

# Use Dataframe to filter Country by Canada
isCanada = df['country'] == 'Canada'
canada_trends = df[isCanada]
canada_woeid = list(canada_trends['woeid'])

# Fetch the Trends for each location in 'canada_trends'
url = 'https://api.twitter.com/1.1/trends/place.json?id='
for id in canada_woeid:
    trend_response = twitter.get(url + str(id))
    trends = trend_response.json()[0]['trends']
    # Insert each trend into the 'trends' table
    for trend in trends:
        cursor.execute(
            "INSERT INTO trends (name, url, promoted_content, query, tweet_volume )VALUES (:name, :url, "
            ":promoted_content, :query, :tweet_volume);",
            trend)
conn.commit()
conn.close()
