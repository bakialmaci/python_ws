gameResults = []
gameNumber = int(input())
Kayra = 0
Asya = 0

for i in range(gameNumber):
    gameResults.append(input().split())
for i in range(len(gameResults)):
    if (((int(gameResults[i][0]) % (int(gameResults[i][1])+2) <= int(gameResults[i][1])) and (int(gameResults[i][0]) != int(gameResults[i][1])+2) and (int(gameResults[i][1]) != int(gameResults[i][0]))) or ((int(gameResults[i][1])+2) > int(gameResults[i][0]))) and not(int(gameResults[i][1]) >= int(gameResults[i][0])):
        if gameResults[i][2] == "K":
            Kayra += 1
        else:
            Asya += 1
    else:
        if gameResults[i][2] == "A":
            Kayra += 1
        else:
            Asya += 1
    # print("asya", Asya)
    # print("kayra", Kayra)

if Kayra <= Asya:
    print("Kayra", Kayra)
else:
    print("Asya", Asya)
