

df <- read.csv("../../data/debate_transcripts_by_candidate_ordered_v1.csv")

library(tidyverse)

df <- read.csv("../../data/debate_transcripts_by_candidate_ordered_v1.csv")
df$debate_date <- mdy(df$debate_date)

# df_by_debate <- df %>% group_by(debate_date) %>% summarise(text = paste0(text, collapse=""))
# df_by_debate['syuzhet_sentiment'] <- get_sentiment(df_by_debate$text, method="syuzhet")


df_by_dnum_dems <- df %>% filter(!is.na(dem_debate_num)) %>% 
                  group_by(debate_date) %>% 
                  summarise(text = paste0(text, collapse=""), dem_debate_num=dem_debate_num[1])

df_by_dnum_dems <- mean(dem_debate_num)
  
View(df_by_dnum_dems)

df_by_dnum_dems <- group_by()

df_by_dnum_rep <- 
  
df_by_dnum_all