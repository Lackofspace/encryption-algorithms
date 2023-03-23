import math

def gcd_extended(num1, num2):
    if num1 == 0:
        return (num2, 0, 1)
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return (div, y - (num2 // num1) * x, x)


def CreateZAndZm(EngList):
    Z = list(range(len(EngList)))
    Zm = [1]
    for i in range(2, len(EngList)):
        if math.gcd(len(EngList), i) == 1:
            Zm.append(i)
    return(Z, Zm)

def CreateKey(Text, a1, a2, b1, b2):
    key = [[0] * 2 for i in range(len(Text))]
    for j in range(len(Text)):
        if j == 0:
            key[j][0], key[j][1] = a1, b1
        if j == 1:
            key[j][0], key[j][1] = a2, b2
        if j >=2:
            key[j][0] = (key[j-1][0] * key[j-2][0]) % len(EngList)
            key[j][1] = (key[j-1][1] * key[j-2][1]) % len(EngList)
    return key


def decryption(Text, key, EngList):
    OriginalText = ""
    for i in range(len(Text)):
        a, b = key[i][0], key[i][1]
        num = gcd_extended(len(EngList), a)[2]
        if num < 0:
            num += len(EngList)
        Index = EngList.index(Text[i])
        NewIndex = ((Index - b) * num) % len(EngList)
        OriginalText += EngList[NewIndex]
    return OriginalText
    


def main(Text, EngList, Z, Zm):
    for i in Zm:
        a1 = i
        for j in Zm:
            a2 = j
            for m in Z:
                b1 = m
                for n in Z:
                    b2 = n
                    key = CreateKey(Text, a1, a2, b1, b2)
                    Result = decryption(Text, key, EngList)
                    print(f'a1 = {a1}, b1 = {b1}, a2 = {a2}, b2 = {b2}: {Result}')


if __name__ == "__main__":
    EngList = list(input("Alphabet:\n"))
    Text = input("Text:\n")
    Z, Zm = CreateZAndZm(EngList)
    main(Text, EngList, Z, Zm)
    