# Will save image to saved_charts file.

library(ggplot2)
library(readr)

working_dir <- "stats_csv"
file_name <- "enterobacterales_stats.csv"
conserved_value <- 98

setwd(working_dir)
pic_name <- paste('picture',substr(file_name, 1, nchar(file_name)-3),sep = '_')
pic_name <- paste(pic_name,'png',sep = '')

data <- read_csv(file_name,col_names = TRUE)
data[data == 'N/A'] <- NA
data <-na.omit(data)
data$Proportion <- as.numeric(data$Proportion) * 100

g<-ggplot(data,aes(x=Position,y=Proportion))+
  geom_col(aes(fill = Proportion > conserved_value))+
  theme(legend.position = "none") +
  scale_fill_manual(values= c('gray32','tomato3'))

ggsave(filename = pic_name,
       plot = g,
       path = '../saved_charts',
       width = 20, height = 4, dpi = 150, units = "in",device = "png",
       limitsize = FALSE)


