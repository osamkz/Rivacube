import datetime
import pandas as pd
import numpy as np
import re
import pprint
pd.options.mode.chained_assignment = None
from textblob import TextBlob
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import tokenize
import spacy
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
import emoji

data = pd.read_csv('File with Reddit data')
data.head()

# split sentences by delimited "\n\n"
data["Text"] = [item.split("\n\n") for item in data.Text]
# explode nested list into individual rows
data = data.explode("Text").rename_axis("index_name").reset_index()
# replace double space with empty string
data["Text"] = data.Text.str.replace("&#x200B;", "")

# for replies with parent comments within, remove parent comment and retain replies
# those are fields with string that start with ">"
# remove bullet points
data.loc[data.Text.str.startswith(">")] = ""
data["Text"] = [i.strip() for i in data.Text]
data["Text"] = [re.sub(r"^[0-9]", " ", i) for i in data.Text]


# define function to remove both links and markup links
# also remove \' from dont\'t
def remove_https(item):
    # remove https links
    item_1 = re.sub(r"[(+*)]\S*https?:\S*[(+*)]", "", item)
    # remove https links with no brackets
    item_2 = re.sub('http://\S+|https://\S+', " ", item_1)
    # remove link markups []
    # note that this will also remove comment fields with ["Delete"]
    item_3 = re.sub(r"[\(\[].*?[\)\]]", " ", item_2)
    #     #remove \ in don\'t
    #     item_4 = re.sub("[\"\']", "'", item_3)
    return item_3


data["Text"] = [remove_https(x) for x in data.Text]
#data = data.groupby("index_name")["Text"].apply(lambda x: " ".join(x)).reset_index().drop("index_name", axis=1)

# define a function to clean up these contractions
# for \'s such as he's, she's we will just replace with he and she as is is a stop word and will be removed
def decontract(phrase):
    phrase = re.sub(r"can\'t", "cannot", phrase)
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"let\'s", "let us", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'s", "", phrase)
    # "kpkb'ing"
    phrase = re.sub(r"\'ing", "", phrase)

    phrase = re.sub(r"can’t", "cannot", phrase)
    phrase = re.sub(r"won’t", "will not", phrase)
    phrase = re.sub(r"let’s", "let us", phrase)
    phrase = re.sub(r"n’t", " not", phrase)
    phrase = re.sub(r"’m", " am", phrase)
    phrase = re.sub(r"’ll", " will", phrase)
    phrase = re.sub(r"’re", " are", phrase)
    phrase = re.sub(r"’d", " would", phrase)
    phrase = re.sub(r"’ve", " have", phrase)
    phrase = re.sub(r"’s", "", phrase)
    # "kpkb'ing"
    phrase = re.sub(r"’ing", "", phrase)
    return phrase


# decontract words in dataframe
data["Text"] = [decontract(i) for i in data.Text]


def extract_emojis(s):
    return ''.join(c for c in s if c in emoji.distinct_emoji_list(c))


# Extract the list of emojis to convert
emoji_lst = [extract_emojis(i) for i in data.Text.tolist()]
emoji_lst = list(filter(None, emoji_lst))


# define a function that converts emojis to words/ phrase
def convert_emoji(phrase):
    phrase = re.sub(r"💕", " love ", phrase)
    return phrase


data["Text"] = [convert_emoji(i) for i in data.Text]


# define a function to convert all short-forms/ short terms
def clean_short(phrase):
    phrase = re.sub(r"fyi", "for your information", phrase)
    phrase = re.sub(r"tbh", "to be honest", phrase)
    phrase = re.sub(r" esp ", " especially ", phrase)
    phrase = re.sub(r" info ", "information", phrase)
    phrase = re.sub(r"gonna", "going to", phrase)
    phrase = re.sub(r"stats", "statistics", phrase)
    phrase = re.sub(r"rm ", " room ", phrase)
    phrase = phrase.replace("i.e.", " ")
    phrase = re.sub(r"idk", "i do not know", phrase)
    phrase = re.sub(r"haha", "laugh", phrase)
    phrase = re.sub(r"yr", " year", phrase)
    phrase = re.sub(r" sg ", " singapore ", phrase)
    phrase = re.sub(r" mil ", " million ", phrase)
    phrase = re.sub(r" =", " same ", phrase)
    phrase = re.sub(r" msr. ", " mortage serving ratio ", phrase)
    phrase = re.sub(r" eip ", " ethnic integration policy ", phrase)
    phrase = re.sub(r" g ", " government ", phrase)
    phrase = re.sub(r"^imo ", " in my opinion ", phrase)
    phrase = re.sub(r" pp ", " private property ", phrase)
    phrase = re.sub(r" grad ", " graduate ", phrase)
    phrase = re.sub(r" ns ", " national service ", phrase)
    phrase = re.sub(r" bc ", " because ", phrase)
    phrase = re.sub(r" u ", " you ", phrase)
    phrase = re.sub(r" ur ", " your ", phrase)
    phrase = re.sub(r"^yo ", " year ", phrase)
    phrase = re.sub(r" vs ", " versus ", phrase)
    phrase = re.sub(r" irl ", " in reality ", phrase)
    phrase = re.sub(r" tfr ", " total fertility rate ", phrase)
    phrase = re.sub(r" fk ", " fuck ", phrase)
    phrase = re.sub(r" fked ", " fuck ", phrase)
    phrase = re.sub(r" fucked ", " fuck ", phrase)
    phrase = re.sub(r".  um.", " cynical. ", phrase)
    phrase = re.sub(r" pre-", " before ", phrase)
    phrase = re.sub(r" ed ", " education ", phrase)
    return phrase


data["Text"] = [clean_short(i) for i in data.Text]


# define a function that converts singlish
def singlish_clean(phrase):
    phrase = re.sub(r"yup", " yes", phrase)
    phrase = re.sub(r" yah ", " yes", phrase)
    phrase = re.sub(r"yeah", "yes", phrase)
    phrase = re.sub(r" ya ", "  yes", phrase)
    phrase = re.sub(r"song ah", "good", phrase)
    phrase = re.sub(r" lah", " ", phrase)
    phrase = re.sub(r"hurray", "congratulation", phrase)
    phrase = re.sub(r"^um", "unsure", phrase)
    phrase = re.sub(r" sian ", " tired of ", phrase)
    phrase = re.sub(r" eh", " ", phrase)
    phrase = re.sub(r" hentak kaki ", " stagnant ", phrase)
    phrase = re.sub(r" ulu ", " remote ", phrase)
    phrase = re.sub(r" kpkb ", " complain ", phrase)
    phrase = re.sub(r" leh.", " .", phrase)
    phrase = re.sub(r"sinkies", " rude ", phrase)
    phrase = re.sub(r"sinkie", " rude ", phrase)
    phrase = re.sub(r"shitty", "shit", phrase)
    return phrase


data["Text"] = [singlish_clean(i) for i in data.Text]
data.head


def others_clean(phrase):
    phrase = re.sub(r" govt ", " government ", phrase)
    phrase = re.sub(r"14 000", "14k", phrase)
    phrase = re.sub(r"14000", "14k", phrase)
    phrase = re.sub(r"14,000", "14k", phrase)
    phrase = re.sub(r"flipper", "flip ", phrase)
    phrase = re.sub(r"flip s", "flip", phrase)
    phrase = re.sub(r"flipping", "flip ", phrase)
    phrase = re.sub(r"hdbs", "hdb", phrase)
    phrase = re.sub(r"dont", "do not", phrase)
    phrase = re.sub(r"cant", "cannot", phrase)
    phrase = re.sub(r"shouldnt", "should not", phrase)
    phrase = re.sub(r"condominiums", "condo ", phrase)
    phrase = re.sub(r"condominium", "condo ", phrase)
    phrase = re.sub(r"btos", "bto", phrase)
    phrase = re.sub(r"non-", "not ", phrase)
    phrase = re.sub(r" x+ ", " ", phrase)
    phrase = re.sub(r" ccr or ", " ", phrase)
    phrase = re.sub(r" its ", " it ", phrase)
    return phrase


data["Text"] = [others_clean(i) for i in data.Text]

sentiment = data
sentiment.head()

# separate each comment into invididual sentences
sentiment["Text"] = [tokenize.sent_tokenize(item) for item in sentiment.Text]

# split each sentence into individual rows
sentiment_1 = sentiment.explode("Text").reset_index(drop=True)
sentiment_1.head()

#Convert from float to string
sentiment_1['Text'] = sentiment_1['Text'].astype(str)


# function to calculate subjectivity
def getSubjectivity(review):
    return TextBlob(review).sentiment.subjectivity
    # function to calculate polarity


def getPolarity(review):
    return TextBlob(review).sentiment.polarity


# function to analyze the reviews
def analysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


sentiment_1['Subjectivity'] = sentiment_1['Text'].apply(getSubjectivity)
sentiment_1['Polarity'] = sentiment_1['Text'].apply(getPolarity)
sentiment_1['Analysis'] = sentiment_1['Polarity'].apply(analysis)
sentiment_1.head()

#########################################################################
# PLOT OVERALL ANALYSIS
#########################################################################
plt.style.use("ggplot")

positive = len(sentiment_1[sentiment_1.Analysis == "Positive"])
negative = len(sentiment_1[sentiment_1.Analysis == "Negative"])
neutral = len(sentiment_1[sentiment_1.Analysis == "Neutral"])

sentiment = [positive, neutral, negative]
sentiment_cat = ["positive", "neutral", "negative"]

sentiment.reverse()
sentiment_cat.reverse()

fig, ax = plt.subplots(figsize=(10, 5))

palette = ["maroon", "darkslategrey", "seagreen"]

hbars = plt.barh(sentiment_cat, sentiment, color=palette, alpha=0.5)

ax.bar_label(hbars, fmt='%.0f', color="grey", padding=5)

plt.xticks(np.arange(0, 560, 50).tolist())

plt.xlabel("Number of Comments")
plt.title("Overall Sentiment Distribution", size=13)
plt.show()

#########################################################################
# ANALYSIS BY DATE
##################################################################

days = [item.split(" ")[0] for item in sentiment_1['Date Created'].values]
sentiment_1['days'] = days
grouped_tweets = sentiment_1[['days', 'Polarity']].groupby('days')
sentiment_byday = grouped_tweets.sum()
print(sentiment_byday)
sentiment_byday['Analysis'] = sentiment_byday['Polarity'].apply(analysis)
sentiment_byday = sentiment_byday.iloc[1:, :]
sentiment_byday.to_csv("CommentPerDay.csv")

#Plot Sentiment Per Day
def plot_df(x, y, title="", xlabel='Date', ylabel='Polarity', dpi=100):
    plt.figure(figsize=(16, 8), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.xticks(np.arange(0, len(sentiment_byday.index), 12))
    plt.xticks(rotation=45)
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.savefig('graph.png')
    plt.show()

plot_df(x=sentiment_byday.index, y=sentiment_byday.Polarity, title='Sentiment Per Day')

