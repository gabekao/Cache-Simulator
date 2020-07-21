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
import queue

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

        #print("Address : " + hex(address))
        #print(" Index : " + hex(index) + " Tag : " + hex(tag) + " Offset : " + hex(offset))

        inCache = self.data[index].keys()

        #print(len(inCache))
        if (tag not in self.data[index]) and (len(self.data[index]) < self.associativity):
            self.data[index][tag] = Block(self.blockSize, currentCycle, offset)
            compMiss += 1
            # TODO: This never gets past 1-block filling a row. Needs a fix. 
        elif (tag not in self.data[index]) and (len(self.data[index]) >= self.associativity):
            if WF.replPol == "RR":
                # Just realized LRU is basically RR except reads can update the last used time. 
                # Both RR and LRU will look for min clock but LRU will adjust blocks read with newer clocks.
                debugVar = 0
            if WF.replPol == "RND":
                #print(random.choice(list(self.data[index])))
                self.data[index][random.choice(list(self.data[index]))] = Block(self.blockSize, currentCycle, offset)
            collMiss += 1
        else:
            hits += 1
            
        totalAccess += 1
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
    WF.IMSkb = float((WF.overhead / 2**10) + WF.cacheSize)
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
    clock = 0
    cacheSim = Cache(WF)
    q1 = queue.Queue(2)
    with open(WF.filename, 'r') as fp:
        clock += 1
        for line in fp:
            if "EIP" in line:
                readSize = line[5:7]
                q1.put(readSize)
                address = int("0x" + line[10:18], 16)
                cacheSim.read(address, readSize, clock)
            elif "dstM" in line:
                if q1.qsize() < 2:
                    continue
                rwSize = q1.get()
                writeAdd = int("0x" + line[6:14], 16)
                readAdd = int("0x" + line[33:41], 16)
                if writeAdd != 0:
                    cacheSim.read(writeAdd, rwSize, clock)
                    # TODO: Needs a way to skip to write immediately. 
                if readAdd != 0:
                    cacheSim.read(readAdd, rwSize, clock)
                else:
                    continue #🐛🐜
            else: #blank line
                continue
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
















































"""
                                                            ``.,:;;;;;;;:,``                                                                          
                                                      .:*#nxW@@@@@WWWWWWW@@@Mn+i,                                                                     
                                                  .izM@@Wxz#*i::,,,,,,,,,,,:i*#nWWz*.                                                                 
                                               `;nW@Mz*;,,,::::::::::::::::::::,,;+x@x*`                                                              
                                              ix@x+;,::::::::::::::::::::::::::::::,:+MW+`                                                            
                                            :xW#:,::::::::::::::::::::::::::::::::::::,*MW*`                                                          
                                          .zW+:::::::::::::::::::::::::::::::::::::::::::#Wx,                                                         
                                         :Wn:::::,,:::::::::::::::::::::::::::::::::::::::;MW:                                                        
                                       `+W*,:::,,..,::::::::::::::::::::::::::::::::::::::::xW;`                                                      
                                      `zM;::,,,....,::::::::::::::::::::::::::::::::::::::::,nW,                                                      
                                     `nM;:::,,....,,::::::::::::::::::::::::::::::::::::::::::xx`                                                     
                                    `nM::::,.....,:::::::::::::::::::::::::::::::::::::::::::::W+                                                     
                                    zW;:::,.....,::::::::::::::::::::::::::::::::::::::::::::::iW,                                                    
                                   *@*:::,....,,:::::::::::::::::::::::::::::::::::::::::::::::,nn                                                    
                                  ,Wz,::,....,,:::::::::::::::::::::::::::::::::*:::::::::::::::i@,                                                   
                                  nW::::,...,,:::::::::::::::::::::::::::::::::,n:::::::::::::::,M+                                                   
                                 :@+::::,..,::::::::::::::::::::::::::::::::::::;z:::::::::::::::#x                                                   
                                 #W:::::,,,,::::::::::::::::::::::::::::::::::::,x:::::::::::::::;@`                                                  
                                 W#::::::::::::::::::i;::::::::::::::::::::::::::#i::::::::::::::,W,                                                  
                                :@:::::::::::::::::::;Mi:::::::::::::::::::::::::i+::::::::::::::,z;                                                  
                                #x,::::::::::::::::::::Mi::::::::::::::::::::::::;z:::::::::::::::++                                                  
                                x+:::::::::::::::::::::;W:::::::::::::::::::::::::z,::::::::::::::i#                                                  
                               `Wi::::::::::::::::::::::+n,::::::::::::::::::::,::z,::::::::::::::;#                                                  
                               ,@,::::::::::::::::::::::,Mi:::::::::::::::::::,z::+,:i:::::::::::::z                                                  
                               iW,:::::::::::::::::::::::in,:::::::::::::::::::#+::::x,:::::::::::;n                                                  
                               #n,:::::::::::::::::::::::ix,::::::::::::::::::::n,::+*::::::::::::;M                                                  
                               z#::::::::::::::::::::::::##::::::::::::::::::::,z::,n,::::::::::::;@,                                                 
                               x+:::::::::::::::::::::::,W::::::::::::::::::::::i*:,n::::::::::::::Mx.                                                
                               M*:::::::::::::::::::::::n+::::::::::::::::::::::,z:i#:::::::::::::::xn                                                
                               Wi::::::::::::::::::::::n#,::::::::::::::::::::::,x,i+::::::::::::::::Wi                                               
                               W;:::::::::::::::::::::+z,:::::::::::::::::::::::,x,i#::::::::::::::::+n                                               
                               W;::::::::::::::::::::,M:::::::::::::::::::::::::i#:,n,:::::::::::::::;M                                               
                               W;::::::::::::::::::::,M,::::::::::::::::::;::::,zi::z*::::::::::::::::M`                                              
                               Wi::::::::::::::::::::,M,:::::::::::::::::zW:::::x,:::i::,::::::::::::*n                                               
                               M*:::::::::::::::::::::zi:::::::::::::::+MW:,::::,::::::,z:::::::::::,ni                                               
                               n#::::::::::::::::::::::M::::::::,,::izM#:ix+:::::::::::,#M:::::::::::M`                                               
                               zn::::::::::::::::::::::i*::::::*MW@Wn*::::,+x::::::zi,*n**x+:,,,:::,ni                                                
                               *M,:::::::::::::::::::::::::::::,;Mi,:::,::::;x,:::,x,#+,::,izWWz,:,z#                                                 
                               i@:::::::::::::::::::::::::;::::,x;:,::i***;:,++::::Wx;::::::::zi::+n                                                  
                               .@*::::::::::::::::::::::::Mi,,::x;#n#+MMMMzznix,:::@*,:*###*i,,x,,M;                                                  
                               `Mn,::::::::::::::::::::::::nMx*iWz:..,xxxx+.,#n,:::@inni:xxxMzznz*W.                                                  
                                zW:::::::::::::::::::::::::,,,::x.....#Mxx:..+*:::,nn:..,MxMM;,n##W                                                   
                                ;@*::::::::::::::::::::::::#zi:,z*.....;i,..;x,:::::M*...*MM#.,xn#@                                                   
                                 xx,::::::::::::::::::::::,:,,:::x*........:M::::::::zn.......+i;iM:                                                  
                                 iW;:::::::::::::::::,:::::::::::,zni,,,,:#M#,:::::::,x,....,#+,::*M,                                                 
                                 `Mz::::::::::::::::n::::::::::::::;+nxxxn*z+:::::::::##*i*#z;,:::,#M`                                                
                                  *@;::::::::::::::+;::::::::::::::::,,,,,##,:::::::::#+;;;,,::::::,x+                                                
                                  `Mx:::::::::::::,#,:::::::::::::::::,,;n#,::::::::::+nn*ii::::::::*M                                                
                                   :@#,:::::::::::ii::::::::::::::::,#zMn;::::::::::::#+,*++::::::::i@                                                
                                    +@*:::::::::::+:::::::::::::::::,ii:::::::::::::::#*::::::::::::iM                                                
                                     z@*,:::::::::+::::::::::::::::::::::::::::::::::,x:::::::::::::+z                                                
                                     `+W#,::::::::ii:::::::::::::::::::::::::::::::::,W,:::::::::::,ni                                                
                                       ;Mx::::::::,#:::::::::::::::::::::::::::::::::;x,:::::::::::;W`                                                
                                        `#W+:::::::+;::::::::::::::::::::::::::::::::*z::::::::::::M*`                                                
                                          ,nM+:,::::z:::::::::::::::::::::W;:::::::::*M:::::::::::xz`                                                 
                                            :nWz*,,::z::::::::::::::::::,nz,:::::::::ixx:::::::::Mn`                                                  
                                              ,zW@+:::z;::::::::::::::::*M:::::::::::;z#z,:::::;Wz`                                                   
                                                `zn::::M#:,:::::::::::::W+:,,:::::::::x;x,::::*W+`                                                    
                                                 ##:::,Wzzn#*ii;,::::::#@;;Mx+,::::::,x+#:::,#W; `                                                    
                                                 x*::::W+:,;*+##x,:::::Wxx;M:z*:::::::#M+:::+M.                                                       
                                                .W:::::W*::::::,M,::::#n,#;*z,xi::::::z;n,:,M;`                                                       
                                                ;x,:::;@i::::::,M,::::W;::::,::M;:::,in,n:,,M,                                                        
                                                z+::::i@;::::::,M,:::*x,:::::::iMz#zn*::z*:,W.                                                        
                                               .@;::::*W:::::::,M,::,n+:::::::::,:;:,,::+#:,W`                                                        
                                               zx,::::+W,::::::,M,::,@;::::::::,,:::::::*z:,W`                                                        
                                              ,W+:::::+M,:::::::M,::iW,::::::,+x#,,*#:::iz:,W                                                         
                                              #W,:::::zx,::::::,;:::#z:::::::nn;*xM#*x::;+:,@                                                         
                                             `W+::::::nn,:::::::::::n+:::::,nn:::::::iz,::::@                                                         
                                             *M::::::,xz:::::::::::,Mi::::,nz:::;:::;:x:::::@                                                         
                                            .W*::::::,M#:::::::::::,M::::;x#:::#M,,#*:i#::::@                                                         
                                        ```,xx:::::::,W*::::::::::::;::::W#**+nWMnnxx#z#::::@                                                         
                               `:i+#nxxMMWM@W;:::::::,@*::::::::::::,::::+Wnz#i,:+i,:;x;::::@                                                         
                           ,izx@@WxxnMx;,,,z#:::::::::@;::::::::::::::::::#x:::::::::;x,::::@                                                         
                       `,+xWWMnz####nx,,::*M:::::::::;@:::::::::::::::::::,n#::::::::ni:::::@                                                         
                     .*x@Wxn#######zM:::::Wi:::::::::i@::::::::::::::::::::,n#,::::,zn,:::::W                                                         
                  `;n@Wxz+#########Wi::::nz::::::::::*M,::::::::::::::::::::,#Wx##zM#,::::::W                                                         
               `,+MWxz############xn,::::;:::::::::::*M,:::::::::::::::::::::,:i*+i,::::::::M                                                         
             `:zWMn##+############Wi:::::::::::::::::+x,::::::::::::::::::::::;:,,::::::::::M                                                         
            ;x@Mz################zM,:::::::::::::::::#n,::::::::::::::::::::::ixxxxi::::::::M                                                         
         `ixWx###################x#::::::::::::::::::#n:::::::::::::::::::::::::,,::::::::::@,                                                        
       `;xWMz###################+Wi::::::::::::::::::#x,::::::::::::::::::::::::::::::::::::*M#,                                                      
     `,nWMz######################@:::::::::::::::::::*W:::::::::::::::::::::::,+##+i:,:::::::,*W:                                                     
    `+@Wn########################M,:::::::::::::::::::W#:::::::::::::::::::::::;i*+zMn:::::::::*n                                                     
   ,x@n#########################zM,:::::::::::::::::::*Wi::::::::::::::::::::::::::,,#x,:::::::,M`                                                    
  iWM###########################zM,:::::::::::::::::::,#W*,::::::::::::::::::::::::::,xi:::::::,M`                                                    
`#Wn############################zM,::::::::::::::::::::,+Wz:::::::::::::::::::::::::::*#::::::::n.                                                    
xWz##############################W,:::::::::::::::::::::,iMW+::::::::::::::::::::::::::n,:::::::nz`                                                   
M################################@::::::::::::::::::::::::,+WM*,::::::::::::::::::::::,x,::::::,WM#                                                   
#####znnnnnz#####################@;::::::::::::::::::::::::::#WM*,:::::::::::::::::::::n,::::,;Mn#M;                                                  
#nMW@WWMMMWW@WMn#################M*::::::::::::::::::::::::::::+MW#;,:::::::::::::::::i#,::,inWz##zWz;``                                              
@Mxzz##+++##znMWWx###############nz,::::::::::::::::::::::::::::,in@x+:,:::::::::::::,n*;*zM@x#####x@Wx;`                                             
################nWWn#############zM,::::::::::::::::::::::::::::::,:+M@n+:,::::::::,:#@MWnnz+#######W+nWn.                                            
##################x@M#############W;:::::::::::::::::::::::::::::::::,;#M@x+;:,,,:izWz:;W###########n###xM;``                                         
###################zMWz###########x#::::::::::::::::::::::::::::::::::::,;+@WWMMWWx#:,:;W################zW*`                                         
#####################MWz###########W,:::::::::::::::::::::::::::::::::::::,M,,::,,,::::;M##################Wi                                         
######################xWz##########x+,::::++:,::::::::::::::::::::::::::::ix,:,::::::::ix###################W;                                        
#######################xW###########W;::,xiin:::::::::::::::::::::::::::::x+::::::::,:,zz###################zW.                                       
########################MM##########nM:,,x,::n,:::::::::::::::::::::::,:+Wz,:::::::::::W+####################xn                                       
#########################Wx##########Mn,,zz+:#::::::::::::::::::::::::+Mz;,::::::::::,nz######################W;                                      
#########################zWz##########W*::;i:#:,,,::::::::::::::::::::,,,::::::::::::*x#######################nx`                                     
#########################+xM###########W;:::,n,*xn*:::::::::::::::::::::::::::::::::iM#########################W;                                     
###########################Wz##########zM:,:z*;x,,n,:::::::::::::::::::::::::::::::iM##########################nn                                     
###########################nM###########zx;x+:#+::+;::::::::::::::,,:::::::::::,:,*M############################W`                                    
############################Wz###########nW+,,x:*,z:*+:::::;+;::::#xi::::::::::,:*M#############################M:                    
"""