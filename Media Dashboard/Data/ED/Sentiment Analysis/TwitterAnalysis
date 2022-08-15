library(rtweet)
library(dplyr)
library(tidyr)
library(tidytext)
library(ggplot2)
library(textdata)
library(wordcloud)
library(reshape2)
library(textclean)
library(lubridate)

setwd("your path here")
data = read.csv("name of file here.csv",header = T,sep = ";")


var = 'name of file ' #Example. 'merck', 'apple'
tweets.data <- data %>% select(text)
tweets.data


#remove links manually
tweets.data$stripped_text <- gsub('http\\S+|\\$\\S+|\\@\\S+|\\#\\S+', "", tweets.data$text)

# create a token for each word in stripped_text (using unnest_tokens to remove punctuations. By default, to_lower is true)
tweets.data_words <- tweets.data %>% select(stripped_text) %>% unnest_tokens(word, stripped_text)

# remove stop words, duplicate words and vulgar words
tweets.data_filtered <- tweets.data_words %>% 
  anti_join(stop_words) %>%
  filter(!grepl("\\d|@|amp|nigg|fuc", word)) %>%
  filter(!grepl(gsub(" ", "|", var), word, ignore.case = TRUE)) %>%
  subset(subset = nchar(word) != 1)

tweets.data_filtered

# Top 10 words in $ tweet
tweets.data_filtered %>%
  count(word, sort=TRUE) %>%
  top_n(20) %>%
  mutate(word=reorder(word, n)) %>%
  ggplot(aes(x=word, y=n)) + geom_col() + xlab(NULL) + coord_flip() + theme_classic() + 
  labs(x="Unique Words", y="Count", title="Unique words found in total")

#bing sentiment analysis
bing_data = tweets.data_filtered %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort=TRUE) %>%
  ungroup()

bing_data

#Data visualization
bing_data %>%
  group_by(sentiment) %>%
  top_n(20) %>%
  ungroup() %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n, fill = sentiment)) + geom_col(show.legend = FALSE) + facet_wrap(~sentiment, scales="free_y") + labs(title="Tweets", x = NULL, y = "contribution to sentiment") + coord_flip() + theme_bw()

#Worldcloud visualization
tweets.data_filtered %>%
  count(word) %>%
  with(wordcloud(word, n, max.words=200))

# Visualization of positive and negative words in a world cloud
bing_data %>%
  acast(word ~ sentiment, value.var = 'n', fill=0) %>%
  comparison.cloud(colors=c("#F8766D", "#00BFC4"),
                   max.words=100)
