import numpy as np
import math


def newkey(k1, k2):
    total = np.array(k1).dot(np.array(k2))
    return total


def alg(word, alphabet, k, n, ExtraLetter, o):
    wordlist = []
    for i in word:
        index = alphabet[0].index(i)
        wordlist.append(index)
    print(wordlist)
    wordlist = [wordlist[x : 1 + x] for x in range(0, len(wordlist), 1)]
    wordlist = [wordlist[x : n + x] for x in range(0, len(wordlist), n)]
    while len(k) != len(wordlist):
        k.append(newkey(k[len(k)-2],k[len(k)-1]))
    if o == 'dec':
        for i in range(len(k)):
            k[i] = np.linalg.inv(k[i])
    cl = []
    for i in range(len(wordlist)):
        total = np.array(k[i]).dot(np.array(wordlist[i]))
        for g in range(n):
            total[g][0] = int(total[g][0])
            total[g][0] = total[g][0] % 26
            if total[g][0] < 0:
                total[g][0] += 26
            if total[g][0] > 25:
                total[g][0] -= 26
            cl.append(int(total[g][0]))
    print(cl)
    Chiphertext = ''
    for i in cl:
        letter = alphabet[0][i]
        Chiphertext += letter
    if ExtraLetter == 0:
        return(Chiphertext)
    else:
        return(Chiphertext[:-ExtraLetter])


def key():
    k_str = input("Введите ключ по строкам матрицы через пробел:\n").split()
    key = []
    for element in k_str:
        key.append(int(element))
    n = int(math.sqrt(len(key)))
    key = [key[x : n + x] for x in range(0, len(key), n)]
    return(key, n)


def main():
    word = input("Введите слово:\n")
    k1, n1 = key()
    k2, n2 = key()
    k = []
    k.append(k1)
    k.append(k2)
    n = n1
    alphabet = [
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
]
    o = input("enc or dec:\n")
    ExtraLetter = 0
    if o == 'enc':
        while len(word) % n != 0:
            word += 'a'
            ExtraLetter += 1
    else:
        while len(word) % n != 0:
            word += 'i'
            ExtraLetter += 1
    ct = alg(word, alphabet, k, n, ExtraLetter, o)
    print(f'Результат:\n{ct}')

    
if __name__ == "__main__":
    main()