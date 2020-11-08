from random import SystemRandom
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Util import number
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import time
import os


##################### AUXILIARY FUNCTIONS ###########################

# use slide implementation of square and multiply, better implementation
# by using modulo reduction at each step
def sam(base, exp, n):
    f = 1
    while exp > 0:
        lsb = 0x1 & exp
        exp >>= 1
        if lsb:
            f *= base
        base *= base
        base = base % n
        f = f % n
    return f


def selExp(phi):
    maxiter = 200
    for i in range(maxiter):
        e = SystemRandom().randint(1, phi - 1)
        g, s, t = eea(e, phi)
        if g == 1:
            # s is the coefficient for the first argument
            # of egcd, so in this case s is coefficient of e
            d = s % phi
            return e, d
    return 0, 0


# based on slide implementation with some improvements
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
    y = sam(x, e, n)
    return y


def decrypt(y, d, n):
    x = sam(y, d, n)
    return x


def initialization(nbit):
    p = number.getPrime(nbit, os.urandom)
    q = number.getPrime(nbit, os.urandom)
    n = p * q
    phi = (p - 1) * (q - 1)
    return n, phi


##################### RSA COMPARISON ###########################

def testRSA(rounds, keylength):
    buffer_size = 102400  # 100k

    ######  ENCRYPTION
    print()
    print("######### ENCRYPTION TEST RSA ############")

    ##### RSA pycrypto
    start_time = time.time()
    random_generator = os.urandom
    key = RSA.generate(keylength, random_generator)  # generate pub and priv key
    print("pycryptodome RSA key generation --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    # In first round save the encrypted file for decrypt test
    f = open("small.txt", "rb")
    output_file = open('small_RSApy.encrypted', 'wb')
    cipher = PKCS1_OAEP.new(key)
    buffer = f.read(buffer_size)
    while len(buffer) > 0:
        ciphered_bytes = cipher.encrypt(buffer)
        output_file.write(ciphered_bytes)
        buffer = f.read(buffer_size)
    f.close()
    output_file.close()

    for i in range(rounds - 1):
        f = open("small.txt", "rb")
        cipher = PKCS1_OAEP.new(key)
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            cipher.encrypt(buffer)
            buffer = f.read(buffer_size)
        f.close()

    print("pycryptodome RSA --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()

    n, phi = initialization(keylength // 2)
    e, d = selExp(phi)

    print("my implementation RSA key generation --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    # In first round save the encrypted file for decrypt test
    f = open("small.txt", "r")
    output_file = open('small_RSAMine.encrypted', 'w')
    buffer = f.read(buffer_size)
    binarybuffer = ''.join(format(ord(x), 'b') for x in buffer)
    while len(buffer) > 0:
        ciphered_bytes = encrypt(int(binarybuffer, 2), e, n)
        output_file.write(str(ciphered_bytes))
        buffer = f.read(buffer_size)
        binarybuffer = ''.join(format(ord(x), 'b') for x in buffer)
    f.close()
    output_file.close()

    for i in range(rounds - 1):
        f = open("small.txt", "r")
        buffer = f.read(buffer_size)
        binarybuffer = ''.join(format(ord(x), 'b') for x in buffer)
        while len(buffer) > 0:
            encrypt(int(binarybuffer, 2), e, n)
            buffer = f.read(buffer_size)
            binarybuffer = ''.join(format(ord(x), 'b') for x in buffer)
        f.close()

    print("my implementation RSA --- %s seconds ---" % (time.time() - start_time))

    ######  DECRYPTION
    print()
    print("######### DECRYPTION TEST RSA ############")

    print()
    start_time = time.time()

    for i in range(rounds):
        f = open("small_RSApy.encrypted", "rb")
        cipher = PKCS1_OAEP.new(key)
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            cipher.decrypt(buffer)
            buffer = f.read(buffer_size)
        f.close()

    print("pycryptodome RSA --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()

    for i in range(rounds):
        f = open("small_RSAMine.encrypted", "r")
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            plain = decrypt(int(buffer), d, n)
            buffer = f.read(buffer_size)
        f.close()
    comp = open("small.txt", "r")
    buffer = comp.read(buffer_size)
    binarybuffer = ''.join(format(ord(x), 'b') for x in buffer)
    comp.close()
    print("original text file   " + str(int(binarybuffer, 2)))
    print("decrypted plain text " + str(plain))

    print("my implementation RSA --- %s seconds ---" % (time.time() - start_time))


##################### AES COMPARISON ###########################

def testAES(rounds, keylength):
    buffer_size = 102400  # 100k

    ######  ENCRYPTION
    print()
    print("######### ENCRYPTION TEST AES ############")

    start_time = time.time()

    # In first round save the encrypted file for decrypt test
    f = open("small.txt", "rb")
    output_file = open('smallECBPycrypto.encrypted', 'wb')
    cipher = AES.new(bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), AES.MODE_ECB)
    buffer = f.read(buffer_size)
    while len(buffer) > 0:
        ciphered_bytes = cipher.encrypt(pad(buffer, 16))
        output_file.write(ciphered_bytes)
        buffer = f.read(buffer_size)
    f.close()
    output_file.close()

    for i in range(rounds - 1):
        f = open("small.txt", "rb")
        cipher = AES.new(bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), AES.MODE_ECB)
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            cipher.encrypt(pad(buffer, 16))
            buffer = f.read(buffer_size)
        f.close()

    print("pycryptodome ECB 1k --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()

    n, phi = initialization(keylength // 2)
    e, d = selExp(phi)

    print("my implementation RSA key generation --- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    # In first round save the encrypted file for decrypt test
    f = open("small.txt", "r")
    output_file = open('small_RSAMine.encrypted', 'w')
    buffer = f.read(buffer_size)
    binarybuffer = ''.join(format(ord(x), 'b') for x in buffer)
    while len(buffer) > 0:
        ciphered_bytes = encrypt(int(binarybuffer, 2), e, n)
        output_file.write(str(ciphered_bytes))
        buffer = f.read(buffer_size)
        binarybuffer = ''.join(format(ord(x), 'b') for x in buffer)
    f.close()
    output_file.close()

    for i in range(rounds - 1):
        f = open("small.txt", "r")
        buffer = f.read(buffer_size)
        binarybuffer = ''.join(format(ord(x), 'b') for x in buffer)
        while len(buffer) > 0:
            encrypt(int(binarybuffer, 2), e, n)
            buffer = f.read(buffer_size)
            binarybuffer = ''.join(format(ord(x), 'b') for x in buffer)
        f.close()

    print("my implementation RSA --- %s seconds ---" % (time.time() - start_time))

    ######  DECRYPTION
    print()
    print("######### DECRYPTION TEST AES ############")

    print()
    start_time = time.time()

    for i in range(rounds):
        f = open("smallECBPycrypto.encrypted", "rb")
        cipher = AES.new(bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), AES.MODE_ECB)
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            cipher.decrypt(buffer)
            buffer = f.read(buffer_size)
        f.close()

    print("pycryptodome ECB 1k --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()

    for i in range(rounds):
        f = open("small_RSAMine.encrypted", "r")
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            plain = decrypt(int(buffer), d, n)
            buffer = f.read(buffer_size)
        f.close()
    comp = open("small.txt", "r")
    buffer = comp.read(buffer_size)
    binarybuffer = ''.join(format(ord(x), 'b') for x in buffer)
    comp.close()
    print("original text file   " + str(int(binarybuffer, 2)))
    print("decrypted plain text " + str(plain))

    print("my implementation RSA --- %s seconds ---" % (time.time() - start_time))


##################### MAIN FUNCTION ###########################

if __name__ == '__main__':
    testRSA(10, 3072)

    testAES(10, 3072)
