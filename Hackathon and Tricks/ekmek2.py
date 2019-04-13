gameResults = []
gameNumber = int(input())
Kayra = 0
Asya = 0

for i in range(gameNumber):
    gameResults.append(input().split())
for i in range(len(gameResults)):
    print((int((int(gameResults[i][0])/(int(gameResults[i][1])+2))) % 2))
    if (int((int(gameResults[i][0])/(int(gameResults[i][1])+2))) % 2 == 0) and ((int(gameResults[i][0]) % (int(gameResults[i][1])+2)) >= int(gameResults[i][1])):
        if gameResults[i][2] == "K":
            Kayra += 1
        else:
            Asya += 1
    else:
        if gameResults[i][2] == "A":
            Kayra += 1
        else:
            Asya += 1
    # print("asya", Asya)1
    # print("kayra", Kayra)

if Kayra <= Asya:
    print("Kayra", Kayra)
else:
    print("Asya", Asya)
