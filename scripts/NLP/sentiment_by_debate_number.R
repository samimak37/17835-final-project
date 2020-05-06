library(tidyverse)
library(syuzhet)

original_df <- read.csv("../../data/debate_transcripts_by_candidate_ordered_v2.csv")
original_df$debate_date <- mdy(original_df$debate_date)

dir.create(file.path("../../plots/sentiment_over_cycle/"), showWarnings = FALSE)

for (method in c("syuzhet", "bing", "afinn", "nrc")) {
  print(paste0("Using method: ", method))
  
  df_by_debate <- original_df %>% group_by(debate_date) %>% summarise(text = paste0(text, collapse=""))
  df_by_debate['sentiment'] <- get_sentiment(df_by_debate$text, method="syuzhet")
  
  df_by_dnum_dems_senti <- original_df %>% filter(party=="Democratic Party") %>% 
    group_by(debate_date) %>% 
    summarise(text = paste0(text, collapse=""), dem_debate_num=dem_debate_num[1]) %>%
    mutate(sentiment = get_sentiment(text, method=method)) %>%
    group_by(dem_debate_num) %>%
    summarise(mean_sentiment_dem = mean(sentiment))
  
  
  df_by_dnum_reps_senti <- original_df %>% filter(party=="Republican Party") %>% 
    group_by(debate_date) %>% 
    summarise(text = paste0(text, collapse=""), rep_debate_num=rep_debate_num[1]) %>%
    mutate(sentiment = get_sentiment(text, method=method)) %>%
    group_by(rep_debate_num) %>%
    summarise(mean_sentiment_rep = mean(sentiment)) 
  
  x <- merge(df_by_dnum_reps_senti, df_by_dnum_dems_senti)
  
  y <- gather(x, condition, measurement, c("mean_sentiment_rep", "mean_sentiment_dem"), factor_key=TRUE)
  
  y$debate_num <- ifelse(y$condition=="mean_sentiment_rep", y$rep_debate_num, y$dem_debate_num)
  y <- y %>% select(-c(1,2))
  y <- unique( y)
  y$party <- ifelse(y$condition=="mean_sentiment_rep", "Republican", "Democrat")
  df <- y %>% select(-c(1))
  
  rep_df <- df %>% filter(df$party=="Republican") 
  rep_lm <- lm(rep_df$measurement ~ rep_df$debate_num)
  rep_lm_summary <- summary(rep_lm) 
  rep_p <- rep_lm_summary$coefficients[2,4]
    
  df_dem <- df %>% filter(df$party == "Democrat")
  dem_lm <- lm(df_dem$measurement ~ df_dem$debate_num)
  dem_lm_summary <- summary(dem_lm)
  dem_p <- dem_lm_summary$coefficients[2,4]
  
  interaction_lm <- lm(df$measurement ~ df$debate_num + df$debate_num:df$party)
  inter_summary <- summary(interaction_lm)
  
  inter_p <- inter_summary$coefficients[3,4]
  
  
  tiff(paste0("../../plots/sentiment_over_cycle/primary_sentiment_over_cycle_", method, "_method.png"), 
       units="in", width=5, height=5, res=300)
  
  p <- ggplot(data=df, aes(x=debate_num, y=measurement, color=party)) +
        geom_point() +
        geom_smooth(method="lm", se=FALSE) +
    scale_colour_manual("Party", values=list("Republican"="Red", "Democrat"="Blue")) +
    labs(x="Number of Primary Debates Through a Cycle", 
         y=paste0("Average Sentiment (", method, ")"), 
         title = paste0("Average Sentiment in Primary Debates \nover an Election Cycle by Party (", method, " Sentiment)")) + 
    annotate(geom="text", x=-Inf, y=Inf, label=paste0("Interaction p: ", round(inter_p, 4)),
             color="black", vjust=2, hjust=-.1) + 
    annotate(geom="text", x=-Inf, y=Inf, label=paste0("Dem Slope p: ", round(dem_p, 4)),
           color="black", vjust=3.5, hjust=-.1) +
    annotate(geom="text", x=-Inf, y=Inf, label=paste0("Rep Slope p: ", round(rep_p, 4)),
             color="black", vjust=5, hjust=-.1) +
    theme_linedraw()
  print(p)
  dev.off()
  
  # png(filename=paste0("../../plots/sentiment_over_cycle/general_sentiment_over_cycle_", method, "_method.png"))
  tiff(paste0("../../plots/sentiment_over_cycle/general_sentiment_over_cycle_", method, "_method.png"), 
       units="in", width=5, height=5, res=300)
  
  df_by_dnum_both_parties <- original_df %>% filter(party=="Both Parties") %>% 
    group_by(debate_date) %>% 
    summarise(text = paste0(text, collapse=""), general_debate_num=general_debate_num[1]) %>%
    mutate(sentiment = get_sentiment(text, method=method)) %>%
    group_by(general_debate_num) %>%
    summarise(mean_sentiment_both = mean(sentiment))
  
  
  p <- ggplot(data=df_by_dnum_both_parties, aes(x=general_debate_num, y=mean_sentiment_both)) +
    geom_point(color="Purple", size=5) +
    labs(x="Number of General Debates Through a Cycle", 
         y=paste0("Average Sentiment (", method, ")"), 
         title = paste0("Average Sentiment in General Debates \nWithin a Cycle (", method, " Sentiment)")) +
    theme_linedraw()
  print(p)
  dev.off()
}








  