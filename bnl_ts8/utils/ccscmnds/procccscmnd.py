from org.lsst.ccs.scripting import *
from java.lang import Exception

CCS.setThrowExceptions(False);


fp = open("/tmp/ccscmndinput","r");
#for line in fp:
ccssys = fp.readline();
#print "ccssys=",ccssys
if ("ts" in ccssys) :
    subsys  = CCS.attachSubsystem("ts");
if ("bias" in ccssys) :
    subsys  = CCS.attachSubsystem("ts/Bias");
#    print "attached bias subsystem"
if ("cryo" in ccssys) :
    subsys  = CCS.attachSubsystem("ts/Cryo");
if ("vac" in ccssys) :
    subsys  = CCS.attachSubsystem("ts/VacuumGauge");
if ("lamp" in ccssys) :
    subsys  = CCS.attachSubsystem("ts/Lamp");
if ("mono" in ccssys) :
    subsys  = CCS.attachSubsystem("ts/Monochromator");
if ("archon" in ccssys) :
    subsys  = CCS.attachSubsystem("archon");

line = fp.readline();
print "Processing command: ",line
result = subsys.synchCommand(30,line);
response = result.getResult();
print "response = ",response

fp.close();
