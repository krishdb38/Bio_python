#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

args <- read.table(args[1], header=FALSE)

N = args$V1

library(glmnet)
library(Matrix)
library(MASS)
##################################################################################################################
# 1.bininfo_file check
# 2.auto,y vector create -> auto_matrix rbind, y c(for loop)
# 3.Matrix
# 4.cv.glmnet
# 5.coef/save
##################################################################################################################
##################################################################################################################
###### 1.bininfo_file check ######################################################################################
#infolist = read.table("~/seqFF/bininfo1/infolist")
print("#########1.bininfo_file check")
###### 2.gmlnet parameter ######################################################################################
print("#########2.gmlnet parameter")
beta = read.csv("temptrainparasrl.csv")
inter = beta$X1[1]
beta <- beta$X1[2:N]
beta[is.na(beta)] <- 0
#names(beta) = bininfo$binName
names(inter) = "Intercept"

y = read.csv("temptestsrly", header=F)
rf = read.csv("temptestsrlrf", header=F)
rf[is.na(rf)] <- 0
x=as.matrix(rf)
y<-as.matrix(y)
###### 3.Matrix ##################################################################################################
print("#########3.Matrix")
for (i in 1:length(y)){
    enet = x[i,] %*% beta+inter
  
    if(i==1){
       final_enet <- c(enet)
    }else{
        final_enet <- c(final_enet, enet)
   }
}
result <- data.frame(final_enet, y)
write.csv(result, file="enetsrl.csv")
