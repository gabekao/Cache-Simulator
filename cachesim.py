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

class fileInfo(object):
    filename = ""
    cacheSize = 0
    blockSize = 0
    associativity = 0
    replPol = ""
    replPolStr = ""

def processArgs():
    currentFile = fileInfo()
    if '-f' in sys.argv:
        currentFile.filename = sys.argv[sys.argv.index('-f')+1]
    if '-s' in sys.argv:
        currentFile.cacheSize = sys.argv[sys.argv.index('-s')+1]
    if '-b' in sys.argv:
        currentFile.blockSize = sys.argv[sys.argv.index('-b')+1]
    if '-a' in sys.argv:
        currentFile.associativity = sys.argv[sys.argv.index('-a')+1]
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

# Print header
print("Cache Simulator CS 3853 Summer 2020 Group #TBD")
workingFile = processArgs()
print("Trace File: " + workingFile.filename)
print("***** Cache Input Parameters ****")
print("Cache Size:\t\t" + workingFile.cacheSize + " KB")
print("Block Size:\t\t" + workingFile.blockSize + " Bytes")
print("Associativity:\t\t" + workingFile.associativity)
print("Replacement Policy:\t" + workingFile.replPolStr)