'''
This module provides user-changeable options in the file
options.text
'''
import interface as intf
from interface import pyCaveOptions
FILENAME = '../options.txt'

def parseLine(line):
    line = line.strip()
    
    if line == '':
        return
    
    if line[0] == '#':
        return
    
    ls = line.split()
    
    if len(ls)!=2:
        print "Error: Must provide pairs"
        return 

    for i in [n*2 for n in range(len(ls)/2)]: #0,2,4,...
        param = ls[i]
        valueStr = ls[i+1]
        if valueStr[0] == '#':
           pass 
        if valueStr == 'True':
            value = True
        elif valueStr == 'False':
            value = False
        elif valueStr[0] == 's':  #support for string prefixing 's'
            value = valueStr[1:]
        elif valueStr.isdigit():
            value = int(valueStr)
        
        else:
            print 'Error: qUnknown value', valueStr
            return
                
    return param,value

def readOpts():
    try:
        fo = open(FILENAME)
        lines = fo.readlines()
        for line in lines:
            result = parseLine(line)
            if result:
                (param,value) = result
                intf.pyCaveOptions[param] = value            
        fo.close()
    except :
        print "Warning: Options file not found"


