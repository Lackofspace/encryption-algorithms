import math
import sys
import time




def ListNum(text, alphabet):
    IndexList = []
    for letter in text:
        index = alphabet[0].index(letter)
        IndexList.append(index)
    return IndexList


def encryption(WordList, e, n):
    C = []
    for element in WordList:
        C.append(element ** e % n)
    return C


def Word(ListNum, alphabet):
    word = ''
    for number in ListNum:
        index = alphabet[1].index(number)
        word += alphabet[0][index]
    return word


def decryption(EncryptionResult, d, n):
    m = []
    for element in EncryptionResult:
        m.append(int(element) ** d % n)
    return m

def gcd_extended(num1, num2):
    if num1 == 0:
        return (num2, 0, 1)
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return (div, y - (num2 // num1) * x, x)


def main():
    alphabet = [
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
         'v',
         'w', 'x', 'y', 'z'],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    ]
    start_time = time.time()
    user = input("Генерация ключей - 1\n"
                 "Зашифрование - 2\n"
                 "Расшифрование - 3 :\n")
    if user == "1":
        p = int(input("Введите простое число p = "))
        q = int(input("Введите простое число q = "))
        n = p * q
        f_n = (p - 1) * (q - 1)
        f = f_n - 1
        e = int(input(f'Выберите число e от 1 до {f} такое, '
        f'чтобы НОД(е, {f_n}) = 1\ne = '))
        if math.gcd(e, f_n) != 1:
            sys.exit(f'НОД({e}, {f_n}) != 1')
        num1, d, num2 = gcd_extended(e, f_n)
        if d < 0:
            d += f_n
        print(f'Открытый ключ: ({e}, {n})\nЗакрытый ключ: {d}')
    if user == "2":
        text = input("Введите текст: ").lower()
        e = int(input("Экспонента зашифрования е = "))
        n = int(input("Модуль алгоритма n = "))
        WordList = ListNum(text, alphabet)
        C = encryption(WordList, e, n)
        print(f'Результат зашифрования: {C}')
    if user == "3":
        EncryptionResult = input("Введите результат зашифрованного текста через пробел: \n").split()
        d = int(input("Экспонента расшифрования d = "))
        n = int(input("Модуль алгоритма n = "))
        List = decryption(EncryptionResult, d, n)
        word = Word(List, alphabet)
        print(f'Результат расшифрования: {word}')
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()