personNumber = int(input())
names = [[[97, 116, 97], [109, 101, 114, 116]]]
values = [[310, 440]]
temp1 = []
temp2 = []
temp4 = []
temp5 = []
max_giybet = []
indicator = 0


def calculate(x):
    a = 0
    b = 0
    for i in range(x):
        for j in range(x):
            a = abs(int(values[i + 1][0]) - int(values[j][0]))
            b = abs(int(values[i + 1][1]) - int(values[j][1]))
            max_giybet.append(a+b)
    print(max(max_giybet))


for _ in range(1, personNumber+1):
    x = 0
    y = 0
    names.append([int(ord(c)) for c in input()])
    for k in names[_]:
        if k == 32:
            indicator = 1
        elif indicator == 0:
            x += k
            temp1.append(k)
        else:
            y += k
            temp2.append(k)
    names[_] = []
    names[_].append(temp1)
    names[_].append(temp2)
    temp4.append(x)
    temp4.append(y)
    values.append(temp4)
    temp4 = []
    temp1 = []
    temp2 = []
    indicator = 0
    calculate(_)


