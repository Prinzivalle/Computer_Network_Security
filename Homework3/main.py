from random import SystemRandom
from Cryptodome.Util import number
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import random
import math
import time
import os

##################### AUXILIARY FUNCTIONS ###########################

# use slide implementation of square and multiply
def sam(base, exp):
    f = 1
    while exp > 0:
        lsb = 0x1 & exp
        exp >>=1
        if lsb:
            f *= base
        base *= base
    return f

def selExp(phi):
    maxiter = 100
    for i in range(maxiter):
        e = SystemRandom().randint(1, phi-1)
        g, s, t = eea(e, phi)
        if g == 1:
            # s is the coefficient for the first argument
            # of egcd, so in this case s is coefficient of e
            d = s % phi
            return e, d
    return 0, 0

# taken from https://code.activestate.com/recipes/474129-extended-great-common-divisor-function/
def eea(a, b):
    s, s1 = 1, 0
    t, t1 = 0, 1
    g, g1 = a, b
    while g1:
        q = g // g1
        s, s1 = s1, s - q * s1
        t, t1 = t1, t - q * t1
        g, g1 = g1, g - q * g1
    return g, s, t

##################### RSA MAIN FUNCTIONS ###########################

# variable name are based on slides RSA schemes
def encrypt(x, e, n):
    y = sam(x, e) % n
    return y

def decrypt(y, d, n):
    x = sam(y, d) % n
    return x

def inizialization(nbit):
    p = number.getPrime(nbit, os.urandom)
    q = number.getPrime(nbit, os.urandom)
    n = p * q
    phi = (p - 1) * (q - 1)
    return n, phi

##################### RSA COMPARISON ###########################

def testRSA(rounds, keylength):

    buffer_size = 102400    # 100k

    ######  ENCRYPTION
    print()
    print("######### ENCRYPTION TEST RSA ############")

    ##### ECB 1K
    start_time = time.time()

    # In first round save the encrypted file for decrypt test
    f = open("1K.txt", "rb")
    output_file = open('1kECBPycrypto.encrypted', 'wb')
    key = RSA.generate(keylength)
    print(key)
    #f = open('mykey.pem', 'wb')
    #f.write(key.export_key('PEM'))
    #f.close()
    #f = open('mykey.pem', 'r')
    #key = RSA.import_key(f.read())
    """buffer = f.read(buffer_size)
    while len(buffer) > 0:
        ciphered_bytes = sam(buffer, key)
        output_file.write(ciphered_bytes)
        buffer = f.read(buffer_size)
    f.close()
    output_file.close()

    for i in range(rounds - 1):
        f = open("1K.txt", "rb")
        cipher = AES.new(bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), AES.MODE_ECB)
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            cipher.encrypt(pad(buffer, 16))
            buffer = f.read(buffer_size)
        f.close()
    """
    print("pycryptodome ECB 1k --- %s seconds ---" % (time.time() - start_time))

    """start_time = time.time()

    # In first round save the encrypted file for decrypt test
    f = open("1K.txt", "rb")
    output_file = open('1kECBMine.encrypted', 'w')
    buffer = binascii.hexlify(f.read(buffer_size)).decode('utf-8')
    while len(buffer) > 0:
        ciphered_bytes = ECB(buffer, "2b7e151628aed2a6abf7158809cf4f3c")
        output_file.write(ciphered_bytes)
        buffer = binascii.hexlify(f.read(buffer_size)).decode('utf-8')
    f.close()

    for i in range(time1 - 1):
        f = open("1K.txt", "rb")
        buffer = binascii.hexlify(f.read(buffer_size)).decode('utf-8')
        while len(buffer) > 0:
            ciphered_bytes = ECB(buffer, "2b7e151628aed2a6abf7158809cf4f3c")
            buffer = binascii.hexlify(f.read(buffer_size)).decode('utf-8')
        f.close()

    print("my implementation ECB 1K --- %s seconds ---" % (time.time() - start_time))"""

    ######  DECRYPTION
    print()
    print("######### DECRYPTION TEST RSA ############")

    """print()
    start_time = time.time()

    for i in range(rounds):
        f = open("1kECBPycrypto.encrypted", "rb")
        cipher = AES.new(bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), AES.MODE_ECB)
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            cipher.decrypt(buffer)
            buffer = f.read(buffer_size)
        f.close()

    print("pycryptodome ECB 1k --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()

    for i in range(time1):
        f = open("1kECBMine.encrypted", "r")
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            ECBinv(buffer, "2b7e151628aed2a6abf7158809cf4f3c")
            buffer = f.read(buffer_size)
        f.close()

    print("my implementation ECB 1K --- %s seconds ---" % (time.time() - start_time))"""

##################### AES COMPARISON ###########################

def testAES(rounds):

    buffer_size = 102400    # 100k

    ######  ENCRYPTION
    print()
    print("######### ENCRYPTION TEST AES ############")

    start_time = time.time()

    # In first round save the encrypted file for decrypt test
    f = open("1K.txt", "rb")
    output_file = open('1kECBPycrypto.encrypted', 'wb')
    cipher = AES.new(bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), AES.MODE_ECB)
    buffer = f.read(buffer_size)
    while len(buffer) > 0:
        ciphered_bytes = cipher.encrypt(pad(buffer, 16))
        output_file.write(ciphered_bytes)
        buffer = f.read(buffer_size)
    f.close()
    output_file.close()

    for i in range(rounds - 1):
        f = open("1K.txt", "rb")
        cipher = AES.new(bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), AES.MODE_ECB)
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            cipher.encrypt(pad(buffer, 16))
            buffer = f.read(buffer_size)
        f.close()

    print("pycryptodome ECB 1k --- %s seconds ---" % (time.time() - start_time))

    """start_time = time.time()

    # In first round save the encrypted file for decrypt test
    f = open("1K.txt", "rb")
    output_file = open('1kECBMine.encrypted', 'w')
    buffer = binascii.hexlify(f.read(buffer_size)).decode('utf-8')
    while len(buffer) > 0:
        ciphered_bytes = ECB(buffer, "2b7e151628aed2a6abf7158809cf4f3c")
        output_file.write(ciphered_bytes)
        buffer = binascii.hexlify(f.read(buffer_size)).decode('utf-8')
    f.close()

    for i in range(time1 - 1):
        f = open("1K.txt", "rb")
        buffer = binascii.hexlify(f.read(buffer_size)).decode('utf-8')
        while len(buffer) > 0:
            ciphered_bytes = ECB(buffer, "2b7e151628aed2a6abf7158809cf4f3c")
            buffer = binascii.hexlify(f.read(buffer_size)).decode('utf-8')
        f.close()

    print("my implementation ECB 1K --- %s seconds ---" % (time.time() - start_time))"""

    ######  DECRYPTION
    print()
    print("######### DECRYPTION TEST AES ############")

    print()
    start_time = time.time()

    for i in range(rounds):
        f = open("1kECBPycrypto.encrypted", "rb")
        cipher = AES.new(bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), AES.MODE_ECB)
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            cipher.decrypt(buffer)
            buffer = f.read(buffer_size)
        f.close()

    print("pycryptodome ECB 1k --- %s seconds ---" % (time.time() - start_time))

    """start_time = time.time()

    for i in range(time1):
        f = open("1kECBMine.encrypted", "r")
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            ECBinv(buffer, "2b7e151628aed2a6abf7158809cf4f3c")
            buffer = f.read(buffer_size)
        f.close()

    print("my implementation ECB 1K --- %s seconds ---" % (time.time() - start_time))"""


##################### MAIN FUNCTION ###########################

if __name__ == '__main__':
    p = 3
    q = 11
    n = p * q
    print(n)
    phi = (p-1)*(q-1)
    print(phi)
    e, d = selExp(phi)
    print()
    print(e)
    print(d)
    print()

    y = encrypt(4, e, n)
    print(y)
    print(decrypt(y, d, n))


    testRSA(10, 3072)
    testAES(10)