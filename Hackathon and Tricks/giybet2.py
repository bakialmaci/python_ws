personNumber = int(input())
names = [[[97, 116, 97], [109, 101, 114, 116]]]
values = [[310, 440]]
max_giybet = []


def calculate(x):
    for i in range(x):
        for j in range(x):
            a = abs(int(values[i + 1][0]) - int(values[j][0]))
            b = abs(int(values[i + 1][1]) - int(values[j][1]))
            max_giybet.append(a+b)
    print(max(max_giybet))


for _ in range(1, personNumber+1):
    x = 0
    y = 0
    indicator = 0
    temp4 = []
    names.append([int(ord(c)) for c in input()])
    for k in names[_]:
        if k == 32:
            indicator = 1
        elif indicator == 0:
            x += k
        else:
            y += k
    names[_] = []
    temp4.append(x)
    temp4.append(y)
    values.append(temp4)
    calculate(_)


