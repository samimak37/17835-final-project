
# Description: K-means and document-word analysis.

# ref: https://javewa.github.io/2018/08/14/trolls/
library(tidyverse)
library(syuzhet)
library(lubridate)
library(RColorBrewer)
library(readtext)
library(quanteda)

df <- read.csv("../../data/debate_transcripts_by_candidate_ordered_v1.csv")
df$debate_date <- mdy(df$debate_date)

##########################################
# Group by debate date
##########################################

df_by_debate <- df %>% group_by(debate_date) %>% summarise(text = paste0(text, collapse=""),  party=party[1])
df_by_debate['syuzhet_sentiment'] <- get_sentiment(df_by_debate$text, method="syuzhet")

ggplot(df_by_debate, aes(x=debate_date, y=syuzhet_sentiment, color=party)) +
  geom_point() +
  labs(x= "Debate Debate", y="Sentiment (Syuzhet)", title="Sentiment of Debates 2000 and After") +
  theme_linedraw() +
  geom_smooth(method='lm', color='black', se=FALSE) +
  scale_colour_manual("Party", values=list("Republican Party"="Red", "Democratic Party"="Blue", "Both Parties"="Purple"))



df_by_debate_after1999 <- df %>% filter(election_cycle >= 2000)  %>% group_by(debate_date) %>% summarise(text = paste0(text, collapse=""), party=party[1])
df_by_debate_after1999['syuzhet_sentiment'] <- get_sentiment(df_by_debate_after1999$text, method="syuzhet")


my_lm <- lm(df_by_debate_after1999$syuzhet_sentiment ~ df_by_debate_after1999$debate_date)
lm_sum <- summary(my_lm)
p_value_1999 <- lm_sum$coefficients[2,4]

tiff(filename=paste0("../../plots/sentiment_2000_and_after.png"),
     units="in", width=5, height=5, res=150)

ggplot(df_by_debate_after1999, aes(x=debate_date, y=syuzhet_sentiment, color=party)) +
  geom_point() +
  labs(x= "Debate Debate", y="Sentiment (Syuzhet)", title="Sentiment of Debates in 2000 and After") +
  theme_linedraw() +
  geom_smooth(method='lm', color='black', se=FALSE) +
  scale_colour_manual("Party", values=list("Republican Party"="Red", "Democratic Party"="Blue", "Both Parties"="Purple")) +
  annotate(geom="text", x=as.Date("2014-10-05"), y=Inf, label=paste0("Slope p-value: ", round(p_value_1999, 4)),
           color="black", vjust=2, hjust=1)
dev.off()



####### Word Clouds

by_debate_corpus <- corpus(df_by_debate, docid_field = "debate_date", text_field="text")
by_debate_dfm <- dfm(by_debate_corpus, remove = stopwords("english"), remove_numbers = TRUE, remove_punct = TRUE, stem = TRUE)

dir.create(file.path("../../plots/word_clouds/by_debate/"), showWarnings = FALSE)
for (doc_name in as.character(df_by_debate$debate_date)) {
  tiff(paste0("../../plots/word_clouds/by_debate/", doc_name, "_word_cloud.png"),
       units="in", width=5, height=5, res=150)
  textplot_wordcloud(by_debate_dfm[doc_name, ], max_words = 100, color = rev(RColorBrewer::brewer.pal(10, "RdBu")))
  dev.off()
}

####### K-means 

by_debate_dfm_tfidf <- dfm_tfidf(by_debate_dfm, base = 2)

k <- 4 # number of clusters

# subset The Federalist papers written by Hamilton 
# hamilton <- c(1, 6:9, 11:13, 15:17, 21:36, 59:61, 65:85) 
# dfm.tfidf.hamilton <- dfm_tfidf[hamilton,]

## run k-means
km.out <- stats::kmeans(by_debate_dfm_tfidf, centers = k)

## label each centroid with the corresponding term 
# colnames(km.out$centers) <- featnames(dfm.tfidf.hamilton)

for (i in 1:k) { # loop for each cluster
  print("CLUSTER", i)
  print("Top 10 words:") # 10 most important terms at the centroid 
  print(head(sort(km.out$centers[i, ], decreasing = TRUE), n = 10)) 
  print("Debates classified: ")
  print(docnames(by_debate_dfm_tfidf)[km.out$cluster == i])
}


##########################################
# Group by election cycle
##########################################

df_by_cycle <- df %>% group_by(election_cycle) %>%  summarise(text = paste0(text, collapse=""))
df_by_cycle['syuzhet_sentiment'] <- get_sentiment(df_by_cycle$text, method="syuzhet")

ggplot(df_by_cycle, aes(x=election_cycle, y=syuzhet_sentiment)) +
  geom_line()

####### Word Clouds 

by_cycle_corpus <- corpus(df_by_cycle, docid_field = "election_cycle", text_field="text")
by_cycle_dfm <- dfm(by_cycle_corpus, remove = stopwords("english"), remove_numbers = TRUE, remove_punct = TRUE, stem = TRUE)

dir.create(file.path("../../plots/word_clouds/by_election_cycle/"), showWarnings = FALSE)
for (doc_name in as.character(df_by_cycle$election_cycle)) {
  tiff(paste0("../../plots/word_clouds/by_election_cycle/", doc_name, "_word_cloud.png"),
      units="in", width=5, height=5, res=150)
  textplot_wordcloud(by_cycle_dfm[doc_name, ], max_words = 100, color = rev(RColorBrewer::brewer.pal(10, "RdBu")))
  dev.off()
}

######## K-means 

by_cycle_dfm_tfidf <- dfm_tfidf(by_cycle_dfm, base = 2)

k <- 2 # number of clusters

# ## subset The Federalist papers written by Hamilton 
# hamilton <- c(1, 6:9, 11:13, 15:17, 21:36, 59:61, 65:85) 
# dfm.tfidf.hamilton <- dfm_tfidf[hamilton,]

## run k-means
km.out <- stats::kmeans(by_cycle_dfm_tfidf, centers = k)

## label each centroid with the corresponding term 
# colnames(km.out$centers) <- featnames(dfm.tfidf.hamilton)

for (i in 1:k) { # loop for each cluster
  cat("CLUSTER", i)
  cat("Top 10 words:") # 10 most important terms at the centroid 
  print(head(sort(km.out$centers[i, ], decreasing = TRUE), n = 10)) 
  cat("Years classified: ")
  print(docnames(by_cycle_dfm_tfidf)[km.out$cluster == i])
}

##########################################
# Group by Party Type
##########################################





