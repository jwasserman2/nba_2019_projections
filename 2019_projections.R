library(plyr)
library(dplyr)
library(ggplot2)
scraped_data <- read.csv('nba_scraped_player_data.csv')
colnames(scraped_data)[1] <- 'player_season_id'


# Analysis ----------------------------------------------------------------
scraped_data %>% filter(Name == 'Alex Abrines')
# find players whose previous seasons had similar MP, FGA, FG%, X3P., X3PA, FT.
find_similar_players <- function(Name){
  player_data <- scraped_data %>% filter(Name == Name)
  
  scraped_data %>% filter(Name != Name)
    
}
scraped_data %>% group_by(Age) %>% 
  filter_all(all_vars(!is.na(PTS))) %>%
  summarize(pts = mean(PTS)) %>%
  mutate(rnorm_row = round(rnorm(nrow(.), mean = mean(pts), sd = sd(pts)), 0)) %>%
  ggplot(.) + geom_bar(aes(x = Age, y = pts), stat = 'identity') +
  theme_minimal()

summary(lm(PTS ~ Age + Tm + Season + MP + FGA, data = scraped_data[!is.na(scraped_data$PTS),]))


         