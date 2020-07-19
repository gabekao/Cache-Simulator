################################################
# Cache Sim Project by Group 9                 #
# Members: Zack Ulloa, Gabriel Kao, Mimi Huynh #
# Class CS3853                                 #
################################################
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import math

class fileInfo(object):
    filename = ""
    cacheSize = 0
    blockSize = 0
    assoc = 0
    replPol = ""
    replPolStr = ""

#defining valid parameter vals
values = {"-f": "", "-s":0, "-b":0, "-a":0, "-r":"", "replPolStr":""}
    
#assigning input vals to the dict
myiter = iter(range(1, len(sys.argv)))
for i in myiter:
    if sys.argv[i] in values:
        values[sys.argv[i]] = sys.argv[i+1]
        next(myiter, None)
  
#setting replPolStr
if values["-r"] == "RR": values["replPolStr"] = "Round Robin"
if values["-r"] == "RND": values["replPolStr"] = "Random"
if values["-r"] == "LRU": values["replPolStr"] = "Least Recently Used"
    
#setting dict vals to object 
workingFile = fileInfo()
workingFile.filename = values["-f"]
workingFile.cacheSize = int(values["-s"])
workingFile.blockSize = int(values["-b"])
workingFile.assoc = int(values["-a"])
workingFile.replPol = values["-r"]
workingFile.replPolStr = values["replPolStr"]

offsetBits = math.log2(workingFile.blockSize)
totalRows = (workingFile.cacheSize * 2**10) / (workingFile.blockSize * workingFile.assoc)
totalBlocks = totalRows * workingFile.assoc
indexSize = math.log2(totalRows)
tagSize = 32 - indexSize - offsetBits
overhead = workingFile.assoc * (1 + tagSize) * totalRows / 8
IMSkb = (overhead / 2**10) + workingFile.cacheSize
IMSbytes = IMSkb * 2**10
cost = "{:.2f}".format(IMSkb * 0.07)

debugVar = 0
testAccess = -totalBlocks

#def main(): 
with open(workingFile.filename, 'r') as fp:
    for line in fp:
        if "EIP" in line:
            readSize = line[5:7]
            address = line[10:18]
            if int(readSize) + int(("0x" + line[17]), 16) > 15: #sample extra-block increment
                testAccess += 2
            else: 
                testAccess += 1
            #👁👄👁
        elif "dstM" in line:
            writeAdd = str(line[6:14])
            readAdd = str(line[33:41])
            if writeAdd == "00000000" and readAdd == "00000000":
                continue #don't process if it's empty  ?
            else:
                testAccess += 1
        else: #blank line
            continue

# Print header
print("***** Cache Simulation Results *****")
print("Total Cache Accesses\t\t" + str(testAccess))
print("Cache Hits\t\t\t" + str(debugVar))
print("Cache Misses\t\t\t" + str(debugVar))
print("--- Compulsory Misses:\t\t" + str(debugVar))
print("--- Conflict Misses:\n")
print("***** ***** CACHE HIT & MISS RATE: ***** *****")
print("Hit Rate:\t\t" + str(int(debugVar)) + "%")
print("Miss Rate:\t\t" + str(int(debugVar)) + "%")
print("CPI:\t\t\t" + str(int(debugVar)) + " Cycles/Instruction")
print("Unused Cache Space:\t" + str(int(debugVar)) + " KB / " + str(debugVar) + " KB = " + str(debugVar) + "% Waste: $" + str(debugVar))
print("Unused Cache Blocks:\t" + str(int(debugVar)) + " / " + str(debugVar))
print()

#main()