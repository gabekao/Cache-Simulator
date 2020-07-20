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
import random
import time #🐛🐜

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

offsetSize = int(math.log2(workingFile.blockSize))
workingFile.totalRows = (workingFile.cacheSize * 2**10) / (workingFile.blockSize * workingFile.assoc)
totalBlocks = workingFile.totalRows * workingFile.assoc
indexSize = math.log2(workingFile.totalRows)
tagSize = int(32 - indexSize - offsetSize)
overhead = workingFile.assoc * (1 + tagSize) * workingFile.totalRows / 8
IMSkb = (overhead / 2**10) + workingFile.cacheSize
IMSbytes = IMSkb * 2**10
cost = "{:.2f}".format(IMSkb * 0.07)

class blockInfo(object):
    addressList = ['0']
    blocksize = workingFile.blockSize

# Print header
print("\nCache Simulator CS 3853 Summer 2020 - Group #9")
print()
print("Trace File: " + workingFile.filename)
print()
print("***** Cache Input Parameters ****")
print("Cache Size:\t\t\t" + str(workingFile.cacheSize) + " KB")
print("Block Size:\t\t\t" + str(workingFile.blockSize) + " Bytes")
print("Associativity:\t\t\t" + str(workingFile.assoc))
print("Replacement Policy:\t\t" + str(workingFile.replPolStr))
print()
print("***** Cache Calculate Values *****")
print()
print("Total # Blocks:\t\t\t" + str(int(totalBlocks)))
print("Tag Size:\t\t\t" + str(int(tagSize)) + " bits")
print("Index Size:\t\t\t" + str(int(indexSize)) + " bits")
print("Total # Rows:\t\t\t" + str(int(workingFile.totalRows)))
print("Overhead Size:\t\t\t" + str(int(overhead)) + " bytes")
print("Implementation Memory Size:\t" + str(int(IMSkb)) + " KB (" + str(int(IMSbytes)) + " bytes)")
print("Cost:\t\t\t\t" + "$" + str(cost) + "\n")
debugVar = 0

totalAccess = 0
hits = 0
compMiss = 0
capMiss = 0
collMiss = 0


# Reads text file and then runs the cache simulation
def runSim(workingFile):
    # Set up cache array
    cacheSim = [[0] * int(workingFile.assoc)] * int(workingFile.totalRows)
    #print(hex(len(cacheSim))) #🐛🐜: address range of the cache.
    #time.sleep(20) #🐛🐜: it's literally just a pause

    global totalAccess
    global hits
    global compMiss
    global capMiss
    global collMiss
    #this is probably a shitty way to do this but im lazy at 5am

    #DEBUGSET = set()#🐛🐜

    with open(workingFile.filename, 'r') as fp:
        for line in fp:
            if "EIP" in line:
                readSize = line[5:7]
                address = int("0x" + line[10:18], 16)

                indexMask = int("0b" + tagSize * "0" + (32 - tagSize) * "1", 2)
                offsetMask = int("0b" + (32 - offsetSize) * "0" + offsetSize * "1", 2)
                tagHex = (address >> (tagSize + offsetSize))
                indexHex = ((address & indexMask) >> offsetSize)
                offsetHex = (address & offsetMask)

                ##print("index is " + hex(indexHex) + " tag is " + hex(tagHex)) #🐛🐜
                #DEBUGSET.add(hex(indexHex)) #🐛🐜
                
                #HEY TEAM READ HERE 🥓⬇⬇⬇⬇⬇⬇⬇
                #can't get the implementation down fully. basically it should go like this:
                if tagHex not in cacheSim[indexHex]: #taghex not at this row, check this index for 0's. 
                    #print("indexHex is " + hex(indexHex) + " and 0 index is: " + str(cacheSim[indexHex].index(0))) #🐛🐜
                    if 0 in cacheSim[indexHex]: #if there is one, put the TAGHEX in the first 0. 
                        cacheSim[indexHex][cacheSim[indexHex].index(0)] = tagHex
                        compMiss += 1 #somehow getting very few compulsory misses. he gets 4824 comp misses. there's 1599 unique indices, so something's very wrong here.
                    else: #taghex not at this row BUT no 0's exist, check replacement policy and replace accordingly. 
                        if workingFile.replPol == "RR":
                            cacheSim[indexHex][random.randint(0, workingFile.assoc - 1)] = tagHex #RND 
                        else:
                            cacheSim[indexHex][random.randint(0, workingFile.assoc - 1)] = tagHex #NEED TO CODE THE OTHER REPLACEMENT STRAT
                        collMiss += 1
                    #print(hex(cacheSim[indexHex][0])) #🐛🐜
                elif tagHex in cacheSim[indexHex]: #tagHex in cacheSim[indexHex]:
                    #print("Address: " + hex(address) + " index: " + hex(indexHex) + " tag: " + hex(tagHex) + " was in cache: " + hex(cacheSim[indexHex][cacheSim[indexHex].index(tagHex)])) #🐛🐜
                    totalAccess += 1
                    hits += 1
                    #check the offset. not sure if i understand this right but the last hex digit won't exceed the block size(?), that being the case:
                    #if int(readSize) + int(("0x" + line[17]), 16) > workingFile.blockSize: #this checks for excess/rollover
                        # totalAccess += #(?) gonna depend on the readSize. should've found the max of them to see if it ever exceeds 2 blocks so we'll need to look
                    #else:
                        # totalAccess += 1
                #and then yeah, we just copy this onto dstM and then add the calculations accordingly. 
                #time.sleep(20) #🐛🐜 I PLACED THESE HAPHAZARDLY, GONNA HAVE TO CTRL-F EM
                #       ▄      ▄    
                #      ▐▒▀▄▄▄▄▀▒▌   
                #    ▄▀▒▒▒▒▒▒▒▒▓▀▄  
                #  ▄▀░█░░░░█░░▒▒▒▐  
                #  ▌░░░░░░░░░░░▒▒▐  
                # ▐▒░██▒▒░░░░░░░▒▐  
                # ▐▒░▓▓▒▒▒░░░░░░▄▀  
                #  ▀▄░▀▀▀▀░░░░▄▀    
                #    ▀▀▄▄▄▄▄▀▀    
                
            elif "dstM" in line:
                writeAdd = str(line[6:14])
                readAdd = str(line[33:41])
                if writeAdd == "00000000" and readAdd == "00000000":
                    continue #don't process if it's empty  ?
                else:
                    #totalAccess += 1
                    continue #🐛🐜

            else: #blank line
                continue
    #print(len(DEBUGSET)) #🐛🐜
    return

runSim(workingFile)

# Print header
print("***** Cache Simulation Results *****")
print("Total Cache Accesses\t\t" + str(totalAccess))
print("Cache Hits\t\t\t" + str(hits))
print("Cache Misses\t\t\t" + str(compMiss + capMiss + collMiss))
print("--- Compulsory Misses:\t\t" + str(compMiss))
print("--- Conflict Misses:\t\t" + str(collMiss) + "\n")
print("***** ***** CACHE HIT & MISS RATE: ***** *****")
print("Hit Rate:\t\t" + str(int(debugVar)) + "%")
print("Miss Rate:\t\t" + str(int(debugVar)) + "%")
print("CPI:\t\t\t" + str(int(debugVar)) + " Cycles/Instruction")
print("Unused Cache Space:\t" + str(int(debugVar)) + " KB / " + str(debugVar) + " KB = " + str(debugVar) + "% Waste: $" + str(debugVar))
print("Unused Cache Blocks:\t" + str(int(debugVar)) + " / " + str(debugVar))
print()
   