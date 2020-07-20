################################################
# Cache Sim Project by Group 9                 #
# Members: Zack Ulloa, Gabriel Kao, Mimi Huynh #
# Class CS3853                                 #
################################################
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import math
import array

class fileInfo(object):
    filename = ""
    cacheSize = 0
    blockSize = 0
    assoc = 0
    totalRows = 0
    replPol = ""
    replPolStr = ""    

def processArgs():
    currentFile = fileInfo()
    if '-f' in sys.argv:
        currentFile.filename = sys.argv[sys.argv.index('-f')+1]
    if '-s' in sys.argv:
        currentFile.cacheSize = int(sys.argv[sys.argv.index('-s')+1])
    if '-b' in sys.argv:
        currentFile.blockSize = int(sys.argv[sys.argv.index('-b')+1])
    if '-a' in sys.argv:
        currentFile.assoc = int(sys.argv[sys.argv.index('-a')+1])
    if '-r' in sys.argv:
        if 'RR' in sys.argv:
            currentFile.replPol = 'RR'
            currentFile.replPolStr = 'Round Robin'
        if 'RND' in sys.argv:
            currentFile.replPol = 'RND'
            currentFile.replPolStr = 'Random'
        if 'LRU' in sys.argv:
            currentFile.replPol = 'LRU'
            currentFile.replPolStr = 'Least Recently Used'
    return currentFile

#setting dict vals to object 
workingFile = processArgs()

offsetBits = math.log2(workingFile.blockSize)
workingFile.totalRows = (workingFile.cacheSize * 2**10) / (workingFile.blockSize * workingFile.assoc)
totalBlocks = workingFile.totalRows * workingFile.assoc
indexSize = math.log2(workingFile.totalRows)
tagSize = 32 - indexSize - offsetBits
overhead = workingFile.assoc * (1 + tagSize) * workingFile.totalRows / 8
IMSkb = (overhead / 2**10) + workingFile.cacheSize
IMSbytes = IMSkb * 2**10
cost = "{:.2f}".format(IMSkb * 0.07)

class blockInfo(object):
    addressList = ['0']
    blocksize = workingFile.blockSize

# Print header
print("\nCache Simulator CS 3853 Summer 2020 - Group #9")
print("Trace File: " + workingFile.filename)
print("***** Cache Input Parameters ****")
print("Cache Size:\t\t\t" + str(workingFile.cacheSize) + " KB")
print("Block Size:\t\t\t" + str(workingFile.blockSize) + " Bytes")
print("Associativity:\t\t\t" + str(workingFile.assoc))
print("Replacement Policy:\t\t" + str(workingFile.replPolStr))
print("***** Cache Calculate Values *****")
print("Total # Blocks:\t\t\t" + str(int(totalBlocks)))
print("Tag Size:\t\t\t" + str(int(tagSize)) + " bits")
print("Index Size:\t\t\t" + str(int(indexSize)) + " bits")
print("Total # Rows:\t\t\t" + str(int(workingFile.totalRows)) + " bytes")
print("Overhead Size:\t\t\t" + str(int(overhead)) + " bytes")
print("Implementation Memory Size:\t" + str(int(IMSkb)) + " KB (" + str(int(IMSbytes)) + " bytes)")
print("Cost:\t\t\t\t" + "$" + str(cost) + "\n")
debugVar = 0
testAccess = totalBlocks

# Reads text file and then runs the cache simulation
def runSim(workingFile, testAccess):
    # Set up cache array
    cachesim = [[0] * int(workingFile.assoc)] * int(workingFile.totalRows)

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
    return

runSim(workingFile, testAccess)

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