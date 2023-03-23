def MakeList(word, alphabet):
    WordList = []
    for symbol in word:
        LetterIndex = alphabet[0].index(symbol)
        WordList.append(alphabet[1][LetterIndex])
    return(WordList)


def ImprovedKey(keyList, LenWordList):
    LenKeyList = len(keyList)
    FullPart = (LenWordList // LenKeyList) * keyList
    slice_object = slice(LenWordList % LenKeyList) 
    ExtendedKeyList = FullPart + keyList[slice_object]
    return(ExtendedKeyList)


def Mod26(number):
    if number > 25:
        number -= 26
    if number < 0:
        number += 26
    return(number)


def Encoding(wordList, keyList):
    EncodedList = []
    for index in range(len(wordList)):
        EncodedList.append(Mod26(wordList[index] + keyList[index]))
    return(EncodedList)
    
    
def Decoding(wordList, keyList):
    DecodedList = []
    for index in range(len(wordList)):
        DecodedList.append(Mod26(wordList[index] - keyList[index]))
    return(DecodedList)


def MakeWord(WordList, alphabet):
    Word = ''
    for index in WordList:
        letter = alphabet[1].index(index)
        Word += alphabet[0][letter]
    return(Word)


def main():
    alphabet = [
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
]
    word = input('Word:\n').lower()
    wordList = MakeList(word, alphabet)
    key = input('Key:\n')
    keyList = MakeList(key, alphabet)
    keyList = ImprovedKey(keyList, len(wordList))
    choice = input("Encoding - 1, Decoding - 2:\n")
    if choice == '1':
        ResultList = Encoding(wordList, keyList)
        result = MakeWord(ResultList, alphabet)
        print(f'Result: {result}')
    if choice == '2':
        ResultList = Decoding(wordList, keyList)
        result = MakeWord(ResultList, alphabet)
        print(f'Result: {result}')
    
if __name__ == "__main__":
    main()
    

