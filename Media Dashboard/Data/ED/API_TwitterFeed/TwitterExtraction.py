import tweepy
from tweepy import place
import pandas as pd
from IPython.display import display

# bearer token
MY_BEARER_TOKEN = "your token here"

# create your client
client = tweepy.Client(bearer_token=MY_BEARER_TOKEN)



# Hashtags
# query to search for tweets
query = "#Drought lang:en -is:retweet" 
# your start and end time for fetching tweets
start_time = "2015-01-01T00:00:00Z" 
end_time = "2015-01-08T00:00:00Z"  

# get tweets from the API
tweets = client.search_all_tweets(query=query,
                                     start_time=start_time,
                                     end_time=end_time,
                                     tweet_fields=['author_id', 'created_at', 'text', 'source', 'lang', 'geo'],
                                     user_fields=['name', 'username', 'location', 'verified', 'description'],
                                     expansions=['geo.place_id', 'author_id'],
                                     place_fields=['country', 'country_code'],
                                     max_results=500,
                                     )

# create a list of records
tweet_info_ls = []
# iterate over each tweet and corresponding user details
for tweet, user in zip(tweets.data, tweets.includes['users'], ):
    tweet_info = {
        'author_id': tweet.author_id,
        'created_at': tweet.created_at,
        'text': tweet.text,
        'source': tweet.source,
        'lang': tweet.lang,
        'geo': tweet.geo,
        'name': user.name,
        'username': user.username,
        'location': user.location,
        'verified': user.verified,
        'description': user.description,
        #'country': place.country,
        #'country_code': place.country_code,

    }
    tweet_info_ls.append(tweet_info)
# create dataframe from the extracted records
tweets_df = pd.DataFrame(tweet_info_ls)
# display the dataframe
display(tweets_df)
# save df
tweets_df.to_csv("Droughttest-tweets.csv")
