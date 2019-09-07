# MLSE Case Study

The Python script collects the what's trending in Canada from Twitter and stores the data into a SQL table.
The script uses pandas, request_oauthlib, and sqlite packages.
The script makes a connection to 'trends.db' and creates the table 'trends'.
We then make an API request to twitter,  OAuth1 authentication with request_oauthlib package, to receive the 'available trends'
We digest the response, convert into a data frame with Pandas and save the dataframe into the txt file 'raw.txt'
Next, filter the data frame to show 'location' trends in 'Canada'
Lastly, make another API request to twitter to get the trends in the desired 'location' using the associated 'woeids'
and for each trend insert into the SQLite table 'trends'

