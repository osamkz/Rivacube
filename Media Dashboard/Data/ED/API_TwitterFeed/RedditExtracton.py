import praw
import pandas as pd
from datetime import datetime

reddit_authorized = praw.Reddit(client_id="...",  # your client id
                                client_secret="...",  # your client secret
                                user_agent="...",  # your user agent
                                username="...",  # your reddit username
                                password="...")  # your reddit password
###########################################################################
# FOR SUBMISSONS

posts_dict = {"Title": [], "Post Text": [],
              "Date Created": [],
              "Total Comments": [],
              }
for submission in reddit_authorized.subreddit("all").search("Drought", sort="relevance", time_filter="all", limit=None):
    date = datetime.utcfromtimestamp(submission.created_utc)

    # Title of each post
    posts_dict["Title"].append(submission.title)

    # Text inside a post
    posts_dict["Post Text"].append(submission.selftext)

    # The date of a post

    posts_dict["Date Created"].append(date)

    # Total number of comments inside the post
    posts_dict["Total Comments"].append(submission.num_comments)

    # Saving the data in a pandas dataframe

df = pd.DataFrame(posts_dict)
df = df.sort_values('Date Created', ascending=False).reset_index(drop=True)
df.to_csv("Submission-Drought-Reddit.csv")



###########################################################################
# FOR COMMENTS

comment_dict = {"Author": [], "Text": [],
                "Date Created": [],
                }
for comment in reddit_authorized.subreddit("Drought").comments(limit=None):
    date = datetime.utcfromtimestamp(comment.created_utc)

    # Title of each comment
    comment_dict["Author"].append(comment.author)

    # Text inside comment
    comment_dict["Text"].append(comment.body)

    # The date of a post

    comment_dict["Date Created"].append(date)

    # Saving the data in a pandas dataframe

cf = pd.DataFrame(comment_dict)
cf = cf.sort_values('Date Created', ascending=False).reset_index(drop=True)
cf.to_csv("Comment-Drought-Reddit.csv")

