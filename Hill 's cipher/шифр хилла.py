import numpy as np
import math


def key():
    k_str = input("Введите ключ по строкам матрицы через пробел:\n").split()
    key = []
    for element in k_str:
        key.append(int(element))
    n = int(math.sqrt(len(key)))
    key = [key[x : n + x] for x in range(0, len(key), n)]
    return(key, n)

    
def encryption(text, alphabet, k, n):
    ExtraLetter = 0
    while len(text) % n != 0:
        text += 'a'
        ExtraLetter += 1
    return(alg(text, alphabet, k, n, ExtraLetter))


def decryption(text, alphabet, k, n):
    k = np.linalg.inv(k)
    ExtraLetter = 0
    while len(text) % n != 0:
        text += 'c'
        ExtraLetter += 1
    return(alg(text, alphabet, k, n, ExtraLetter))
    
    
def alg(text, alphabet, k, n, ExtraLetter):
    det = round(np.linalg.det(k))
    print(f'det k = {det}, OK!')
    if det == 0:
        print("Определитель матрицы не должен быть равен 0!")
        import sys
        sys.exit()
    IndexList = []
    for letter in text:
        index = alphabet[0].index(letter)
        IndexList.append(index)
    print(IndexList)
    IndexList = [IndexList[x : 1 + x] for x in range(0, len(IndexList), 1)]
    IndexList = [IndexList[x : n + x] for x in range(0, len(IndexList), n)]
    ChiphList = []
    for i in range(len(IndexList)):
        total = np.array(k).dot(np.array(IndexList[i]))
        for g in range(n):
            total[g][0] = total[g][0] % 26
            if total[g][0] < 0:
                total[g][0] += 26
            if total[g][0] > 25:
                total[g][0] -= 26
            ChiphList.append(int(total[g][0]))
    print(ChiphList)
    Chiphertext = ''
    for index in ChiphList:
        letter = alphabet[0][index]
        Chiphertext += letter
    if ExtraLetter == 0:
        return(Chiphertext)
    else:
        return(Chiphertext[:-ExtraLetter])

    
def main():
    text = input("Введите текст:\n").lower()
    alphabet = [
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
]
    k, n = key()
    if input("enc or dec:\n") == 'enc':
        ct = encryption(text, alphabet, k, n)
        print(f'Шифртекст:\n{ct}')
    else:
        pt = decryption(text, alphabet, k, n)
        print(f'Открытый текст:\n{pt}')


if __name__ == "__main__":
    main()