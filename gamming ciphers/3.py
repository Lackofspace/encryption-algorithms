import copy


def MakeList(word, alphabet):
    WordList = []
    for symbol in word:
        LetterIndex = alphabet[0].index(symbol)
        WordList.append(alphabet[1][LetterIndex])
    return(WordList)


def KeyList(key, wordList, alphabet):
    LetterIndex = alphabet[0].index(key)
    keyList = copy.deepcopy(wordList)
    keyList.insert(0, alphabet[1][LetterIndex])
    keyList = keyList[:-1]
    return keyList


def Mod26(number):
    if number > 25:
        number -= 26
    if number < 0:
        number += 26
    return(number)


def Decoding(wordList, keyList):
    EncodedList = []
    for index in range(len(wordList)):
        EncodedList.append(Mod26(wordList[index] - keyList[index]))
    return(EncodedList)


def MakeWord(WordList, alphabet):
    Word = ''
    for index in WordList:
        letter = alphabet[1].index(index)
        Word += alphabet[0][letter]
    return(Word)


def Encoding(wordList, alphabet, key):
    LetterIndex = alphabet[0].index(key)
    KeyIndex = alphabet[1][LetterIndex]
    ResultList = []
    ResultList.append(Mod26(wordList[0] + KeyIndex))
    for index in range(1, len(wordList)):
        Element = Mod26(wordList[index] + ResultList[index - 1])
        ResultList.append(Element)
    return ResultList


def main():
    alphabet = [
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
]
    word = input('Word:\n')
    wordList = MakeList(word, alphabet)
    key = input('Key letter:\n') 
    choice = input("Encoding - 1, Decoding - 2:\n")
    if choice == '1':
        ResultList = Encoding(wordList, alphabet, key)
        result = MakeWord(ResultList, alphabet)
        print(f'Result: {result}')
    if choice == '2':
        keyList = KeyList(key, wordList, alphabet)
        ResultList = Decoding(wordList, keyList)
        result = MakeWord(ResultList, alphabet)
        print(f'Result: {result}')
        

if __name__ == '__main__':
    main()