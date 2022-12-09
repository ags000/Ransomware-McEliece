"""
A brief class which uses McElice encryption method. 
For example, an AES key is going be encrypted. Nevertheless, you can replace it. This method encrypts whatever you want.

Here, we encode with a matrix composed of the multiplication of three matrices (S, G and P).
So, SGP is the public key for cipher. 
The ransomware and desencryp will have to know S,G and P in order to get the msg (they are the private key).

Note: Ham(3,4) is used.

@author Adrián Galdeano (ags000). 
@contributor Miguel Gonzalez (mgr369)
"""

from Crypto.Util import number
import random


class McElice:

    # Note key_aes is a sequence of bytes. 
    def __init__(self, key_aes):
        self.key_aes = key_aes
        

    # Returns a list of lists of ciphered vectors. Each element represents a bit.
    def encode(self):
        
        # bytes ciphered
        msg_encoded = [] 


        """"
        #Uncomment this if you want to see how the bytes are encoded but no ciphered with the error vector e
        msg_codificado_sin_errores = [] # Represent the encoded text without being ciphered with error vector
        """
        # SGP is the public key of McElice method. It is form with the multiplication of a matrix S,G and P.See encryptor and decryptor for more info. 
        SGP = [[1,1,1,1,1,1,1], [1,1,0,0,1,0,0], [1,1,0,1,0,1,0], [0,1,0,0,1,1,1]]

        work_aes = self.key_aes

        # we're iterating int by int. Each int is a representation of a bit.
        for byte_read in work_aes: 
            
            # For each int, we convert it to binary.
            byte = bin(byte_read)[2:].rjust(8,'0') 

            # For each byte, we divide it in 2 blocks of 4 bits. They will be encoded.
            b1 = int(byte[0])
            b2 = int(byte[1])
            b3 = int(byte[2])
            b4 = int(byte[3])

            b5 = int(byte[4])
            b6 = int(byte[5])
            b7 = int(byte[6])
            b8 = int(byte[7])

            # We have to do m * SGP + e, where m and e are vectors and e is a vector wich contains one error.
            # m is (b1,b2,b3,b4), e could be (0,0,0,1,0,0,0)

            # Multiply m and SGP
            for i in range(0,7):

                # Operations of multiplying bits b1-b4 with the matrix.
                v1 = b1* SGP[0][i]
                v2 = b2* SGP[1][i]
                v3 = b3* SGP[2][i]
                v4 = b4* SGP[3][i]

                # Operations of multiplying bits b5-b8
                v5 = b5*SGP[0][i]
                v6 = b6*SGP[1][i]
                v7 = b7*SGP[2][i]
                v8 = b8*SGP[3][i]


                if(i == 0):
                    a0 = v1 ^ v2 ^ v3 ^ v4 
                    a02 = v5 ^ v6 ^ v7 ^ v8 
                if(i == 1):
                    a1 = v1 ^ v2 ^ v3 ^ v4
                    a12 = v5 ^ v6 ^ v7 ^ v8
                if(i==2):
                    a2 = v1 ^ v2 ^ v3 ^ v4
                    a22 = v5 ^ v6 ^ v7 ^ v8
                if(i==3):
                    a3 = v1 ^ v2 ^ v3 ^ v4
                    a32 = v5 ^ v6 ^ v7 ^ v8
                if(i == 4):
                    a4 = v1 ^ v2 ^ v3 ^ v4 
                    a42 = v5 ^ v6 ^ v7 ^ v8
                if(i == 5):
                    a5 = v1 ^ v2 ^ v3 ^ v4
                    a52 = v5 ^ v6 ^ v7 ^ v8
                if(i==6):
                    a6 = v1 ^ v2 ^ v3 ^ v4
                    a62 = v5 ^ v6 ^ v7 ^ v8

            # Once we get the components of both vectors, we have to add them to a list.

            # bits_codificados represents the first vector of the msg (b1-b4)
            bits_codificados = []
            bits_codificados.append(0) # We add 0 to first element to form a vector of 8 bits. Note that next 7 bits is the encoded msg.
            bits_codificados.append(a0)
            bits_codificados.append(a1)
            bits_codificados.append(a2)
            bits_codificados.append(a3)
            bits_codificados.append(a4)
            bits_codificados.append(a5)
            bits_codificados.append(a6)

            """""
            Uncomment this if you want to see how the bytes are encoded but no ciphered with the error vector e

            bits_codificados_b1 = []
            bits_codificados_b1.append(0) # We add 0 to first element to form a vector of 8 bits. Note that next 7 bits is the encoded msg.
            bits_codificados_b1.append(a0)
            bits_codificados_b1.append(a1)
            bits_codificados_b1.append(a2)
            bits_codificados_b1.append(a3)
            bits_codificados_b1.append(a4)
            bits_codificados_b1.append(a5)
            bits_codificados_b1.append(a6)

            """
            
            # bits_codificados represents the second vector of the msg (b1-b4)
            bits_codificados_2 = []
            bits_codificados_2.append(0) # We add 0 to first element to form a vector of 8 bits. Note that next 7 bits is the coded msg.
            bits_codificados_2.append(a02)
            bits_codificados_2.append(a12)
            bits_codificados_2.append(a22)
            bits_codificados_2.append(a32)
            bits_codificados_2.append(a42)
            bits_codificados_2.append(a52)
            bits_codificados_2.append(a62)

            """""
            Uncomment this if you want to see how the bytes are encoded but no ciphered with the error vector e
            bits_codificados_2_b2 = []
            bits_codificados_2_b2.append(0) # We add 0 to first element to form a vector of 8 bits. Note that next 7 bits is the coded msg.
            bits_codificados_2_b2.append(a02)
            bits_codificados_2_b2.append(a12)
            bits_codificados_2_b2.append(a22)
            bits_codificados_2_b2.append(a32)
            bits_codificados_2_b2.append(a42)
            bits_codificados_2_b2.append(a52)
            bits_codificados_2_b2.append(a62)

            """
            """"
            msg_codificado_sin_errores.append(bits_codificados_b1)
            msg_codificado_sin_errores.append(bits_codificados_2_b2)
            """


            # As we are using hamming codes, we can introduce an error each 7 bits coded. This process will encrypt our data.
            # Then, I'm doing it randomly for bits_codificados1 and bit_codificados2 (Note that I'm not using the first position, it's a 0)




            first_random = random.randint(1,7) 
            second_random = random.randint(1,7) 

            # Let's replace each bit of the vector.
            bits_codificados[first_random] = bits_codificados[first_random] ^ 1
            bits_codificados_2[second_random] = bits_codificados_2[second_random] ^ 1
            
            msg_encoded.append(bits_codificados)
            msg_encoded.append(bits_codificados_2)



       # print(msg_codificado_sin_errores) # Uncomment if you want to see encoded msg.
       
       # print(msg_encoded) # Uncomment if you want to see ciphered msg. 

        
        return msg_encoded


