def encryption(Plaintext):
    Ciphertext = ""
    for symbol in Plaintext:
        Ciphertext += NewEngList[EngList.index(symbol)]
    return Ciphertext


def decryption(Ciphertext):
    OriginalText = ""
    for symbol in Ciphertext:
        OriginalText += EngList[NewEngList.index(symbol)]
    return OriginalText


def main(text):
    Ciphertext = encryption(text)
    OriginalText = decryption(text)
    if input("enc or dec: ") == "enc":
        print("Сiphertext: ", Ciphertext)
    else:
        print("Original text: ", OriginalText)
 
        
if __name__ == "__main__":
    print("Key:")
    EngList = list(input("Alphabet:\n"))
    NewEngList = list(input("New alphabet:\n"))
    text = input("Text:\n")
    main(text)

"""Alphabet:
ABCDEFGHIJKLMNOPQRSTUVWXYZ
New alphabet:
FPRBVAWXHCDGITQJEKZNYULOMS"""