#!/usr/bin/env python
from PythonBinding import *
import os
#import lsst.eotest.sensor as sensorTest
import sys
#from lcatr.harness.helpers import dependency_glob

fileName = "/tmp/ccscmndinput"
fo = open(fileName,"w");
#print "Number of arguments = ", len(sys.argv)
fo.write(sys.argv[1]+"\n");
if (len(sys.argv)==3) :
    fo.write(sys.argv[2]+"\n");
else :
    line = sys.argv[2]+" "+sys.argv[3]+"\n"
    fo.write(line);
fo.close();

fileName = "/usr/bin/ccscmnds/procccscmnd.py"
fo = open(fileName, "r");
content = fo.read();
fo.close();

try:
#Create an instance of the python binding
    print 'connecting interpreter'
    ccs1 = CcsJythonInterpreter();
 
 
    print 'starting synch execution'
    result1 = ccs1.syncExecution(content);
    print result1.getOutput();    
 
 
except CcsException as ex:
    print 'Failure', ex

