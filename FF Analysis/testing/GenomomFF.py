#!/usr/bin/python
# GENOMOMFF
import re
import os
import sys, getopt
import commands
from scipy import stats
import pdb


def Act1():
    cmd = 'sh act1.sh'
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

def GetNumber_rgc():
    cmd = 'wc -l GC1806N2990_R1_V1_IonXpress_088.Fastq.sam.bam.sort.bam.rmdup.bam.sam_rgc.csv > Number_rgc'
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)
    ip = 'Number_rgc'
    input = open(ip,'r')
    for line in input:
        #pdb.set_trace()
        arr = str.split(line)
    return arr[0]

def GetNumber_srl():
    cmd = 'wc -l GC1806N2990_R1_V1_IonXpress_088.Fastq.sam.bam.sort.bam.rmdup.bam.sam.srl > Number_srl'
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)
    ip = 'Number_srl'
    input = open(ip,'r')
    for line in input:
        #pdb.set_trace()
        arr = str.split(line)
    return arr[0]

def Loesstest_rgc():
    cmd = 'Rscript loessgctest.R Number_rgc'
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

def Loesstest_srl():
    cmd = 'Rscript srlnormtest.R Number_srl'
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

def Cal_enet_rgc():
    cmd = 'Rscript cal_enetrgc.R Number_rgc'                             
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

def Cal_enet_srl():
    cmd = 'Rscript cal_enetsrl.R Number_srl'
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

def CalCor():
    sp1 = {}
    ip = 'enetrgc.csv'
    input = open(ip,'r')
    check = 0
    for line in input:
        #pdb.set_trace()
        arr = str.split(line,',')
        if check > 0:
           key = check
           if not sp1.has_key(key):
                sp1[key] = []
           sp1[key].append(float(arr[2][:-1]))
           sp1[key].append(float(arr[1]))
        check += 1

    sp2 = {}
    ip = 'enetsrl.csv'
    input = open(ip,'r')
    check = 0
    for line in input:
        #pdb.set_trace()
        arr = str.split(line,',')
        if check > 0:
           key = check
           if not sp2.has_key(key):
                sp2[key] = []
           sp2[key].append(float(arr[2][:-1]))
           sp2[key].append(float(arr[1]))
        check += 1

    output = open("corr_out", 'a')
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

def Arrangetest_rgc(N):
    cmd = 'python2 arrangetest_rgc.py'
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

    cmd = "cut -f1 temptestrgc -d',' > temptestrgcy"
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

    cmd = "cut -f2-"+N+" temptestrgc -d',' > temptestrgcrf"
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

def Arrangetest_srl(N):
    cmd = 'python2 arrangetest_srl.py'
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

    cmd = "cut -f1 temptestsrl -d',' > temptestsrly"
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

    cmd = "cut -f2-"+N+" temptestsrl -d',' > temptestsrlrf"
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

def Check():
    cmd = 'ls -alh *.srl > srlist'
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)

    ip = 'srlist'
    input = open(ip,'r')
    ln = 0
    for line in input:
        #pdb.set_trace()
        arr = str.split(line)
        if len(arr[4]) > 1:
           ln += 1
    return ln

def Remove():
    cmd = 'rm *_rgc.csv *.srl *.py.*'
    (status, output) = commands.getstatusoutput(cmd)
    if status:
            sys.stderr.write(output)
            sys.exit(1)


#pdb.set_trace()   
#Act1()

check = True
while check:
      try:
         length = Check()
         if length == 900:
            check = False
         else:
             continue
      except:
            pass

Nrgc = GetNumber_rgc()
Nsrl = GetNumber_srl()
Loesstest_rgc()
Loesstest_srl()
Arrangetest_rgc(Nrgc)
Arrangetest_srl(Nsrl)
Cal_enet_rgc()
Cal_enet_srl()
CalCor()
#Remove()
