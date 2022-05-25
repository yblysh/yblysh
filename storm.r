
#1
#Read in the data
data=read.csv('Australia_severe_storms_1975-2015.csv')
#Dimensions of the data
dim(data)

#2
#Clean the data
data=data[!(data$Database=='Waterspout'),-3]
#Dimensions of the cleaned data frame
dim(data)
#Print the first few rows without the 6 columns of comments
print(data[1:10,1:7])

#3
#Allocate a time zone based upon the input of State and Nearest.town
allocate=function(state,town){
  list=NULL
  for(i in 1:length(state)){
    #Broken Hill is special
    if(grepl('broken',tolower(town[i]))){
      list[i]='Australia/Broken_Hill'
    }
    #Use switch
    else{
      list[i]=switch(state[i],QLD='Australia/Queensland',NSW='Australia/NSW'
                  ,VIC='Australia/Victoria',SA='Australia/South'
                  ,WA='Australia/West',TAS='Australia/Tasmania'
                  ,NT='Australia/North',ACT='Australia/ACT')
    }
  }
  return(list)
}
#Add a column
data$Time.Zone=allocate(data$State,data$Nearest.town)

#4
#Converts the time into UTC
list=NULL
for(i in 1:length(data$Date.Time)){
  list[i]=paste(lubridate::with_tz(lubridate::as_datetime(data$Date.Time[i]
                                 ,format="%d/%m/%Y %H:%M"
                                 ,tz=data$Time.Zone[i])
                        ,tz='UTC')
                ,'',sep='')
}
data$UTC=list
#Print the first few rows without the 6 columns of comments
print(data[1:10,-(8:13)])

#5
#Create new variables for the month and year of each event
data$year=as.numeric(substring(data$UTC,1,4))
data$month=as.numeric(substring(data$UTC,6,7))
#Print the first few rows without the 6 columns of comments
print(data[1:10,-(8:13)])

#6
##i
#Create a new data frame
event_month=dplyr::count(data,data$Database,data$month)
##ii
plot(event_month[1:12,2:3],type='l',xaxt = "n"
      ,xlab='Month',col="blue",lwd=2,ylim=c(0,1000)
      ,main='the total number of event against month')
#set month.abbreviation
axis(1,1:12,month.abb)
#Set col
collist=c("blue",'purple','darkgreen','red','black')
for(i in 2:5){
  lines(event_month[(12*i-11):(12*i),2:3],col=collist[i],lwd=2)
}
legend("top",legend=dplyr::count(event_month,event_month[,1])[,1],
       col=collist,lty=1,cex=0.6)

#7
##i
#Combine the comments from these columns into a single column,
data$All.comments=paste(data$Comments,data$X,data$X.1,data$X.2,data$X.3
                        ,data$X.4,sep='')
##ii
DF=data[c(1,2,5,18,16)]
##iii
print(sapply(DF, class))

#8
##i
list=NULL
for(i in 1:length(DF$Event.ID)){
  list[i]=stringr::str_detect(DF$All.comments[i]
                      ,stringr::regex('flood', ignore_case = T))
  if(!list[i]){
    list[i]=stringr::str_detect(DF$All.comments[i]
                                ,stringr::regex('wash', ignore_case = T))
  }
  if(!list[i]){
    list[i]=stringr::str_detect(DF$All.comments[i]
                                ,stringr::regex('overflow', ignore_case = T))
  }
}
DF$indicator=list
##ii
#create a data frame to contain the number of flash floods per year.
count=dplyr::count(DF,DF$indicator,DF$year)[42:82,]
plot(count[,2:3],type='l',xlab='year',col="black",lwd=2
     ,main='the number of flash floods per year')


#9
##i
#Extract all wind speeds both those in knots and km/h
list=NULL
for(i in 1:length(data$Event.ID)){
  list[i]=stringr::str_extract(data$All.comments[i]
                              ,stringr::regex('[0-9.]+.?kt',ignore_case = T))
  
  if(is.na(list[i])){
    list[i]=stringr::str_extract(DF$All.comments[i]
                                ,stringr::regex('[0-9.]+.?knot',ignore_case = T))
  }
  if(is.na(list[i])){
    list[i]=stringr::str_extract(DF$All.comments[i]
                                ,stringr::regex('[0-9.]+.?km/h',ignore_case = T))
  }

}
data$speed=list
##ii
#Omit NA
data=na.omit(data)
#Convert km/h wind speeds to knots
for(i in 1:length(data$Event.ID)){
  if(stringr::str_detect(data$speed[i]
                         ,stringr::regex('km/h',ignore_case=T))){
    num=stringr::str_extract(data$speed[i]
                         ,stringr::regex('[1-9]+[0-9.]*',ignore_case=T))
    num=as.numeric(num)
    data$speed[i]=round(num/1.852)
  }
  else{
    num=stringr::str_extract(data$speed[i]
                          ,stringr::regex('[1-9]+[0-9.]*',ignore_case=T))
    if(num==20026){
      num=26
    }
    data$speed[i]=num
  }
}
data$speed=as.numeric(data$speed)
##iii
#Print a box plot 
boxplot(speed~State,data)
#Remove outliers
data$speed[data$speed==540]=NA
boxplot(speed~State,data,main='the wind speeds recorded per state')

