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

# Decl. global vars
totalAccess = 0 #DEBUG
hits = 0
compMiss = 0
capMiss = 0
collMiss = 0
debugVar = 0
currentCycle = 0

# Decl. objects
class fileInfo(object):
    filename = ""
    cacheSize = 0
    blockSize = 0
    assoc = 0
    totalRows = 0
    replPol = ""
    replPolStr = ""
    offsetSize = 0
    totalBlocks = 0
    indexSize = 0
    tagSize = 0
    overhead = 0
    IMSkb = 0
    IMSbytes = 0
    cost = 0

# TEAM: This is the new structure/framework for the cache I'm implementing. I didn't
# take out the old one yet just in case this is a bust for whatever reason. When
# referencing the cache, use the self value. 
class Cache:
    def __init__(self, WF):
        # Parameters for initialization
        self.blockSize = WF.blockSize
        self.totalBlocks = WF.totalBlocks
        self.associativity = WF.assoc
        self.replPol = WF.replPol
        self.totalSets = WF.totalRows # This is just the rows. The 'total set' of blocks.
        # Dictionary that holds the cache blocks.
        self.data = {}

        # Initialize the cache with the dictionaries.
        for i in range(self.totalSets):
            #index = str((i))[2:].zfill(self.totalSets)
            #
            #if index == '':
            #    index = '0'
            self.data[i] = {}   #Create a dictionary of blocks for each set
        
    def read(self, address, readSize, currentCycle):
        # We implement the read here to keep the code clean and associated
        # with our cache object.

        global compMiss
        global totalAccess
        global hits
        global capMiss
        global collMiss

        indexMask = int("0b" + WF.tagSize * "0" + (32 - WF.tagSize) * "1", 2)
        offsetMask = int("0b" + (32 - WF.offsetSize) * "0" + WF.offsetSize * "1", 2)
        tag = (address >> (WF.tagSize + WF.offsetSize))
        index = ((address & indexMask) >> WF.offsetSize)
        offset = (address & offsetMask)

        # TODO: Implement replacement policies.

        inCache = self.data[index].keys()

        # When there's space in the set, add this block to it.
        if len(self.data[index]) > 2:
            print("fucking finally")

        if len(self.data[index]) < self.associativity:
            self.data[index][tag] = Block(self.blockSize, currentCycle, address)
            compMiss += 1
        elif (tag not in self.data[index]) and (len(self.data[index]) > self.associativity):
            if WF.replPol == "RR":
                #self.data[index][random.choice()]
                # Handle replacement policies here.
                debugVar = 0
            if WF.replPol == "RND":
                print("yeeyee")
        else:
            totalAccess += 1
            hits += 1
            
        return

    def write(self, address, currentCycle):
        # Same as before, keeping it assoc with the obj.
        # TODO: Parse the address given for read into the index,
        # tag, and the offset.
        # TODO: Implement replacement policies.
        index = 0
        tag = 0
        offSet = 0
        # Get the tags in this set
        inCache = self.data[index].keys()

        # Check if the tag is in the cache set.
        if tag in inCache:
            self.data[index][tag].write(currentCycle)
            # Then the call was a hit.
        elif len(inCache) < self.associativity:
            # If there is space in this set, create a new block and set its dirty bit to true if this write is coming from the CPU
            self.data[index][tag] = Block(self.blockSize, currentCycle, address)

        else:
            # Handle replacement policies here.
            debugVar = 0
        return

# Create block obj to populate our 'cache'.
class Block:
    def __init__(self, blockSize, currentCycle, address):
        self.size = blockSize
        self.inUse = False
        self.lastAccess = currentCycle
        self.address = address
    # Check if the block is empty.
    def is_empty(self):
        return self.inUse
    # Write to block.
    def write(self, currentCycle):
        self.inUse = True
        self.lastAccess = currentCycle
    # Empty the block.
    def empty(self):
        self.inUse = False
        self.address = 0
    # Read from block
    def read(self, currentCycle):
        self.lastAccess = currentCycle

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

def calculateArgs(WF):
    WF.offsetSize = int(math.log2(WF.blockSize))
    WF.totalRows = int((WF.cacheSize * 2**10) / (WF.blockSize * WF.assoc))
    WF.totalBlocks = WF.totalRows * WF.assoc
    WF.indexSize = int(math.log2(WF.totalRows))
    WF.tagSize = int(32 - WF.indexSize - WF.offsetSize)
    WF.overhead = int(WF.assoc * (1 + WF.tagSize) * WF.totalRows / 8)
    WF.IMSkb = int((WF.overhead / 2**10) + WF.cacheSize)
    WF.IMSbytes = int(WF.IMSkb * 2**10)
    WF.cost = "{:.2f}".format(WF.IMSkb * 0.07)
    return WF

#setting dict vals to object 
WF = processArgs()
WF = calculateArgs(WF)

class blockInfo(object):
    addressList = ['0']
    blocksize = WF.blockSize

# Print header
print("\nCache Simulator CS 3853 Summer 2020 - Group #9")
print()
print("Trace File: " + WF.filename)
print()
print("***** Cache Input Parameters ****")
print("Cache Size:\t\t\t" + str(WF.cacheSize) + " KB")
print("Block Size:\t\t\t" + str(WF.blockSize) + " Bytes")
print("Associativity:\t\t\t" + str(WF.assoc))
print("Replacement Policy:\t\t" + str(WF.replPolStr))
print()
print("***** Cache Calculate Values *****")
print()
print("Total # Blocks:\t\t\t" + str((WF.totalBlocks)))
print("Tag Size:\t\t\t" + str((WF.tagSize)) + " bits")
print("Index Size:\t\t\t" + str((WF.indexSize)) + " bits")
print("Total # Rows:\t\t\t" + str((WF.totalRows)))
print("Overhead Size:\t\t\t" + str((WF.overhead)) + " bytes")
print("Implementation Memory Size:\t" + str((WF.IMSkb)) + " KB (" + str((WF.IMSbytes)) + " bytes)")
print("Cost:\t\t\t\t" + "$" + str(WF.cost) + "\n")

# Reads text file and then runs the cache simulation
def runSim(WF):
    counter = 0
    cacheSim = Cache(WF)
    with open(WF.filename, 'r') as fp:
        counter += 1
        for line in fp:
            if "EIP" in line:
                readSize = line[5:7]
                address = int("0x" + line[10:18], 16)
                cacheSim.read(address, readSize, counter)
                """
                      ▄      ▄    
                      ▐▒▀▄▄▄▄▀▒▌   
                    ▄▀▒▒▒▒▒▒▒▒▓▀▄  
                  ▄▀░█░░░░█░░▒▒▒▐  
                  ▌░░░░░░░░░░░▒▒▐  
                 ▐▒░██▒▒░░░░░░░▒▐  
                 ▐▒░▓▓▒▒▒░░░░░░▄▀  
                  ▀▄░▀▀▀▀░░░░▄▀    
                    ▀▀▄▄▄▄▄▀▀    
                """
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

runSim(WF)
hitRate = round(((hits/totalAccess)*100), 2)
missRate = round((((compMiss + capMiss)/totalAccess)*100), 2)
# Print header
print("***** Cache Simulation Results *****")
print("Total Cache Accesses\t\t" + str(totalAccess))
print("Cache Hits\t\t\t" + str(hits))
print("Cache Misses\t\t\t" + str(compMiss + capMiss + collMiss))
print("--- Compulsory Misses:\t\t" + str(compMiss))
print("--- Conflict Misses:\t\t" + str(collMiss) + "\n")
print("***** ***** CACHE HIT & MISS RATE: ***** *****")
print("Hit Rate:\t\t" + str(hitRate) + "%")
print("Miss Rate:\t\t" + str(missRate) + "%")
print("CPI:\t\t\t" + str(int(debugVar)) + " Cycles/Instruction")
print("Unused Cache Space:\t" + str(int(debugVar)) + " KB / " + str(debugVar) + " KB = " + str(debugVar) + "% Waste: $" + str(debugVar))
print("Unused Cache Blocks:\t" + str(int(debugVar)) + " / " + str(debugVar))
print()