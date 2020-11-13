#!/bin/python3
# author : Krish Adhikari
# Address : krishdb38@gmail.com

"""
This is python Version3 program, which search ["High","FAIL","Re-draw","Re-seqlib","Re-seq","검사불능"] 
words inside PDF file. 
This Program only run in Linux and Not in Windows.
Before Running this Program pdf2txt program must be installed in your linux system.
and also added in path

>> Method to run this Program
python3 automatic_detection.py Folder_name 

Folder_name contains pdf files

Limitation of This Program:
--> Since the Pdf File is not arranged Properly, it is difficult to extract FF From PDf File
-- > if needed we can think 

Patterns can be changed inside list item

Any kinds of Bugs Or Errors are welcome

"""
import subprocess
import sys
import os
import re


def pdf_to_text(pdf_file):
    #print("Reading text file of",pdf_file)
    process = subprocess.Popen(["pdf2txt",pdf_file],stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    stdout, stderr = process.communicate()

    if process.returncode != 0 or stderr:
        raise OSError("Executing the command for {} caused an error:\nCode:{}\
        \nOutput:{}\nError:{}".format(pdf_file,process.returncode, stdout,stderr))

    #print(stdout.count("High"))

    return stdout.decode("utf-8")


def write_result(regex):
    try:
        result.write("\t" + regex[0])
    except IndexError:
        result.write("\t" + str(regex))

folder = sys.argv[1]
# check weather given Folder exists or Not in Current Directory
result = open(folder + "_result.txt","w")
if os.path.isdir(folder):
    print("Folder Exist in Current directory")
    result.write(folder)
    pdf_files = os.listdir(folder)
    
    print(pdf_files)
    
    ## The list of Words We want to see in Pdf Files are
    patterns = ["High","FAIL","Re-draw","Re-seqlib","Re-seq","검사불능","Critical"]

    for file in pdf_files:
        if file[-3:] =="pdf":
            # print(file)
            print("DOing\t",file)
            result.write("\n" + file)
            std_out = pdf_to_text(folder+"/" + file)

            # GC & Fetal Fraction using Regular Expression
            string = std_out.replace("\n","")
            with open(file+".txt","w") as test:
                # To save all file as text
                test.write(std_out)

            gc = re.findall(r"GC \(%\)\d+\.\d+", string)
            ff = re.findall(r"Fetal fraction\(%\)\d+\.\d+",string)
            read_count = re.findall(r"Unique Reads\(bp\)\d+.....\d+", string)
            fetal = re.findall(r"No. of fetus +[a-zA-Z]+", string.replace("\n"," "))
            
            write_result(gc)
            write_result(ff)
            write_result(read_count)
            write_result(fetal)


            print(gc, ff, file)


            for pattern in patterns:
                print(pattern +"\t" + str(std_out.count(pattern)))
                result.write("\t" + pattern +":\t" + str(std_out.count(pattern)))

    result.close()
else:
    print("Please Check the Folder Name You passed is in same directory or Not")

print(folder)