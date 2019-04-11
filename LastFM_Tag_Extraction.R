devtools::install_github("juyeongkim/lastfmr", force=TRUE)
library(lastfmr)
library(dplyr)
library(tidyr)

Sys.setenv(lastfm_key = "#")

#add data
library(data.table)
setwd("#")
spotify <- fread("cleandata.csv", stringsAsFactors = F)

#turn to dataframe
spotify.df<-as.data.frame(spotify)

#############################################################
#extract track info function
song_info<- function (x,l){
  my_vector <- vector("character",length = 0L)
  j1 <- which(tolower(colnames(x)) == "artist")
  j2 <- which(tolower(colnames(x)) == "song_title")
  for (i in 1:nrow(x)){
    song_detail<-try(as.data.frame(track_getInfo(artist = (x[i,j1]), track = (x[i,j2]))),silent = T)
    if(inherits(song_detail, "try-error"))
    {
      my_vector[i] = NA
      next
    }
    song_details_final<-song_detail[,l]
    my_vector[i] = song_details_final
  }
  return(my_vector)
}

#run function to create new variables
spotify.df$listeners <- song_info(x = spotify.df,l='listeners')
spotify.df$playcount <- song_info(x = spotify.df,l='playcount')
toptag_variable <- song_info(x = spotify.df,l='toptags')

#function to iterate through tags and extract top 5 tags
topt<-function (y){
  df = data.frame()
for (i in 1:NROW(y)){
  for (j in 1:5){
    name<-try(y[[i]][[1]][j],silent = T)
    if(inherits(name, "try-error"))
    {
      name<- NA
      next
    }
    df[i,j]<-name
  }
}
  return(df)
}

#call tag function
tags<-topt(y = toptag_variable)

#bind output tag dataframe to main dataframe
spotify.df<-cbind(spotify.df,tags)

#change new column names
setnames(spotify.df, "V1", "toptag1")
setnames(spotify.df, "V2", "toptag2")
setnames(spotify.df, "V3", "toptag3")
setnames(spotify.df, "V4", "toptag4")
setnames(spotify.df, "V5", "toptag5")

#write to csv
write.csv(spotify.df, "spotify_final.csv")

