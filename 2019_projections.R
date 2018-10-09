library(plyr)
library(dplyr)
library(ggplot2)
library(rlang)
library(plotly)
setwd('~/Documents/R Codes & Datasets Full')
scraped_data <- read.csv('nba_scraped_player_data.csv')
setwd('~/Documents/R Codes & Datasets Full/nba_2019_projections')
colnames(scraped_data)[1] <- 'player_season_id'


# Analysis ----------------------------------------------------------------
scraped_data %>% filter(Name == 'Alex Abrines')
# find players whose previous seasons had similar MP, FGA, FG%, X3P., X3PA, FT.
find_similar_players <- function(Name){
  sym_name = sym(Name)
  player_data <- scraped_data %>% filter(Name == !!Name)

  rest_data <- scraped_data %>% filter(Name != !!Name,
                          Age %in% player_data$Age)
  
  find_similar_col_values(player_data, rest_data, 'MP')
    
}

find_similar_col_values <- function(data1, data2, column){
  sym_column = sym(column)
  for (i in data1$Age){
    compare_value <- data1 %>% filter(Age == i) %>% select(!!sym_column)
    print(map(data2 %>% filter(Age == i) %>% select(!!sym_column), function(x) x < compare_value + 1 & x > compare_value - 1))
  }
}
player_data_abrines <- scraped_data %>% filter(Name == 'Alex Abrines') %>% filter(Age == 23)
data_23_yo_not_abrines <- scraped_data %>% filter(Name != 'Alex Abrines', Age %in% player_data_abrines$Age) %>% .[1,]
compare_value <- 15.5
purrr::map(scraped_data %>% filter(Age == 23) %>% select(MP), function(x) x < compare_value + 1 & x > compare_value - 1)

scraped_data %>% group_by(Age) %>% 
  filter_all(all_vars(!is.na(PTS))) %>%
  summarize(pts = mean(PTS)) %>%
  mutate(rnorm_row = round(rnorm(nrow(.), mean = mean(pts), sd = sd(pts)), 0)) %>%
  ggplot(.) + geom_bar(aes(x = Age, y = pts), stat = 'identity') +
  theme_minimal()

scraped_data %>% 
  plotly::plot_ly(type = 'parcoords', line = list(color = ~Tm),
                  dimensions = list(
                    list(range = c(min(scraped_data$MP[!is.na(scraped_data$MP)]), max(scraped_data$MP[!is.na(scraped_data$MP)])),
                         label = 'MP', values = ~MP),
                    list(range = c(min(scraped_data$FG.[!is.na(scraped_data$FG.)]), max(scraped_data$FG.[!is.na(scraped_data$FG.)])),
                         label = 'FG %', values = ~FG.),
                    list(range = c(min(scraped_data$X3P.[!is.na(scraped_data$X3P.)]), max(scraped_data$X3P.[!is.na(scraped_data$X3P.)])),
                         label = '3 PT %', values = ~X3P.)
                  ))

log_pts_on_mp <- scraped_data %>%
  filter_all(all_vars(!is.na(.))) %>%
  mutate(Last_Name = paste0(sapply(strsplit(as.character(Name), " "), "[", 2))) %>%
  ggplot(data = ., aes(label = Last_Name)) +
  geom_point(aes(x = MP, y = log(PTS + 1), color = Season)) +
  geom_text(aes(x = MP, y = log(PTS + 1), color = Season), size = 4)
  
cor(scraped_data %>%
      filter_all(all_vars(!is.na(.))) %>% mutate(logPTS = log(PTS + 1)) %>%
      select(logPTS), scraped_data %>%
      filter_all(all_vars(!is.na(.))) %>% select(MP))
