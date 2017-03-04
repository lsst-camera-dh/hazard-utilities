#!/usr/bin/env python
from PythonBinding import *
import os
import sys
print "sending abort script command to Jython"
try:
#Create an instance of the python binding
    ccs1 = CcsJythonInterpreter("ts");
    result = ccs1.syncExecution("abortInterpreter ts");
    print result.getOutput();    
 
 
except CcsException as ex:
    print 'Failure', ex

