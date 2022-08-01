library(academictwitteR)
library(lubridate)

api_key <- "your key here"
api_secret_key <- "your secret key"

# authenticate via web browser
token <- create_token(
  app = "Your name of App here",
  consumer_key = api_key,
  consumer_secret = api_secret_key)

chemin = "your path here"

# Choose start and end date
start_date = ymd("2015-01-01")
end_date = ymd("2022-07-17")



rt0 = search_tweets("#Tesla", n = 18000, since = "2022-07-20", until = "2022-07-21", retryonratelimit = TRUE)

#rt0 <- search_tweets("#Drought", n = 18000, type = "recent",since = start_date, until = start_date + 7, retryonratelimit = TRUE)

k=1
while ((start_date + 7*(k+1)) <= "2022-07-17") {
  rt = search_tweets("#Tesla", n = 18000, since = "2020-07-20", until = "2020-07-21", retryonratelimit = TRUE)
  rt0 = rbind(rt0,rt)
  k = k+1
}

setwd(chemin)

write.csv2(rt0, file = "nameoffile.csv")
