import random


def add(num1: int, num2: int, modulo: int = 65536) -> int:
    return (num1 + num2) % modulo


def multiply(num1: int, num2: int, modulo: int = 65537) -> int:
    return num1 * num2 % modulo


def mul(num1: int, num2: int, modulo: int = 65537) -> int:
    if num1 == 0:
        num1 = 65536
    if num2 == 0:
        num2 = 65536
    return num1 * num2 % modulo


def encrypt_block(block: str, keyToEncode: list[list], bitsInBlock: int = 16,
                  bitBlockSize: int = 64, binaryConstant: int = 2) -> str:
    # Разделение блока на 4 полуслова
    d1, d2, d3, d4 = [int(block[i:i+bitsInBlock], binaryConstant) for i in range(0, bitBlockSize, bitsInBlock)]

    for everyRound in range(8):

        a = multiply(d1, keyToEncode[everyRound][0])
        b = add(d2, keyToEncode[everyRound][1])
        c = add(d3, keyToEncode[everyRound][2])
        d = multiply(d4, keyToEncode[everyRound][3])
        e = a ^ c
        f = b ^ d

        part = mul(add(f, mul(e, keyToEncode[everyRound][4])), keyToEncode[everyRound][5])
        d1 = a ^ part
        d2 = c ^ part
        part2 = add(mul(e, keyToEncode[everyRound][4]), part)
        d3 = b ^ part2
        d4 = d ^ part2

    d1 = multiply(d1, keyToEncode[8][0])
    d2Save = d2
    d2 = add(d3, keyToEncode[8][1])
    d3 = add(d2Save, keyToEncode[8][2])
    d4 = multiply(d4, keyToEncode[8][3])

    bin_str = ''.join([bin(d)[binaryConstant:].zfill(bitsInBlock) for d in [d1, d2, d3, d4]])

    return bin_str


def split_data_into_blocks(plaintext: str, byteBlockSize: int = 8, bitStringsList=None) -> list[str]:
    if bitStringsList is None:
        bitStringsList = []
    padding = b'\x00' * (byteBlockSize - (len(plaintext) % byteBlockSize))
    padded_data = plaintext.encode() + padding
    blocks = [padded_data[i:i + byteBlockSize] for i in range(0, len(padded_data), byteBlockSize)]

    for block in blocks:
        bitStringsList.append(''.join([format(ord(c), '08b') for c in block.decode()]))
    return bitStringsList


def joinBlocksIntoData(blocks: list[str], bitsInByte: int = 8, binaryConstant: int = 2) -> str:
    bit_strings_list = [b''.join([bytes([int(block[i:i+bitsInByte], binaryConstant)])
                                  for i in range(0, len(block), bitsInByte)]) for block in blocks]
    text = b''.join(bit_strings_list)
    # Удаляем добавленные нулевые байты (если есть)
    text = text.rstrip(b'\x00')
    return text.decode()


def divideToBlocksKey(givenKey: str, blockSize: int = 16, binaryConstant: int = 2, keyLength: int = 128) -> list[int]:
    blocks = [int(givenKey[i:i + blockSize], binaryConstant) for i in range(0, keyLength, blockSize)]
    return blocks


def generate_keys(keyLength: int = 128, numKeys: int = 52, keyBlock: int = 6, generatedKey=None) -> list[list]:
    # Генерируем 128-битный ключ случайным образом
    if generatedKey is None:
        generatedKey = []
    getKey = bin(random.getrandbits(keyLength))[2:]
    generatedKey.extend(divideToBlocksKey(getKey))

    for j in range(6):
        generatedKey.extend(divideToBlocksKey(getKey[25:] + getKey[:25]))

    generatedKey = generatedKey[:-4]
    generatedKey = [generatedKey[i:i + keyBlock] for i in range(0, numKeys, keyBlock)]
    return generatedKey


def multiplicativeInverse(num: int, exp: int = -1, modulo: int = 65537) -> int:
    return pow(num, exp, modulo)


def additiveInverse(num: int, modulo: int = 65536) -> int:
    return modulo - num


def keyInverse(keyToInverse: list[list], numKeys: int = 52, keyBlock: int = 6, invKey=None) -> list[list]:
    if invKey is None:
        invKey = []

    for i in range(8, -1, -1):
        l = [multiplicativeInverse(keyToInverse[i][0])]

        if i == 8 or i == 0:
            l.append(additiveInverse(keyToInverse[i][1]))
            l.append(additiveInverse(keyToInverse[i][2]))
        else:
            l.append(additiveInverse(keyToInverse[i][2]))
            l.append(additiveInverse(keyToInverse[i][1]))

        l.append(multiplicativeInverse(keyToInverse[i][3]))

        if i != 0:
            l.append(keyToInverse[i - 1][4])
            l.append(keyToInverse[i - 1][5])

        invKey.extend(l)

    invKey = [invKey[i:i + keyBlock] for i in range(0, numKeys, keyBlock)]
    return invKey


def encodeData(plaintext: str, keyToEncode: list[list], stringOfBits: str = '') -> str:
    blocks = split_data_into_blocks(plaintext)
    for block in blocks:
        stringOfBits += encrypt_block(block, keyToEncode)
    return stringOfBits


def decodeData(binData: str, invKey: list[list], plaintext: str = '') -> str:
    blocks = [binData[i:i + 64] for i in range(0, len(binData), 64)]
    for block in blocks:
        plaintext += joinBlocksIntoData([encrypt_block(block, invKey)])
    return plaintext


if __name__ == "__main__":
    cin = input("[D]ecode or [E]ncode: ").lower()
    if cin == "d":
        filename = input("Input file name: ") + ".bin"
        keyList = input('Input keyToInverse with whitespace (52 numbers): ').split(" ")
        key = []
        for element in keyList:
            key.append(int(element))
        numberOfKeys = 52
        keysInBlock = 6
        inv = keyInverse([key[i:i + 6] for i in range(0, numberOfKeys, keysInBlock)])
        with open(filename, "r") as binFile:
            decodedData = binFile.read()
        result = decodeData(decodedData, inv)
        print(result)
    if cin == "e":
        filename = input("Input file name: ") + ".txt"
        key = generate_keys()
        print(f'keyToInverse is:')
        for sublist in key:
            for element in sublist:
                print(element, end=' ')
        with open(filename, "r") as textFile:
            data = textFile.read()

        string = encodeData(data, key)

        fileWrite = input("\nInput file name to write encoded plaintext: ") + ".bin"
        with open(fileWrite, "wb") as createdBinFile:
            createdBinFile.write(bytes(string, 'utf-8'))
