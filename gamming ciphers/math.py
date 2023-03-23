one = [0,14,15,11,5,4,4,0,2,0,21,4,8,7,21,10,1,10,22,0,0,8,5,20,15,4]
another = [1,
0,
9,
3,
10,
12,
4,
0,
10,
12,
17,
7,
2,
8,
0,
7,
2,
20,
3,
10,
16,
21,
8,
2,
13,
13



]
a = []
for i in range(len(one)):
   a.append(one[i]*another[i]) 
print(a)
s = 0
for i in a:
    s += i
print(s)

