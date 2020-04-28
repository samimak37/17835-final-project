
# Description: K-means and document-word analysis.

# ref: https://javewa.github.io/2018/08/14/trolls/
library(tidyverse)
library(syuzhet)
library(lubridate)
library(RColorBrewer)


df <- read.csv("../../data/debate_transcripts_by_candidate_ordered_v1.csv")
df$debate_date <- mdy(df$debate_date)

##########################################
# Group by debate date
##########################################

df_by_debate <- df %>% group_by(debate_date) %>% summarise(text = paste0(text, collapse=""))

df_by_debate['syuzhet_sentiment'] <- get_sentiment(df_by_debate$text, method="syuzhet")

ggplot(df_by_debate, aes(x=df_by_debate$debate_date, y=df_by_debate$syuzhet_sentiment)) +
  geom_line()

df_by_debate_after1999 <- df_by_debate %>% filter(election_cycle >= 2000)

ggplot(df_by_debate_after1999, aes(x=debate_date, y=syuzhet_sentiment)) +
  geom_line()

####### Word Clouds

by_debate_corpus <- corpus(df_by_debate, docid_field = "debate_date", text_field="text")
by_debate_dfm <- dfm(by_debate_corpus, remove = stopwords("english"), remove_numbers = TRUE, remove_punct = TRUE, stem = TRUE)

dir.create(file.path("../../plots/word_clouds/by_debate/"), showWarnings = FALSE)
for (doc_name in as.character(df_by_debate$debate_date)) {
  png(filename=paste0("../../plots/word_clouds/by_debate/", doc_name, "_word_cloud.png"))
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
  cat("CLUSTER", i)
  cat("Top 10 words:") # 10 most important terms at the centroid 
  print(head(sort(km.out$centers[i, ], decreasing = TRUE), n = 10)) 
  cat("Debates classified: ")
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
  png(filename=paste0("../../plots/word_clouds/by_election_cycle/", doc_name, "_word_cloud.png"))
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

# TODO!!!




