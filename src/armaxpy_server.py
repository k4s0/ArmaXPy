import sys
import socket
import threading
import socketserver
import imp
import os
import logging
import inspect

def extractParameters(stringa):
    if not type(stringa) is str:
        return stringa
    curParameter=""
    parametri = []
    for idx,item in enumerate(stringa):
        if item == '&':
            parametri.append(curParameter)
            curParameter = ""
        else:
            curParameter+=item
            if idx == (len(stringa) - 1):
                parametri.append(curParameter)
    
    return parametri
    
    
def LogStuff(step,parameters):
    logging.basicConfig(filename='./logs/armaxpy.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p')
    if step == "reqReceived":
        msg = "########## Request received for the execution of the {0} function located in the {1} file ##########".format(parameters[0],parameters[1])
    elif step == "funcExecuted":
        msg = "Function executed,infos on the returned variable \nType:{0}\nValue:{1}\nDimension:{2} Bytes".format(parameters[0],parameters[1],parameters[2])
    elif step == "fileNotExists":
        msg = "Error: The file {0} does not exists".format(parameters[0])
    elif step ==  "varSent":
        msg = "########## Variable has been sent back to C extension. End of session ##########"
    logging.debug(msg)  
    
def toLaunch(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((ip, port))
    except socket.error as e:
        s.close()
        return 0
    s.close()
    return 1
    
def delIdxs(array,idxs):
    idxs.sort(reverse=True)
    for idx in idxs:
        del array[idx]
    return array
    
def selIdxs(array,idxs):
    a=[]
    for idx in idxs:
        a.append(array[idx])
    return a
    
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        def sendBack(request,data):
            response = os.fsencode(str(data)) #Encode the string(For sending it back)
            request.sendall(response) #Send it back
            LogStuff("varSent",[])
            
        parameters = self.request.recv(1024) #Receive data
        safepar = (os.fsdecode(parameters)).replace(" ", "") #Decode the bytestring
        returns=extractParameters(safepar) #Extract parameters (Split when & is encountered)
        filePath,funcName = selIdxs(returns,[0,1]) #Return an array composed by element 0 and 1 of returns
        if os.path.isfile(filePath):
            LogStuff("reqReceived",[funcName,filePath]) #Log the path of the script and its function name
            mod = imp.load_source("mainModule", filePath) #Load the module as 'mainModule'
            import mainModule #Import the module
        else:
            LogStuff("fileNotExists",[filePath]) #Log the error
            sendBack(self.request,"ArmaXPy: Error: File does not exist") #Send back this string(TBR)
            return #Stop the execution
        
        returns = delIdxs(returns,[0,1]) #Removes elements 0-1
        if len(returns) == 1: #Does returns have a single item?
            scriptArguments = returns[0] #Select it
        elif len(returns) > 1:#Does returns have multiple items?
            scriptArguments = returns #Assign it to scriptArguments

        if 'scriptArguments' in locals():#Are there any parameters for the python function?
            command = "global data; data=mainModule.{}(scriptArguments)".format(funcName) #Format the code (With args)
        else:
            command = "global data; data=mainModule.{}()".format(funcName) #Format the code(No args)
        exec(command) #Execute the code
        LogStuff("funcExecuted",[str(type(data)),str(data),sys.getsizeof(data)]) #Log type value,value and size
        sendBack(self.request,data)



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer): #SocketServer stuff
     pass
        

if __name__ == "__main__":
    os.chdir(sys.path[0])
    HOST, PORT = "localhost", 8888
    if not(toLaunch(HOST,PORT)): #Should the py server get started?
        quit() #If not,quit
    toCreate = not(os.path.exists("./logs"))
    if (toCreate):#Create logs directory(For storing logs)
        os.makedirs("./logs")
    processID = os.getpid()
    with open("./logs/processID.txt", "w") as text_file: #Write process id of the server
        text_file.write("{}".format(processID))
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = False
    
    server_thread.start()
    print("Python server Launched!")
    
    
    
    
    #Shit nobody cares about
    #server_thread.do_run=False     Chiusura thread
    #server.shutdown()  
    #server.server_close()            
    