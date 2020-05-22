#/bin/python
import os
import subprocess 
from subprocess import run
#! This must be run in linux

in_path = "/BiO/Preterm/raw_data/"
# Old 20 and new 40 are different
out_path = "/BiO/Preterm/intervar_result/"
# Check for old and New


#files = [1119,910,873,1489,989,880,1282,1584,875,1009,1093,1134,1293,1316,1389,1428,1477,1481,1557,1591]
#files = ["MWB_1008",'MWB_1040','MWB_110','MWB_1151','MWB_1226','MWB_1244','MWB_1250','MWB_1276','MWB_1443','MWB_1445','MWB_161','MWB_1676','MWB_174']
files = ['MWB_1960','MWB_1964','MWB_1975','MWB_1977','MWB_1982','MWB_1995','MWB_2007','MWB_2008','MWB_242','MWB_276','MWB_437','MWB_490','MWB_506','MWB_540']
#files = ['MWB_548','MWB_564','MWB_626','MWB_719','MWB_740','MWB_746','MWB_815','MWB_870','MWB_895','MWB_911','MWB_941','MWB_956','MWB_961']



for _ in files:
    vcf_file = in_path+ str(_) +"/"+ str(_)+".PASS.vcf"

    #if vcf_file.endswith(".vcf") and len(_) <10:
        #vcf_file = _
        #name = _.split(".")[0]
        # print(name)
    try:
            # Check for the Folder exists or Not
        os.mkdir(out_path+str(_))
    except FileExistsError as e:
        pass
        
    condition = os.path.isfile(out_path+ str(_)+"/"+str(_)+".hg19_multianno.txt") # .anno.hg19_multianno.txt 
    if condition: 
        print(str(_)+"skipping\n\n")
    else:
        error_out = open(out_path+"/"+str(_)+"_error.txt","w+")

        cmd = ["python","Intervar.py", "-b","hg19", "-i", vcf_file, "--input_type", "VCF", "-o", out_path+ str(_)+"/"+ str(_)]
        print(cmd)
        print("\n\nDoing Subprocess in ", str(_))
        #process = subprocess.run(cmd,universal_newlines = True, stdout = error_out,\
        #    stderr = subprocess.PIPE, shell = False)
        #if process.stderr:
        #    print(process.stderr)
        #else:
        #    print("Success", name, "\n")
        #print(process.returncode)


print("All tasks Completed")
    # If some process already done no need to repeat so we also need to check weather processed file exists or not


#


#process = subprocess.Popen(cmd,universal_newlines = True, stdout =  subprocess.PIPE,\
#    stderr = subprocess.PIPE, shell = False)

#std_out = process.communicate()[0]

# For LInux remove shell = True

#print(out.stderr)
#print(process.returncode)
#print(process.stdout)

# We will run Foor loop later But now lets test weather the Output is correct or not
#for i in range(100):
    #os.makedirs(str(i))
    #os.removedirs(str(i))
