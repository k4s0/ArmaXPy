$xpyPath = $PSScriptRoot

#Verifica esistenza .so
if (-Not (Test-Path "$xpyPath/armaxpy.so")) {

Invoke-WebRequest -Uri "https://gist.githubusercontent.com/DardoTheMaster/4a8507681ed5a333c186ed5b26f1c238/raw/f162ac2f388f4ca68625a64b84f1d5321dac923c/ArmaXPy.c" -OutFile "$xpyPath/armaxpy.c"
Invoke-Expression "gcc -shared -fPIC -m32 -o $xpyPath/armaxpy.so $xpyPath/armaxpy.c"

Remove-Item "$xpyPath/armaxpy.c"
}

#Verifica esistenza .pyc
if (-Not (Test-Path "$xpyPath/armaxpy_server.pyc")) {
Invoke-WebRequest -Uri "https://gist.githubusercontent.com/DardoTheMaster/ee8901d715414395ad00de9c6a05d380/raw/c469c6ccaa20025ab8c0f8526afe05ff6041d8f0/armaxpy_server.py" -OutFile "$xpyPath/armaxpy_server.py"
Invoke-Expression "python3 -m compileall $xpyPath/armaxpy_server.py -b" 
Remove-Item "$xpyPath/armaxpy_server.py"
}