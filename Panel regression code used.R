install.packages("plm") 
install.packages("lmtest") 
library(lmtest) 
library(plm) 
dataset<-read.csv("C:\\Users\\arora\\Downloads\\dataset (2).csv") 
dataset<-pdata.frame(dataset, index=c("Dist.Name","Year")) 
#Handling duplicate values 
dataset <- dataset[!duplicated(dataset[, c("Dist.Name", "Year")]), ] 

#Model building 
model<- plm(RICE.PRODUCTION..1000.tons._x ~ 
              Amount.Outstanding..in.Rs.Crores., 
            data = dataset, 
            index = c("Dist.Name","Year"), 
            model = "within", 
            effect = "twoways") 

coeftest(model,vcov=vcovHC, type = "HC1") 
## t test of coefficients: 
##  
##                                     Estimate Std. Error t value Pr(>|t|) 
## Amount.Outstanding..in.Rs.Crores. -0.0010767  0.0046337 -0.2324   0.8163