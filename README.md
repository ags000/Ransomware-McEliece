
# Install modules
> pip install pycryptodome

> pip install uuid

> pip install tk

# How to use

Please if you execute this, do it in a Virtual Machine or in a secured-system.


First, run Serverc.py in a computer. You could change the IP of server in Serverc.py, Ran.py and Des.py.
Now, it is in localhost. Server and Ransomware must run in same computer.

> python Serverc.py


Ransomware and decrypt must be executed in another. Server must be 
running.

Execute ransomware:

> Python Ran.py 

Execute desencrypt:

> Python Des.py

The password is : TCYC2022


It is made with python for Windows.

If you want to generate .exe use pyinstaller or another tool. 


> THIS IS FOR EDUCATIONAL PURPOSES ONLY!!! EXECUTE THIS CODE BY YOUR OWN RISK. WE ARE NOT responsible for accidents or damages relating to THIS CODE.

# Matrices for McEliece used

SGP = [{1,1,1,1,1,1,1},{1,1,0,0,1,0,0},{1,1,0,1,0,1,0},{0,1,0,0,1,1,1}]

S = [{1,1,1,1},{1,0,0,1},{1,1,1,0},{0,1,0,1}]
S^-1 = [{1,1,1,0}, {1,0,1,1},{0,1,1,1},{1,0,1,0}]

G = [{1,1,0,1,0,0,1},{0,1,0,1,0,1,0},{1,1,1,0,0,0,0},{1,0,0,1,1,0,0}]

P = [{0,0,0,0,0,0,1},{0,1,0,0,0,0,0},{0,0,0,1,0,0,0},{0,0,1,0,0,0,0},{0,0,0,0,1,0,0},{0,0,0,0,0,1,0},{1,0,0,0,0,0,0}]
Note: p^-1 == p

H = [{0,0,0,1,1,1,1},{0,1,1,0,0,1,1},{1,0,1,0,1,0,1}]
and its transpose.

# Authors

## Adrián Galdeano Salinas (ags000)
## Miguel Gonzalez Rodríguez (mgr369)
