import math

def gcd_extended(num1, num2):
    if num1 == 0:
        return (num2, 0, 1)
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return (div, y - (num2 // num1) * x, x)



def decryption(Ciphertext, a, b):
    OriginalText = ""
    num = gcd_extended(len(EngList), a)[2]
    if num < 0:
        num += len(EngList)
    for symbol in Ciphertext:
        Index = EngList.index(symbol)
        NewIndex = ((Index - b) * num) % len(EngList)
        OriginalText += EngList[NewIndex]
    print(f'a = {a}, b = {b}: {OriginalText}')
    
    
def CreateZAndZm(EngList):
    Z = list(range(len(EngList)))
    Zm = [1]
    for i in range(2, len(EngList)):
        if math.gcd(len(EngList), i) == 1:
            Zm.append(i)
    return(Z, Zm)
    
def main(Text, Z, Zm):
    for i in Zm:
        a = i
        for j in Z:
            b = j
            decryption(Text, a, b)

if __name__ == "__main__":
    EngList = list(input("Alphabet:\n"))
    Text = input("Text:\n")
    Z, Zm = CreateZAndZm(EngList)
    main(Text, Z, Zm)