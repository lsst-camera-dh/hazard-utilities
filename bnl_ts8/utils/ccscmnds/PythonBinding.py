#!/usr/bin/python2.7
import socket  
import threading
import time
import random
import exceptions


class CcsExecutionResult:
    def __init__(self, thread):
        self.thread = thread;

    def isRunning(self):
        return self.thread.running;

    def getOutput(self):
        while self.thread.running:
            time.sleep(0.1);
        return self.thread.executionOutput;
            

class CcsException(Exception):
    def __init__(self, value):
        self.value = value;
    def __str__(self):
        return repr(self.value);


class CcsJythonInterpreter:
    port = 4444;
    host = None;


    def __init__(self, host=None,port=4444):
        CcsJythonInterpreter.port = port;
        host = "127.0.0.1";
        print "host = %s" % host;
        if host == None:
            CcsJythonInterpreter.host = socket.gethostname() # Get local machine name
            print "found host = %s " %  CcsJythonInterpreter.host
        else:
            CcsJythonInterpreter.host = host;
        try:
            print "try to get socket connection";
            self.socketConnection = CcsJythonInterpreter.__establishSocketConnectionToCcsJythonInterpreter__();
            print 'Initialized connection to CCS Python interpreter on on host ', CcsJythonInterpreter.host,':',CcsJythonInterpreter.port;
        except :
            raise CcsException("Could not establish a connection with CCS Python Interpreter on host "+CcsJythonInterpreter.host+":"+str(CcsJythonInterpreter.port));

    @staticmethod
    def __establishSocketConnectionToCcsJythonInterpreter__():
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         s.connect((CcsJythonInterpreter.host, CcsJythonInterpreter.port))
         connectionResult = s.recv(1024);
         if "ConnectionRefused" in connectionResult:
            raise CcsException("Connection Refused ");
         return s;



#    def executeScriptFromFile(self, fileName):
#        fo = open(fileName, "r");
#        content = fo.read();
#        result = self.sendInterpreterServer(content);
#        fo.close()
#        return result;

    def aSyncExecution(self, statement):
        return self.sendInterpreterServer(statement);

    def aSyncExecution(self, fileName):
        fo = open(fileName, "r");
        fileContent = fo.read();
        fo.close();
        return self.sendInterpreterServer(fileContent);

    def syncExecution(self, statement):
        result = self.sendInterpreterServer(statement);
        output = result.getOutput();
        return result;

    def syncScriptExecution(self, fileName):
        fo = open(fileName, "r");
        fileContent = fo.read();
        fo.close();
        result = self.sendInterpreterServer(fileContent);
        output = result.getOutput();
        return result;

    def sendInterpreterServer(self, content):
        threadId = str(int(round(time.time() * 1000)))+"-"+str(random.randint(0,1000));
        thread = _CcsPythonExecutorThread(threadId,self.socketConnection);
        thread.executePythonContent(content);
        return CcsExecutionResult(thread);



class _CcsPythonExecutorThread:

    def __init__(self, threadId, s):
#        self.s = CcsJythonInterpreter.__establishSocketConnectionToCcsJythonInterpreter__();
        self.s = s;
        self.threadId = threadId;
        self.outputThread = threading.Thread(target=self.listenToSocketOutput);


    def executePythonContent(self,content):
        self.running = True;
        self.outputThread.start();        
        content = "startContent:"+self.threadId+"\n"+content+"\nendContent:"+self.threadId+"\n";
        self.s.send(content);
        return CcsExecutionResult(self);

    def listenToSocketOutput(self):
        self.executionOutput = "";
        while self.running:
            try:
                output = self.s.recv(1024)
            except:
                raise CcsException("Communication Problem with Socket");
            self.executionOutput += output
            if "doneExecution:"+self.threadId in self.executionOutput:
                self.running = False;
                self.executionOutput = self.executionOutput.replace("doneExecution:"+self.threadId+"\n","");
        self.outputThread._Thread__stop();


 
