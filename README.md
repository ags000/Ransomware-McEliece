
# Install modules
> pip install pycryptodome

> pip install uuid

> pip install tk

# How to use

If you execute the following program, it is highly recommended doing it in a Virtual Machine or in a secured-system.

First, run Serverc.py. You are able to change the IP of server in Serverc.py, Ran.py and Des.py. Once the IP has changed, it is accessible from the netwrok. 
Currently, it is in localhost. So, Server and Ransomware must run in the same computer.

> python Serverc.py

Server must be running before executing the Ransomware o the Decrypt module. The idea is storing the server in one PC and the ransomware in another in order to see the whole process.

Execute ransomware:

> Python Ran.py 

Execute desencrypt:

> Python Des.py

The password is : TCYC2022


Developed with python for Windows.

You're free to generate a .exe with pyinstaller or another tool. 

> THIS IS FOR EDUCATIONAL PURPOSES ONLY!!! EXECUTE THIS CODE BY YOUR OWN RISK. WE ARE NOT responsible for accidents or damages relating to THIS CODE.

# Matrices for McEliece used

The AES key is encoded with McEliece, Ham(3,2) also known as Ham(7,4,3)  

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
