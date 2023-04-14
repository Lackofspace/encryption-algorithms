def RC5_encrypt(key):
    with open('plaintext.txt', 'r') as file:
        plaintext = file.read().encode('utf-8')

    # Set up parameters for RC5 algorithm
    w = 64  # word size in bits
    r = 12  # number of rounds
    b = len(key)  # length of key in bytes
    u = w // 8  # word size in bytes
    t = 2 * (r + 1)  # number of words in expanded key
    mod = 2 ** w  # modulus used in arithmetic operations

    # Initialize key schedule
    L = [0] * (b // u)  # list of b/u words
    for i in range(len(key)):
        L[i // u] = L[i // u] + (key[i] << (8 * (i % u)))

    S = [0] * t  # expanded key
    S[0] = 0xb7e15163
    for i in range(1, t):
        S[i] = (S[i - 1] + 0x9e3779b9) % mod

    # Perform encryption
    A, B = plaintext[:8], plaintext[8:]
    A = int.from_bytes(A, byteorder='little')
    B = int.from_bytes(B, byteorder='little')
    A = (A + S[0]) % mod
    B = (B + S[1]) % mod

    for i in range(1, r + 1):
        A = ((A ^ B) + S[2 * i]) % mod
        B = ((B ^ A) + S[2 * i + 1]) % mod

    ciphertext = A.to_bytes(8, byteorder='little') + B.to_bytes(8, byteorder='little')
    with open('encoded.bin', 'wb') as f:
        f.write(ciphertext)

    return ciphertext


def RC5_decrypt(key):
    with open('encoded.bin', 'rb') as file:
        ciphertext = file.read()

    # Set up parameters for RC5 algorithm
    w = 64  # word size in bits
    r = 12  # number of rounds
    b = len(key)  # length of key in bytes
    u = w // 8  # word size in bytes
    t = 2 * (r + 1)  # number of words in expanded key
    mod = 2 ** w  # modulus used in arithmetic operations

    # Initialize key schedule
    L = [0] * (b // u)  # list of b/u words
    for i in range(len(key)):
        L[i // u] = L[i // u] + (key[i] << (8 * (i % u)))

    S = [0] * t  # expanded key
    S[0] = 0xb7e15163
    for i in range(1, t):
        S[i] = (S[i - 1] + 0x9e3779b9) % mod

    # Perform decryption
    A, B = int.from_bytes(ciphertext[:8], byteorder='little'), int.from_bytes(ciphertext[8:], byteorder='little')
    for i in range(r, 0, -1):
        B = (B - S[2 * i + 1]) % mod
        B = (B ^ A) % mod
        A = (A - S[2 * i]) % mod
        A = (A ^ B) % mod

    B = (B - S[1]) % mod
    A = (A - S[0]) % mod

    plaintext = A.to_bytes(8, byteorder='little') + B.to_bytes(8, byteorder='little')
    plaintext = plaintext.strip(b'\x00')

    with open('decoded.txt', 'wb') as f:
        f.write(plaintext)

    return plaintext.decode('utf-8')


def check_key(key):
    while len(key) % 8 != 0:
        key += b'\x00'
    return key


key = input("input key: ")
key = key.encode('utf-8')
key = check_key(key)
ciphertext = RC5_encrypt(key)

dec = RC5_decrypt(key)
print(dec)
