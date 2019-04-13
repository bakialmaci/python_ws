friendNumber = int(input())
requests = []
eachAverage = []
result = 0
r = 0
g = 0
b = 0
red_result = 0
green_result = 0
blue_result = 0

for _ in range(friendNumber):
    requests.append(input().split())

for _ in range(friendNumber):
    r += int(requests[_][0])
    g += int(requests[_][1])
    b += int(requests[_][2])

eachAverage.append(r / friendNumber)
eachAverage.append(g / friendNumber)
eachAverage.append(b / friendNumber)

for i in range(friendNumber):
    red_result += abs(int(requests[i][0]) - eachAverage[0])
    green_result += abs(int(requests[i][1]) - eachAverage[1])
    blue_result += abs(int(requests[i][2]) - eachAverage[2])

result = int(red_result + green_result + blue_result)

print(result)
