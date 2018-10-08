options(warn=-1)
library(stringr)
library(plyr)
library(tm)


#MyData <- read.csv(file="C:/Users/Dell/Desktop/tw.csv", header=TRUE, sep="\n")
#MyData <- read.csv("F:/DM project/Python Scripts/ww.csv", header=FALSE)
#MyData<-unlist(MyData)
MyData <- read.csv("ww.csv", header=FALSE, comment.char="#")


sometext = sapply(MyData$V1, function(some_txt){
  # Check if tweets.csv exists
  #if (file.exists(names)){file<- read.csv(names)}
  
  # Merge the data in the file with our new tweets
  #df <- do.call("rbind", lapply(tweets, as.data.frame))
  
  #test1 of removal of stop words
  # some_txt <- df
  some_txt = gsub("(.)\\1{2,}", "\\1\\1",some_txt)
  some_txt = gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", some_txt)
  # remove at people
  some_txt = gsub("@\\w+", "", some_txt)
  # remove punctuation
  some_txt = gsub("[[:punct:]]", "", some_txt)
  # remove numbers
  some_txt = gsub("[[:digit:]]", "", some_txt)
  # remove html links
  some_txt = gsub("http\\w+", "", some_txt)
  # remove unnecessary spaces
  some_txt = gsub("[ \t]{2,}", "", some_txt)
  some_txt = gsub("^\\s+|\\s+$", "", some_txt)
  
  # define "tolower error handling" function 
  
  # lower case using try.error with sapply 
  # some_txt = sapply(some_txt, try.error)
  
  
  # remove NAs in some_txt
  #some_txt = some_txt[!is.na(some_txt)]
  #names(some_txt) = NULL
  
})



#Alia <- read.csv("F:/DM project/Python Scripts/ww.csv", header=FALSE, comment.char="#")



AFINN.111 <- read.delim("F:/DM project datasets/AFINN-111.txt", header=FALSE)

AFF <- AFINN.111
names(AFF) <-c('words','score')
AFF$words <- tolower((AFF$words))


##test under 1



sentimentScore <- function(sentences){
  final_scores <- matrix('', 0, 2)
  scores <- lapply(sentences, function(sentence){
    
    sent <- gsub('\\d+', '', sentence)
    # sentence <- tolower(sentence)
    wordList <- str_split(sent, '\\s+')
    words <- unlist(wordList)
    words <- stemDocument(words)
    
    #sentence <- gsub('\\d+', '', sentence)
    # sentence <- tolower(sentence)
  #  wordList <- str_split(sentence, '\\s+')
   # words <- unlist(wordList)
    
    sentimatch <- match(words,AFF$words)
    test_inp <- lapply(sentimatch,function(x){ 
      if(!is.na(x)){
        sumsa <- AFF$score[x]}
    }
    )
    test_inp <-unlist(test_inp)
    test_inp <- sum(test_inp)
    if(test_inp>0){
      newrow <- c(test_inp,1)}
    else if(test_inp < 0){
      newrow <- c(test_inp,-1)
    }
    else{
      newrow <-c(test_inp,0)
    }
    final_scores <- rbind(newrow)
    return(final_scores)
  })
  return(scores)
}


Result <- as.data.frame(sentimentScore(sometext))


PosN <- 0
negN <- 0
Netural <- 0
for(i in 1: length(Result)){
  if(Result[i]>0){PosN <- sum(PosN,1)}
  else if(Result[i]<0){negN <- sum(negN,1)}
  else if (Result[i]==0){Netural <- sum(Netural,1)}
  
}
PosN <- PosN/2
negN <- negN/2
Netural <- Netural/2

rate <- PosN+(0.5*Netural)
len <- (PosN+negN+Netural)/10
rate <- rate/len

rate


