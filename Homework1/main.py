# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def subByteSingle(byte):
    Sbox = (
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
    )
    return Sbox[byte]


# working TODO verify since now it works with int and remove comments
def subByte(state):
    for i in range(16):
        state[i] = subByteSingle(state[i])
    # print(int(byte.hex(),16))
    # print(Sbox[int(byte.hex(),16)])
    #return Sbox[int(byte.hex(), 16)]  # modify if you use int instead of byte for byte representation
    return state


# working TODO remove prints
def shiftRow(state):
    row = [0] * 4
    for i in range(1, 4):
        add = 4
        for j in range(4):
            row[j] = state[i + j * add]
            print(row[j])
        for k in range(i):
            temp = row[0]
            row[0] = row[1]
            row[1] = row[2]
            row[2] = row[3]
            row[3] = temp
        print()
        print(row)
        for j in range(4):
            state[i + j * add] = row[j]
        print()
        print()
    return state

# working with int
def xtime(element):
    if element & 0x80:
        element << 1
        element ^ 0x1B
        #print("true")
    else:
        element << 1
    return element


# working TODO remove prints
def mixcolumns(state):
    column = [0] * 4
    for i in range(4):
        add = 4
        for j in range(4):
            column[j] = state[i * add + j]
            print(column[j])
        xorAll = column[0] ^ column[1] ^ column[2] ^ column[3]
        temp = column[0]
        column[0] = column[0] ^ xtime(column[0] ^ column[1]) ^ xorAll
        column[1] = column[1] ^ xtime(column[1] ^ column[2]) ^ xorAll
        column[2] = column[2] ^ xtime(column[2] ^ column[3]) ^ xorAll
        column[3] = column[3] ^ xtime(column[3] ^ temp) ^ xorAll
        print()
        print(column)
        for j in range(4):
            state[i * add + j] = column[j]
        print()
        print()
    return state

# TODO delete it since we don't need it
def mixColumnsSingle(column):
    xorAll = column[0] ^ column[1] ^ column[2] ^ column[3]
    temp = column[0]
    column[0] = column[0] ^ xtime(column[0] ^ column[1]) ^ xorAll
    column[1] = column[1] ^ xtime(column[1] ^ column[2]) ^ xorAll
    column[2] = column[2] ^ xtime(column[2] ^ column[3]) ^ xorAll
    column[3] = column[3] ^ xtime(column[3] ^ temp) ^ xorAll
    print(column)
    return column

# working
def gFunction(word, round):
    #define round addiction vector
    rc = (0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36)
    # left shift of 1 byte
    temp = word[0]
    word[0] = word[1]
    word[1] = word[2]
    word[2] = word[3]
    word[3] = temp
    # byte substitution
    for i in range(4):
        subByteSingle(word[i])
    # xor first value
    word[0] ^= rc[round]
    return word

# to test(maybe it's working)
def roundKey(key, round):
    # word division
    word0 = [key[0], key[1], key[2], key[3]]
    word1 = [key[4], key[5], key[6], key[7]]
    word2 = [key[8], key[9], key[10], key[11]]
    word3 = [key[12], key[13], key[14], key[15]]
    # g function computation
    gRound = gFunction(word3, round)
    for i in range(4):
        word0[i] ^= gRound[i]
        word1[i] ^= word0[i]
        word2[i] ^= word1[i]
        word3[i] ^= word2[i]
    for i in range(4):
        key[i] = word0[i]
        key[i+4] = word1[i]
        key[i+8] = word2[i]
        key[i+12] = word3[i]
    return key


def keyAddition(state, subkey):
    for i in range(16):
        state[i] ^= subkey[i]
    return state


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #prova = subByte(b"\xc2")
    #xtime(prova)
    # xtime(subByte(b"\x04"))
    # xtime(b"\xc2")
    state = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    print(state)
    """state = subByte(state)
    print(state)"""
    roundKey(state, 0)
    print(state)
    """word = [0, 1, 2, 3]
    word = gFunction(word,5)
    print(word)"""
    """state = shiftRow(state)
    print(state)
    state = mixcolumns(state)
    print(state)"""
    #mixColumnsSingle([12,9,10,11])
