#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 19:59:18 2020

@author: sourav
"""


import os
import base64
from PIL import Image
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptDecrypt():
    def decrypt_image(self, img_dir, image, key):
        self.dir = img_dir
        self.HenonDecryption(self.dir+image, key)
        
    def encrypt_vectors(self, data):
        password_provided = "sourav" # This is input in the form of a string
        password = password_provided.encode() # Convert to type bytes
        salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
            )
        key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
        f = Fernet(key)
        encrypted = f.encrypt(data)
        return encrypted
            
    def getImageMatrix(self, imageName):
        im = Image.open(imageName) 
        pix = im.load()
        color = 1
        if type(pix[0,0]) == int:
          color = 0
        image_size = im.size 
        image_matrix = []
        for width in range(int(image_size[0])):
            row = []
            for height in range(int(image_size[1])):
                    row.append((pix[width,height]))
            image_matrix.append(row)
        return image_matrix,image_size[0],color

    def dec(self, bitSequence):
        decimal = 0
        for bit in bitSequence:
            decimal = decimal * 2 + int(bit)
        return decimal

    def genHenonMap(self, dimension, key):
        x = key[0]
        y = key[1]
        sequenceSize = dimension * dimension * 8 #Total Number of bitSequence produced
        bitSequence = []    #Each bitSequence contains 8 bits
        byteArray = []      #Each byteArray contains m( i.e 512 in this case) bitSequence
        TImageMatrix = []   #Each TImageMatrix contains m*n byteArray( i.e 512 byteArray in this case)
        for i in range(sequenceSize):
            xN = y + 1 - 1.4 * x**2
            yN = 0.3 * x
    
            x = xN
            y = yN
    
            if xN <= 0.4:
                bit = 0
            else:
                bit = 1
    
            try:
                bitSequence.append(bit)
            except:
                bitSequence = [bit]
    
            if i % 8 == 7:
                decimal = self.dec(bitSequence)
                try:
                    byteArray.append(decimal)
                except:
                    byteArray = [decimal]
                bitSequence = []
    
            byteArraySize = dimension*8
            if i % byteArraySize == byteArraySize-1:
                try:
                    TImageMatrix.append(byteArray)
                except:
                    TImageMatrix = [byteArray]
                byteArray = []
        return TImageMatrix

    def HenonDecryption(self, imageNameEnc, key):
        imageMatrix, dimension, color = self.getImageMatrix(imageNameEnc)
        transformationMatrix = self.genHenonMap(dimension, key)
        henonDecryptedImage = []
        for i in range(dimension):
            row = []
            for j in range(dimension):
                try:
                    if color:
                        row.append(tuple([transformationMatrix[i][j] ^ x for x in imageMatrix[i][j]]))
                    else:
                        row.append(transformationMatrix[i][j] ^ imageMatrix[i][j])
                except:
                    if color:
                        row = [tuple([transformationMatrix[i][j] ^ x for x in imageMatrix[i][j]])]
                    else :
                        row = [transformationMatrix[i][j] ^ x for x in imageMatrix[i][j]]
            try:
                henonDecryptedImage.append(row)
            except:
                henonDecryptedImage = [row]
        if color:
            im = Image.new("RGB", (dimension, dimension))
        else: 
            im = Image.new("L", (dimension, dimension)) # L is for Black and white pixels
    
        pix = im.load()
        for x in range(dimension):
            for y in range(dimension):
                pix[x, y] = henonDecryptedImage[x][y]
        im.save(".decrypted_images/" + os.path.basename(imageNameEnc).split('.')[0] + ".png")
