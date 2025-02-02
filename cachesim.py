################################################
# Cache Sim Project by Group 9                 #
# Members: Zack Ulloa, Gabriel Kao, Mimi Huynh #
# Version: 1.0                                 #
# Date: 07/07/2020                             #
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

def cachesimPrint():
    print("***** Cache Simulation Results *****")
    print("Total Cache Accesses\t\t" + str(debugVar))
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
    return

workingFile = processArgs()
offsetBits = math.log2(workingFile.blockSize)
totalRows = (workingFile.cacheSize * 2**10) / (workingFile.blockSize * workingFile.assoc)
totalBlocks = totalRows * workingFile.assoc
indexSize = math.log2(totalRows)
tagSize = 32 - indexSize - offsetBits
overhead = workingFile.assoc * (1 + tagSize) * totalRows / 8
IMSkb = (overhead / 2**10) + workingFile.cacheSize
IMSbytes = IMSkb * 2**10
cost = "{:.2f}".format(IMSkb * 0.07)

# Print header
print("\nCache Simulator CS 3853 Summer 2020 - Group #9\n\n")
print("Trace File: " + workingFile.filename + "\n")
print("***** Cache Input Parameters ****")
print("Cache Size:\t\t\t" + str(workingFile.cacheSize) + " KB")
print("Block Size:\t\t\t" + str(workingFile.blockSize) + " Bytes")
print("Associativity:\t\t\t" + str(workingFile.assoc))
print("Replacement Policy:\t\t" + str(workingFile.replPolStr) + "\n")
print("***** Cache Calculate Values ***** \n")
print("Total # Blocks:\t\t\t" + str(int(totalBlocks)))
print("Tag Size:\t\t\t" + str(int(tagSize)) + " bits")
print("Index Size:\t\t\t" + str(int(indexSize)) + " bits")
print("Total # Rows:\t\t\t" + str(int(totalRows)))
print("Overhead Size:\t\t\t" + str(int(overhead)) + " bytes")
print("Implementation Memory Size:\t" + str(int(IMSkb)) + " KB (" + str(int(IMSbytes)) + " bytes)")
print("Cost:\t\t\t\t" + "$" + str(cost) + "\n")

with open(workingFile.filename, 'r') as fp:
    for x in range(60):
        line = fp.readline()
        if x % 3 == 0:
            print("0x" + line[10:18] + ": (00" + line[5:7] + ")")
        else:
            continue
print()
fp.close()

cachesimPrint()