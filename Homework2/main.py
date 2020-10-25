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
    # print(column)
    return column

# working
def gFunction(word, round):
    # define round addiction vector
    rc = (0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36)

    # left shift of 1 byte
    temp = word[0]
    word[0] = word[1]
    word[1] = word[2]
    word[2] = word[3]
    word[3] = temp

    # byte substitution
    for i in range(4):
        word[i] = subByteSingle(word[i])

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
    gRound = gFunction(list(word3), round)

    # xor implemetation
    for i in range(4):
        word0[i] ^= gRound[i]
        word1[i] ^= word0[i]
        word2[i] ^= word1[i]
        word3[i] ^= word2[i]

    # rebuild key from word
    for i in range(4):
        subkey[i] = word0[i]
        subkey[i + 4] = word1[i]
        subkey[i + 8] = word2[i]
        subkey[i + 12] = word3[i]

    return subkey

# working
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

###################     INPUT MANIPULATION    #####################

def block2int(block):
    return [int(block[i * 2:i * 2 + 2], 16) for i in range(16)]

def int2block(list):
    return ' '.join(str("%0.2X" % i) for i in list)

def text2blocks(text):
    # preallocate blocks as number of bytes of text
    length = int(len(text) / 32)
    blocks = ["00000000000000000000000000000000"] * (length)

    # split text into blocks of 16 bytes
    for i in range(length):
        blocks[i] = text[i * 32:i * 32 + 32]

    return blocks

def text2blocksPadding(text):
    # preallocate blocks as number of bytes of text
    length = int(len(text) / 32)
    blocks = ["00000000000000000000000000000000"] * (length + 1)

    # split text into blocks of 16 bytes
    for i in range(length + 1):
        blocks[i] = text[i * 32:i * 32 + 32]

    # add padding PKCS#7
    count = int(len(blocks[-1]) / 2)
    if count == 0:
        blocks.pop()
        blocks.append("10101010101010101010101010101010")
    else:
        string = list(blocks[-1])
        for i in range(16 - count):
            string[2 * count + 2 * i:2 * count + 2 * i + 2] = str("%0.2X" % (16 - count))
        blocks[-1] = "".join(string)

    return blocks

def blocks2text(blocks):
    # preallocate list to be threated as string for text
    length = len(blocks)
    textList = [00000000000000000000000000000000] * length

    # generate list from every block
    for i in range(length):
        textList[i] = blocks[i].replace(" ", "")

    # generate string from textlist
    return "".join(textList)

def blocks2textPadding(blocks):
    # preallocate list to be threated as string for text
    length = len(blocks)
    textList = [00000000000000000000000000000000] * length

    # remove padding PKCS#7
    # array indexes are strange values since hex values are separated by spaces
    last = int(blocks[-1][45:47], 16)
    if last == 16:
        blocks.pop()
        textList.pop()
    else:
        string = list(blocks[-1])
        for i in range(last):
            string.pop()
            string.pop()
            string.pop()
        blocks[-1] = "".join(string)

    # generate list from every block
    for i in range(len(blocks)):
        textList[i] = blocks[i].replace(" ", "")

    # generate string from textlist
    return "".join(textList)

###################     AES MAIN FUNCTIONS    #####################

def encrypt(plaintext, key):
    state = list(plaintext)

    #############   ENCRYPTION

    rounds = 0
    ##### first round
    # first round key is simply the original key
    subkey = list(key)
    state = keyAddition(state, subkey)
    # update rounds
    rounds += 1
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
    for i in range(1, 9):
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

    return state

def decrypt(ciphertext, key):
    state = list(ciphertext)

    #############   DECRYPTION

    rounds = 0
    ##### first round
    # compute last subkey
    subkey = list(key)
    for i in range(10):
        rounds += 1
        subkey = roundKey(subkey, rounds)
    # revert key addition
    state = keyAddition(state, subkey)
    # revert shift row
    state = shiftRowInv(state)
    # revert byte substitution
    state = subByteInv(state)
    # update rounds
    rounds = 0

    ##### intermediate iterations
    for i in range(1, 9):
        # compute subkey
        subkey = list(key)
        for j in range(10 - i):
            rounds += 1
            subkey = roundKey(subkey, rounds)
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
    subkey = roundKey(subkey, 1)
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

    return state

###################     OPERATION MODES    #####################

def ECB(plaintext, key):

    # get 16 bytes blocks from text
    blocks = text2blocksPadding(plaintext)

    # transform key into int
    key = block2int(key)

    # encrypt every block
    for i in range(len(blocks)):
        blockInt = block2int(blocks[i])
        blockInt = encrypt(blockInt, key)
        blocks[i] = int2block(blockInt)

    # get ciphertext from encrypted blocks
    ciphertext = blocks2text(blocks)

    return ciphertext

def ECBinv(ciphertext, key):

    # get 16 bytes blocks from text
    blocks = text2blocks(ciphertext)

    # transform key into int
    key = block2int(key)

    # decrypt every block
    for i in range(len(blocks)):
        blockInt = block2int(blocks[i])
        blockInt = decrypt(blockInt, key)
        blocks[i] = int2block(blockInt)

    # get ciphertext from encrypted blocks
    plaintext = blocks2textPadding(blocks)

    return plaintext

def CBC(plaintext, key, IV):

    # get 16 bytes blocks from text
    blocks = text2blocksPadding(plaintext)

    # transform key into int
    key = block2int(key)

    # first block encryption
    blockInt = block2int(blocks[0])
    IVint = block2int(IV)
    for j in range(16):
        blockInt[j] ^= IVint[j]
    blockInt = encrypt(blockInt, key)
    blocks[0] = int2block(blockInt)

    # following blocs encryption
    for i in range(1, len(blocks)):
        blockInt = block2int(blocks[i])
        blockIntprev = block2int(blocks[i-1].replace(" ", ""))
        for j in range(16):
            blockInt[j] ^= blockIntprev[j]
        blockInt = encrypt(blockInt, key)
        blocks[i] = int2block(blockInt)

    # get ciphertext from encrypted blocks
    ciphertext = blocks2text(blocks)

    return ciphertext

def CBCinv(ciphertext, key, IV):

    # get 16 bytes blocks from text
    blocks = text2blocks(ciphertext)

    # get 16 bytes blocks from text, to be used in xor
    text = text2blocks(ciphertext)

    # transform key into int
    key = block2int(key)

    # decrypt first block
    blockInt = block2int(blocks[0])
    blockInt = decrypt(blockInt, key)
    IVint = block2int(IV)
    for j in range(16):
        blockInt[j] ^= IVint[j]
    blocks[0] = int2block(blockInt)

    # decrypt following blocks
    for i in range(1, len(blocks)):
        blockInt = block2int(blocks[i])
        blockInt = decrypt(blockInt, key)
        textInt = block2int(text[i-1])
        for j in range(16):
            blockInt[j] ^= textInt[j]
        blocks[i] = int2block(blockInt)

    # get ciphertext from encrypted blocks
    plaintext = blocks2textPadding(blocks)

    return plaintext

def CFB(plaintext, key, IV):

    # get 16 bytes blocks from text
    blocks = text2blocksPadding(plaintext)

    # transform key into int
    key = block2int(key)

    # first block encryption
    blockInt = block2int(blocks[0])
    IVint = block2int(IV)
    crypt = encrypt(IVint, key)
    for j in range(16):
        blockInt[j] ^= crypt[j]
    blocks[0] = int2block(blockInt)

    # following blocs encryption
    for i in range(1, len(blocks)):
        blockInt = block2int(blocks[i])
        blockIntprev = block2int(blocks[i - 1].replace(" ", ""))
        crypt = encrypt(blockIntprev, key)
        for j in range(16):
            blockInt[j] ^= crypt[j]
        blocks[i] = int2block(blockInt)

    # get ciphertext from encrypted blocks
    ciphertext = blocks2text(blocks)

    return ciphertext

def CFBinv(ciphertext, key, IV):

    # get 16 bytes blocks from text
    blocks = text2blocks(ciphertext)

    # get 16 bytes blocks from text, to be used in xor
    text = text2blocks(ciphertext)

    # transform key into int
    key = block2int(key)

    # first block encryption
    blockInt = block2int(blocks[0])
    IVint = block2int(IV)
    crypt = encrypt(IVint, key)
    for j in range(16):
        blockInt[j] ^= crypt[j]
    blocks[0] = int2block(blockInt)

    # following blocs encryption
    for i in range(1, len(blocks)):
        blockInt = block2int(blocks[i])
        textInt = block2int(text[i-1])
        crypt = encrypt(textInt, key)
        for j in range(16):
            blockInt[j] ^= crypt[j]
        blocks[i] = int2block(blockInt)

    # get ciphertext from encrypted blocks
    plaintext = blocks2textPadding(blocks)

    return plaintext

def OFB(plaintext, key, IV):

    # get 16 bytes blocks from text
    blocks = text2blocksPadding(plaintext)

    # transform key into int
    key = block2int(key)

    # first block encryption
    blockInt = block2int(blocks[0])
    IVint = block2int(IV)
    crypt = encrypt(IVint, key)
    for j in range(16):
        blockInt[j] ^= crypt[j]
    blocks[0] = int2block(blockInt)

    # following blocs encryption
    for i in range(1, len(blocks)):
        blockInt = block2int(blocks[i])
        crypt = encrypt(crypt, key)
        for j in range(16):
            blockInt[j] ^= crypt[j]
        blocks[i] = int2block(blockInt)

    # get ciphertext from encrypted blocks
    ciphertext = blocks2text(blocks)

    return ciphertext

def OFBinv(ciphertext, key, IV):

    # get 16 bytes blocks from text
    blocks = text2blocks(ciphertext)

    # get 16 bytes blocks from text, to be used in xor
    text = text2blocks(ciphertext)

    # transform key into int
    key = block2int(key)

    # first block encryption
    blockInt = block2int(blocks[0])
    IVint = block2int(IV)
    crypt = encrypt(IVint, key)
    for j in range(16):
        blockInt[j] ^= crypt[j]
    blocks[0] = int2block(blockInt)

    # following blocs encryption
    for i in range(1, len(blocks)):
        blockInt = block2int(blocks[i])
        crypt = encrypt(crypt, key)
        for j in range(16):
            blockInt[j] ^= crypt[j]
        blocks[i] = int2block(blockInt)

    # get ciphertext from encrypted blocks
    plaintext = blocks2textPadding(blocks)

    return plaintext

def CTR(plaintext, key, nonce):

    # get 16 bytes blocks from text
    blocks = text2blocksPadding(plaintext)

    # transform key into int
    key = block2int(key)

    # transform nonce into int
    nonce = block2int(nonce)

    # encrypt every block
    for i in range(len(blocks)):
        crypt = encrypt(nonce, key)
        blockInt = block2int(blocks[i])
        for j in range(16):
            blockInt[j] ^= crypt[j]
        blocks[i] = int2block(blockInt)
        nonce[15] += 1
        for j in range(14):
            if nonce[15 - i] > 255:
                nonce[14 - i] += 1
                nonce[15 - i] = nonce[15] - 255

    # get ciphertext from encrypted blocks
    ciphertext = blocks2text(blocks)

    return ciphertext

def CTRinv(ciphertext, key, nonce):

    # get 16 bytes blocks from text
    blocks = text2blocks(ciphertext)

    # transform key into int
    key = block2int(key)

    # transform nonce into int
    nonce = block2int(nonce)

    # encrypt every block
    for i in range(len(blocks)):
        crypt = encrypt(nonce, key)
        blockInt = block2int(blocks[i])
        for j in range(16):
            blockInt[j] ^= crypt[j]
        blocks[i] = int2block(blockInt)
        nonce[15] += 1
        for j in range(14):
            if nonce[15 - i] > 255:
                nonce[14 - i] += 1
                nonce[15 - i] = nonce[15] - 255

    # get ciphertext from encrypted blocks
    plaintext = blocks2textPadding(blocks)

    return plaintext

###################     MAIN    #####################

if __name__ == '__main__':
    #key = "00010203040506070809101112131415"
    #text = "0001020304050607080910111213141516"
    #print(text2blocks(text))
    #print(blocks2text(text2blocks(text)))
    #text = "000102030405060708091011121314151617181920212223"
    #print(text2blocks(text))
    #print(blocks2text(text2blocks(text)))
    #text = "0001020304050607080910111213141516171819202122232425262728293031"
    #print(text2blocks(text))
    #print(blocks2text(text2blocks(text)))
    # print([key[i*2:i*2+2] for i in range(16)])
    # print([int(key[i*2:i*2+2]) for i in range(16)])
    # print(' '.join(str(i) for i in [int(key[i*2:i*2+2]) for i in range(16)]))
    # print(''.join(str([int(key[i*2:i*2+2]) for i in range(16)])))

    #state = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    # key = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    #key = [16, 22, 53, 10, 89, 100, 69, 13, 36, 54, 67, 91, 12, 1, 78, 51]
    #print(state)
    # mixColumnsSingle([12,9,10,11])

    #state = encrypt(state, key)

    #print(state)

    #state = decrypt(state, key)

    #print(state)

    #ciphertext = ECB("000102030405060708091011121314151617181920212223", "5468617473206D79204B756E67204675")
    #print(ciphertext)
    #print(ECBinv(ciphertext, "00010203040506070809101112131415"))

    #key = block2int("5468617473206D79204B756E67204675")
    #subkey = list(key)
    #subkey = roundKey(subkey, 1)
    #print(' '.join(str("%0.2X" % i) for i in subkey))

    ciphertext = ECB("6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c37", "2b7e151628aed2a6abf7158809cf4f3c")
    print(ciphertext)
    print(ECBinv(ciphertext, "2b7e151628aed2a6abf7158809cf4f3c"))

    ciphertext = CBC(
        "6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c37",
        "2b7e151628aed2a6abf7158809cf4f3c", "5468617473206D79204B756E67204675")
    print(ciphertext)
    print(CBCinv(ciphertext, "2b7e151628aed2a6abf7158809cf4f3c", "5468617473206D79204B756E67204675"))

    ciphertext = CFB(
        "6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c37",
        "2b7e151628aed2a6abf7158809cf4f3c", "5468617473206D79204B756E67204675")
    print(ciphertext)
    print(CFBinv(ciphertext, "2b7e151628aed2a6abf7158809cf4f3c", "5468617473206D79204B756E67204675"))

    ciphertext = OFB(
        "6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c37",
        "2b7e151628aed2a6abf7158809cf4f3c", "5468617473206D79204B756E67204675")
    print(ciphertext)
    print(OFBinv(ciphertext, "2b7e151628aed2a6abf7158809cf4f3c", "5468617473206D79204B756E67204675"))

    ciphertext = CTR(
        "6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c37",
        "2b7e151628aed2a6abf7158809cf4f3c", "5468617473206D79204B756E67204675")
    print(ciphertext)
    print(CTRinv(ciphertext, "2b7e151628aed2a6abf7158809cf4f3c", "5468617473206D79204B756E67204675"))

    #print(str("%0.2X" % 72))