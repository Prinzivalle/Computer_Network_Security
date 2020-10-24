# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#################   ENCRYPTION     ###################

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

# working
def subByte(state):
    for i in range(16):
        state[i] = subByteSingle(state[i])
    return state

# working
def shiftRow(state):
    row = [0] * 4
    for i in range(1, 4):
        add = 4
        # build row from state vector
        for j in range(4):
            row[j] = state[i + j * add]

        # shift rows
        for k in range(i):
            temp = row[0]
            row[0] = row[1]
            row[1] = row[2]
            row[2] = row[3]
            row[3] = temp

        # rebuild state vector from every row
        for j in range(4):
            state[i + j * add] = row[j]

    return state

# working
def xtime(element):
    if element & 0x80:
        element = element << 1
        element ^= 0x1B
    else:
        element = element << 1
    # the & in the return is to rebuild the byte dimension
    return element & 0xFF

# working
def mixcolumns(state):
    column = [0] * 4
    for i in range(4):
        # build column from state vector
        add = 4
        for j in range(4):
            column[j] = state[i * add + j]

        # mixcolumn
        xorAll = column[0] ^ column[1] ^ column[2] ^ column[3]
        temp = column[0]
        column[0] = column[0] ^ xtime(column[0] ^ column[1]) ^ xorAll
        column[1] = column[1] ^ xtime(column[1] ^ column[2]) ^ xorAll
        column[2] = column[2] ^ xtime(column[2] ^ column[3]) ^ xorAll
        column[3] = column[3] ^ xtime(column[3] ^ temp) ^ xorAll

        # rebuild state from the column
        for j in range(4):
            state[i * add + j] = column[j]

    return state

# TODO delete it since we don't need it
def mixColumnsSingle(column):
    xorAll = column[0] ^ column[1] ^ column[2] ^ column[3]
    temp = column[0]
    column[0] = column[0] ^ xtime(column[0] ^ column[1]) ^ xorAll
    column[1] = column[1] ^ xtime(column[1] ^ column[2]) ^ xorAll
    column[2] = column[2] ^ xtime(column[2] ^ column[3]) ^ xorAll
    column[3] = column[3] ^ xtime(column[3] ^ temp) ^ xorAll
    #print(column)
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

# working
def roundKey(subkey, round):

    # word division
    word0 = [subkey[0], subkey[1], subkey[2], subkey[3]]
    word1 = [subkey[4], subkey[5], subkey[6], subkey[7]]
    word2 = [subkey[8], subkey[9], subkey[10], subkey[11]]
    word3 = [subkey[12], subkey[13], subkey[14], subkey[15]]

    # g function computation
    gRound = gFunction(word3, round)

    # xor implemetation
    for i in range(4):
        word0[i] ^= gRound[i]
        word1[i] ^= word0[i]
        word2[i] ^= word1[i]
        word3[i] ^= word2[i]

    # rebuild key from word
    for i in range(4):
        subkey[i] = word0[i]
        subkey[i+4] = word1[i]
        subkey[i+8] = word2[i]
        subkey[i+12] = word3[i]
    return subkey

def keyAddition(state, subkey):
    for i in range(16):
        state[i] ^= subkey[i]
    return state

################    DECRYPTION     ##########################

# working
def mixcolumnsInv(state):
    column = [0] * 4
    for i in range(4):
        add = 4
        # build column from state vector
        for j in range(4):
            column[j] = state[i * add + j]

        # preprocessing
        u = xtime(xtime(column[0] ^ column[2]))
        v = xtime(xtime(column[1] ^ column[3]))
        column[0] = column[0] ^ u
        column[1] = column[1] ^ v
        column[2] = column[2] ^ u
        column[3] = column[3] ^ v

        # standard mixcolumn
        xorAll = column[0] ^ column[1] ^ column[2] ^ column[3]
        temp = column[0]
        column[0] = column[0] ^ xtime(column[0] ^ column[1]) ^ xorAll
        column[1] = column[1] ^ xtime(column[1] ^ column[2]) ^ xorAll
        column[2] = column[2] ^ xtime(column[2] ^ column[3]) ^ xorAll
        column[3] = column[3] ^ xtime(column[3] ^ temp) ^ xorAll

        # rebuild state from the column
        for j in range(4):
            state[i * add + j] = column[j]

    return state

# TODO delete it since we don't need it
def mixColumnsSingleInv(column):
    u = xtime(xtime(column[0] ^ column[2]))
    v = xtime(xtime(column[1] ^ column[3]))
    column[0] = column[0] ^ u
    column[1] = column[1] ^ v
    column[2] = column[2] ^ u
    column[3] = column[3] ^ v

    xorAll = column[0] ^ column[1] ^ column[2] ^ column[3]
    temp = column[0]
    column[0] = column[0] ^ xtime(column[0] ^ column[1]) ^ xorAll
    column[1] = column[1] ^ xtime(column[1] ^ column[2]) ^ xorAll
    column[2] = column[2] ^ xtime(column[2] ^ column[3]) ^ xorAll
    column[3] = column[3] ^ xtime(column[3] ^ temp) ^ xorAll
    return column

# working
def shiftRowInv(state):
    row = [0] * 4
    for i in range(1, 4):
        add = 4
        # build row from state vector
        for j in range(4):
            row[j] = state[i + j * add]

        # shift rows
        for k in range(i):
            temp = row[3]
            row[3] = row[2]
            row[2] = row[1]
            row[1] = row[0]
            row[0] = temp

        # rebuild state vector from every row
        for j in range(4):
            state[i + j * add] = row[j]

    return state

def subByteSingleInv(byte):
    SboxInv = (
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
    )
    return SboxInv[byte]

# working
def subByteInv(state):
    for i in range(16):
        state[i] = subByteSingleInv(state[i])
    return state

###################     MAIN    #####################

#shorter version
"""if __name__ == '__main__':
    state = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    #print(shiftRow(state))
    #print(subByteSingle(16))
    #print(shiftRowInv([0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]))
    #print(mixcolumns([219, 19, 83, 69, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]))
    #print()
    #key = "00112233445566778899aabbccddeeff"
    key= "00010203040506070809101112131415"
    print([[int(key[i * 8 + j * 2:i * 8 + j * 2 + 2], 16) for j in range(4)]
     for i in range(4)])
    
    print(mixColumnsSingleInv(mixColumnsSingle([219, 19, 83, 69])))
    print(mixColumnsSingleInv(mixColumnsSingle([242, 10, 34, 92])))
    print(mixColumnsSingleInv(mixColumnsSingle([1, 1, 1, 1])))
    print(mixColumnsSingleInv(mixColumnsSingle([198, 198, 198, 198])))
    print(mixColumnsSingleInv(mixColumnsSingle([212, 212, 212, 213])))
    print(mixColumnsSingleInv(mixColumnsSingle([45, 38, 49, 76])))

    print()
    #print(xtime(150))
    #print(xtime(16))
    #prova = subByte(b"\xc2")
    #xtime(prova)
    # xtime(subByte(b"\x04"))
    # xtime(b"\xc2")
    #state = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    state = [219, 1, 2, 3, 4, 19, 6, 7, 8, 9, 83, 11, 12, 13, 14, 69]
    key = [16, 17, 18, 19, 20, 21, 22, 23, 24, 24, 26, 27, 28, 29, 30, 31]
    print(state)
    print()
    state = subByte(state)
    print(state)
    roundKey(state, 0)
    print(state)
    word = [0, 1, 2, 3]
    word = gFunction(word,5)
    print(word)
    state = shiftRow(state)
    print(state)
    state = mixcolumns(state)
    print(state)
    #mixColumnsSingle([12,9,10,11])

    #############   ENCRYPTION

    rounds = 0
    ##### first round
    # first round key is simply the original key
    subkey = [16, 22, 53, 10, 89, 100, 69, 13, 36, 54, 67, 91, 12, 1, 78, 51]
    state = keyAddition(state, subkey)
    #print(state)
    # byte substitution
    state = subByte(state)
    #print(state)
    # shift row
    state = shiftRow(state)
    #print(state)
    # mix columns
    state = mixcolumns(state)
    #print(state)
    # key addition
    subkey = roundKey(subkey, rounds)
    print(subkey)
    state = keyAddition(state, subkey)
    # update rounds
    rounds += 1

    ##### intermediate iterations
    for i in range(1, 10):
        # byte substitution
        state = subByte(state)
        # shift row
        state = shiftRow(state)
        # mix columns
        state = mixcolumns(state)
        # key addition
        subkey = roundKey(subkey, rounds)
        print(subkey)
        state = keyAddition(state, subkey)
        #print(subkey)

        # update rounds
        rounds += 1

    ##### last iteration
    # byte substitution
    state = subByte(state)
    # shift row
    state = shiftRow(state)
    # key addition
    subkey = roundKey(subkey, rounds)
    print(subkey)
    state = keyAddition(state, subkey)

    # print the cyphertext
    print()
    print(state)
    #print(subkey)
    #print(rounds)
    print()

    #############   DECRYPTION

    rounds = 0
    ##### first round
    # compute last subkey
    subkey = [16, 22, 53, 10, 89, 100, 69, 13, 36, 54, 67, 91, 12, 1, 78, 51]
    for i in range(11):
        subkey = roundKey(subkey, rounds)
        rounds += 1
        #print(rounds)
        #print(subkey)
    print(subkey)
    state = keyAddition(state, subkey)
    # revert shift row
    state = shiftRowInv(state)
    # revert byte substitution
    state = subByteInv(state)
    # update rounds
    rounds = 0

    ##### intermediate iterations
    for i in range(1, 10):
        # compute subkey
        subkey = [16, 22, 53, 10, 89, 100, 69, 13, 36, 54, 67, 91, 12, 1, 78, 51]
        for j in range(11 - i):
            #print(rounds)
            subkey = roundKey(subkey, rounds)
            #print(subkey)
            rounds += 1
        print(subkey)
        state = keyAddition(state, subkey)
        # revert mix columns
        state = mixcolumnsInv(state)
        # revert shift row
        state = shiftRowInv(state)
        # revert byte substitution
        state = subByteInv(state)
        # update rounds
        rounds = 0

    ##### last iteration
    # revert key addition
    subkey = [16, 22, 53, 10, 89, 100, 69, 13, 36, 54, 67, 91, 12, 1, 78, 51]
    subkey = roundKey(subkey, 0)
    print(subkey)
    state = keyAddition(state, subkey)
    # revert mix columns

    state = mixcolumnsInv(state)
    # revert shift row
    state = shiftRowInv(state)
    # revert byte substitution
    state = subByteInv(state)
    # revert key addition
    subkey = [16, 22, 53, 10, 89, 100, 69, 13, 36, 54, 67, 91, 12, 1, 78, 51]
    state = keyAddition(state, subkey)

    # print the plaintext
    print()
    print(state)
    """

if __name__ == '__main__':
    state = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    key = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    print(state)
    # mixColumnsSingle([12,9,10,11])

    #############   ENCRYPTION

    rounds = 0
    ##### first round
    # first round key is simply the original key
    subkey = list(key)
    state = keyAddition(state, subkey)
    # byte substitution
    state = subByte(state)
    # shift row
    state = shiftRow(state)
    # mix columns
    state = mixcolumns(state)
    # key addition
    subkey = roundKey(subkey, rounds)
    state = keyAddition(state, subkey)
    # update rounds
    rounds += 1

    ##### intermediate iterations
    for i in range(1, 10):
        # byte substitution
        state = subByte(state)
        # shift row
        state = shiftRow(state)
        # mix columns
        state = mixcolumns(state)
        # key addition
        subkey = roundKey(subkey, rounds)
        state = keyAddition(state, subkey)

        # update rounds
        rounds += 1

    ##### last iteration
    # byte substitution
    state = subByte(state)
    # shift row
    state = shiftRow(state)
    # key addition
    subkey = roundKey(subkey, rounds)
    state = keyAddition(state, subkey)

    # print the cyphertext
    print()
    print(state)
    print(key)
    print()

    #############   DECRYPTION

    rounds = 0
    ##### first round
    # compute last subkey
    subkey = list(key)
    for i in range(11):
        subkey = roundKey(subkey, rounds)
        rounds += 1
    # revert key addition
    state = keyAddition(state, subkey)
    # revert shift row
    state = shiftRowInv(state)
    # revert byte substitution
    state = subByteInv(state)
    # update rounds
    rounds = 0

    ##### intermediate iterations
    for i in range(1, 10):
        # compute subkey
        subkey = list(key)
        for j in range(11 - i):
            subkey = roundKey(subkey, rounds)
            rounds += 1
        # revert key addition
        state = keyAddition(state, subkey)
        # revert mix columns
        state = mixcolumnsInv(state)
        # revert shift row
        state = shiftRowInv(state)
        # revert byte substitution
        state = subByteInv(state)
        # update rounds
        rounds = 0

    ##### last iteration
    # revert key addition
    subkey = list(key)
    subkey = roundKey(subkey, 0)
    state = keyAddition(state, subkey)
    # revert mix columns
    state = mixcolumnsInv(state)
    # revert shift row
    state = shiftRowInv(state)
    # revert byte substitution
    state = subByteInv(state)
    # revert key addition
    subkey = list(key)
    state = keyAddition(state, subkey)

    # print the plaintext
    print()
    print(state)

