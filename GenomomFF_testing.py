#Author:Sunshin Kim (sunshinkim3@gmail.com)
# Krishna(krishdb38@gmail.com)

import pandas as pd
import numpy as np
import os
import subprocess
import time
import os,sys
from scipy import stats
import shutil#To copy parameter File from test to testing Folder
#from shutil import copyfile
# Declaring Global Variables
#Variable Related to RGC
rgc_bin_info = None #User Input RGC Bin File
ffyrgc = None       # FFyrgc + ... Out put By Loesstrain() Function
trgc   = None       #trgc +.... is  also Output By Loesstrain() Function
temptrain_rgc = None # Output by Arrangetrain() 
temptrain_rgc_y=None #output By Enet() Function Arrangetrain()
temptrain_rgc_rf=None #Output By Enet() Function
temp_train_par_rgc = "temptrain_par_rgc1000.csv" #1000 Data Set
#temp_train_par_rgc =None#Output By GLmnet for Training Purpose
enet_rgc = None     #Output By testing cal_enetrgc

# Global Variable for SRL
srl_bin_info = None #User Input SRL Bin File 
ffysrl= None       # FFyrgc + ... Out put By Loesstrain() Functio  = None       #trgc +.... is  also Output By Loesstrain() Function
tsrl   = None       #trgc +.... is  also Output By Loesstrain() Function
temptrain_srl = None # Output by Arrangetrain() 
temptrain_srl_y=None #output By Enet() Function
temptrain_srl_rf=None #Output By Enet() Function
enet_srl = None

temp_train_par_srl = "temptrain_par_srl1000.csv"
#temp_train_par_srl =None #Output By GLmnet for Training Purpose

def read_bin():
    global srl_bin_info,rgc_bin_info   # info File 
    global ffyrgc,trgc    #RGC R file Output
    global ffysrl,tsrl
    ###############################
    global temptrain_rgc, temptrain_srl
    #Arrange train
    global temptrain_srl_rf, temptrain_srl_y
    global temptrain_rgc_rf, temptrain_rgc_y
    #Parameter Value
    global temp_train_par_rgc , temp_train_par_srl
    global enet_rgc , enet_srl
    print("Welcome To FF Analysis 1.0 Version \nTESTING")
    #print( "Put your RGC files and rgc_bininfo file in RGC FOLDER")
    #print("Put Your SRL FILes and SRL bin info in SRL FOLDER")
    files = os.listdir("./testing/")
    #print(files)
    for file in files:
        if file[:10]=="rgcbininfo":
            rgc_bin_info = file
            ffyrgc = "ffyrgc_"+file[11:]
            trgc   = "trgc_"+ file[11:]
            temptrain_rgc = "temptrain_rgc_"+file[11:]            
            temptrain_rgc_rf = "temptrain_rgc_rf"+file[11:]
            temptrain_rgc_y = "temptrain_rgc_y"+file[11:]
            #temp_train_par_rgc = "temptrain_par_rgc"+file[11:]
            enet_rgc = "enet_rgc_" + file[11:]
    if rgc_bin_info == None:
        print("RGC Bininfo file Not found")
        sys.exit(1)
    #for SRL 
    files = os.listdir("./testing/")
    for file in files:
        if file[:10] in ("srlbininfo","SRLBININFO"):
            srl_bin_info = file
            ffysrl= "ffysrl_"+file[11:]
            tsrl = "tsrl_" + file[11:]
            temptrain_srl = "temptrain_srl_"+file[11:]
            temptrain_srl_rf = "temptrain_srl_rf_"+file[11:]
            temptrain_srl_y = "temptrain_srl_y_"+file[11:] 
            #temp_train_par_srl = "temptrain_par_srl"+file[11:]
            enet_srl = "enet_srl_"+file[11:]
        
    if srl_bin_info == None:
        print("SRL Bininfo file Not found")
        sys.exit(1)
    files = os.listdir("./")
    print("we found following RGC and SRL bininfo files")
    print("RGC info file is \t",rgc_bin_info)
    print("SRL info file is \t",srl_bin_info)
    print("\n\n")
    

def get_parameter_file(): #Files must be copoied by Automatic....py
    global temp_train_par_rgc , temp_train_par_srl
    files = os.listdir("./test/")
    
    if temp_train_par_rgc in files and temp_train_par_srl in files:
        shutil.copy("./test/"+temp_train_par_rgc , "./testing/")
        shutil.copy("./test/"+temp_train_par_srl, "./testing/")
        print("Files Copied SUCCESSFULLY")
    else:
        print("Please Copy temptrain parameter Files Manually")

def Loesstest_rgc(): #Rscript Code Will Run with Python
    global rgc_bin_info,ffyrgc , trgc
    #print(rgc_bin_info,ffyrgc,trgc )
    #While Running All Code
    #From Now we will run all code in 
    os.chdir("./testing/")
    #changed the working Directory
    #os.chdir("./test/RGC/") #While Running RGC Only
    cmd = ['Rscript','loessgctest.R',rgc_bin_info ,ffyrgc,trgc ] 
    #Parameter Must be passed bininfo file, Y and X[ffyrgc and trgc is Output file made by loessgctrain.R]
    out = subprocess.run(cmd,shell=True,capture_output =True, text=True)
    if out.returncode !=0:
        print("Error rises")
        print(out.stderr)
        print(out.returncode)
    else:
        print("cal_enetrgc. Ran SuccessFully")
        print(out.stdout)

def Arrangetest_rgc():
    #If this Function raises Error then need to check working Directory
    #a =(os.getcwd())
        
    global ffyrgc , trgc, temptrain_rgc , temptrain_rgc_rf , temptrain_rgc_y

    #print(ffyrgc , trgc, temptrain_rgc , temptrain_rgc_rf , temptrain_rgc_y)
    ##################################################cd .
    df_y = pd.read_csv(ffyrgc,usecols=[1])
    df_y = df_y.rename(columns=df_y.iloc[0]) #Rename First Row as Header
    df_y = df_y.iloc[1:,:] #Since Header is replaced with FIrst Row so remove FIrst Row
    #Remove first Row that is header was replaced #all rows from 1
    #Need to Check and compare before final
    df_y.to_csv(temptrain_rgc_y,index=False)#,index = None , header = False)
    #Variable Y
    df_x = pd.read_csv(trgc)
    df_x= df_x.iloc[:,1:]
    df_x = df_x.rename(columns = df_x.iloc[0])
    df_x = df_x.iloc[1:,:]
    
    df_x.to_csv(temptrain_rgc_rf,index=None)
    #,index = None , header = False)Index = False
    #The below File is not used 
    pd.concat([df_y , df_x],axis =1).to_csv("temptrain_rgc.csv")#,index =None,header=False) 

def losetrain_SRL_R():  #rlnormtest change
    global srl_bin_info,ffysrl , tsrl
    print(srl_bin_info,ffysrl , tsrl)
    print(os.getcwd())
    #os.chdir("./test/SRL") #When Working with RGC FOlder Path Must Be changed
    #if Error raised then need to varify path (working directory) folder
    cmd = ['Rscript',"srlnormtest.R",srl_bin_info , ffysrl , tsrl]
    #print(os.getcwd())
    
    out = subprocess.run(cmd,shell=True,capture_output =True, text=True)
    if out.returncode !=0:
        print("Error rises")
        print(out.stderr)
        print(out.returncode)
    else:
        print("cal_enetrgc. Ran SuccessFully")
        print(out.stdout)
        
def cal_enet_rgc():
    print("Calculating calenet_rgc") 
    global temp_train_par_rgc , temptrain_rgc_y , temptrain_rgc_rf ,enet_rgc 
    #print(type(temp_train_par_rgc) , type(temptrain_rgc_y) , type(temptrain_rgc_rf) ,type(enet_rgc))
    #Accept 3 Parameter as input and Give One Output enet.rgc
    #Cal_enet  first param temptrain_par_rgc_.. , temp_test_rgc_y_.. ,temp_test_rgc_rf(x).. and Output_file to save
    
    cmd = ['Rscript', 'cal_enetrgc.R',temp_train_par_rgc,temptrain_rgc_y,temptrain_rgc_rf,enet_rgc]
    out = subprocess.run(cmd,shell=True,capture_output =True, text=True)
    if out.returncode !=0:
        print("Error rises")
        print(out.stderr)
        print(out.returncode)
    else:
        print("cal_enetrgc. Ran SuccessFully")
        print(out.stdout)

def Arrangetest_srl():
    global   ffysrl , tsrl, temptrain_srl , temptrain_srl_rf , temptrain_srl_y
    df_y = pd.read_csv(ffysrl,usecols=[1])
    df_y = df_y.rename(columns = df_y.iloc[0])  #Rename First Row as Header
    df_y = df_y.iloc[1:,:]  #Remove First Rows
    df_y.to_csv(temptrain_srl_y,index=False) #save as csv
   
    df_x = pd.read_csv(tsrl)
    df_x = df_x.iloc[:,1:]
    df_x = df_x.rename(columns = df_x.iloc[0])
    df_x = df_x.iloc[1:,:]
    
    df_x.to_csv(temptrain_srl_rf,index =False)
    merge = pd.concat([df_y,df_x], axis=1)
    merge.to_csv(temptrain_srl)
    print("arrange test_srl Finished")


def cal_enet_srl():
    print("Cal_enet_srl")
    global temp_train_par_srl , temptrain_srl_y , temptrain_srl_rf ,enet_srl
    
    #print(temp_train_par_srl , temptrain_srl_y , temptrain_srl_rf ,enet_srl)
    #print(type(temp_train_par_srl),type(temptrain_srl_y),type(temptrain_srl_rf),type(enet_srl))
    
    cmd = ['Rscript', 'cal_enetsrl.R',temp_train_par_srl,temptrain_srl_y,temptrain_srl_rf,enet_srl]
    out = subprocess.run(cmd,shell=True,capture_output =True, text=True)
    if out.returncode !=0:
        print("Error rises")
        print(out.stderr)
        print(out.returncode)
    else:
        print("cal_enetrgc. Ran SuccessFully")
        print(out.stdout)

def Cal_Cor_new():
    global enet_rgc , enet_srl
    df1 = pd.read_csv(enet_srl,usecols=["final_enet"])
    df2 = pd.read_csv(enet_rgc,usecols =["final_enet","V1"])
    df1 = pd.concat([df1,df2],axis=1)
    #Renaming The Column Name to Avoid Conflict
    df1.columns = ['final_enet', 'final_enet_1', 'Standard FF']
    df1["Predicted"]= (df1["final_enet"]+df1["final_enet_1"])/2#Creating Average of Both
    df1 = df1.iloc[:,2:]
    Correlation  = stats.pearsonr(df1["Standard FF"],df1.Predicted)[0] #Calculating Correlation
    df1 = df1.append(pd.Series(["Correlation",Correlation],index = df1.columns),ignore_index=True)
    df1.to_csv("Correlation.csv",sep ="\t")
    
def CalCor():
    global enet_rgc , enet_srl
    sp1 = {}
    ip = enet_rgc
    input = open(ip,'r')
    check = 0
    for line in input:
        arr = str.split(line,',')
        if check > 0:
           key = check
           if key not in sp1:
                sp1[key] = []
           sp1[key].append(float(arr[2][:-1]))
           sp1[key].append(float(arr[1]))
        check += 1

    sp2 = {}
    ip = enet_srl
    input = open(ip,'r')
    check = 0
    for line in input:
        #pdb.set_trace()
        arr = str.split(line,',')
        if check > 0:
           key = check
           if key not in sp2 :
                sp2[key] = []
           sp2[key].append(float(arr[2][:-1]))
           sp2[key].append(float(arr[1]))
        check += 1

    output = open("corr_out.csv", 'a')
    output.write('Number'+'\t'+'Standard FF'+'\t'+'Predicted FF'+'\n')
    sf = []
    cf = []
    for x in range(len(sp1)):
        sf.append(sp1[x+1][0])
        cf.append((sp1[x+1][1]+sp2[x+1][1])/2)
        output.write(str(x+1)+'\t'+str(sp1[x+1][0])+'\t'+str((sp1[x+1][1]+sp2[x+1][1])/2)+'\n')

    cor = stats.pearsonr(sf, cf)
    output.write('#########################################'+'\n')
    output.write('Correlation:'+' '+str(cor[0])+'\n')
    output.close()
if __name__ == "__main__":
    read_bin()
    get_parameter_file() #On
    Loesstest_rgc() #Run Srl Norm test
    #os.chdir("./testing/") # Need to comment if Loesstest_rgc
    Arrangetest_rgc()
    cal_enet_rgc()
    losetrain_SRL_R()
    Arrangetest_srl()
    cal_enet_srl()
    #CalCor() #R 
    Cal_Cor_new() #Python
    
