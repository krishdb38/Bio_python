#!/usr/bin/env Rscript

library(glmnet)
library(Matrix)
library(MASS)
library(doParallel)
registerDoParallel(40)
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
y = read.csv("temptrainy", header=F)
rf = read.csv("temptrainrf", header=F)
rf[is.na(rf)] <- 0
###### 3.Matrix ##################################################################################################
print("#########3.Matrix")
x=as.matrix(rf)
#x = rf
y<-as.matrix(y)
#y<-y*0.01
###### 4.cv.glmnet ###############################################################################################
print("#########4.cv.glmnet")
seqFF_para_cv = cv.glmnet(x, y, alpha=.01, grouped = FALSE, nfolds=10, parallel=TRUE)
#par(mar = rep(2, 4))
#plot(seqFF_para_cv)
###### 5.coef/save ###############################################################################################
print("#########5.coef()/save")
#seqFF_para_cv_result <-coef(seqFF_para_cv, s=seqFF_para_cv$lambda.min)
seqFF_para_cv_result <-coef(seqFF_para_cv, s="lambda.min")
result <- as.data.frame(as.matrix(seqFF_para_cv_result))
#write.csv(result,file="~/seqFF/test_result.csv")
write.csv(result,file="temptrainparargc10000.csv")
