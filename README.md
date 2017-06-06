# Introduction
This is an extension that will allow you to run Python scripts on the fly on linux servers
The extension relies on a socket-based communication between the C extension and the Python server.
The code contained in the file ADDME.sh is responsible for launching the Python server,so it is mandatory to execute that code each time the Arma server gets started.
----------
# <i class="icon-download"></i> PREREQUISITES 

## Powershell
Most of our scripts for managing the extension processes are written in powershell, a cross platform scripting language.
You can download the binary files from its Github repo - https://github.com/PowerShell/PowerShell/releases

##### Ubuntu 16.04

    $ wget url/to/powershell.deb
    $ sudo apt-get install libunwind8 libicu55
    $ sudo dpkg -i /path/to/powershell.deb
     
    
##### Ubuntu 14.04

    $ wget url/to/powershell.deb
    $ sudo apt-get install libunwind8 libicu52
    $ sudo dpkg -i /path/to/powershell.deb
    

## Python
As the main server script for handling socket connections (and executing Python scripts) is written in Python 3, you will need to check that it is actually installed.
(Most of Linux distros do have it installed by default)


    $ sudo apt-get install python3


----------

# <i class="icon-play"></i> SETUP






## <i class="icon-folder"></i> Folder Structure

Having a good folder structure will avoid any kind of errors related to missing scripts,as right now the extension does not have any kind of exception handling, wrong paths sent to the socket server will very likely result in crashes.
You can easily obtain the following folder structure by executing setupwspace.ps1 script in the extension folder.

Below, a scheme of the needed folder structure, that you can also find on our Github repo:
```
Arma Root
│     
│
└───@armaxpy
   │   armaxpy.so
   │   armaxpy_server.py  
   │   setupwspace.ps1
   └───scripts
       │   script1.py
       │   script2.py
       │   ...
 
```
After the first start,the python server will create a new folder named 'logs', the python program will write a few of information about the incoming connections from the C extension.


----------


## <i class="icon-code"></i> Compiling from source


We may not release a compiled shared object for each modify we are doing to the C extension , that's why you may need to compile the project yourself.

#### What will I need to compile?

The only thing you will need to compile is the C extension

#### Which compiler should I install ?

You should use the gcc compiler,which comes preinstalled with most of Linux Distros

#### How can I compile?

Just run the following commands in the directory of the armaxpy.c file

    $ cd /path/to/armaxpy
    $ gcc -shared -fPIC -m32 -o armaxpy.so armaxpy.c
Then, move the shared object in the extension folder 

---------------------



# <i class="icon-info-circled"></i> Use

Currently,the extension is only accepting strings.
You can split arguments using the '&' character, the extension requires at least two arguments,but if you add more arguments they will be passed to the python script. The main two arguments are the file path and the function name, let's take an example:

![alt text](http://i.imgur.com/sapN5LR.png)

In addition,the extension is meant to have both python server and C extension on the same server.
Using external servers could lead to bad performances and several exceptions.

> **Note:** There's no exception handler in the whole process. This means that badly formatted arguments will crash the extension and the python server.

----------
