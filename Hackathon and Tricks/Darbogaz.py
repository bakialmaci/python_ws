features = []
price_performance = []
user = list(map(float, input().split()))

for i in range(int(user[0])):
    features_temp = list(map(float, input().split()))
    features.append(features_temp)

for i in range(int(user[0])):
    if int(user[4]) >= int(features[i][0]):
        for j in range(1, int(user[1])):  # 1,2,3
            if features[i][j] - features[i][j+1] > int(user[2]):
                features[i][j] = features[i][j+1]+int(user[2])
        if sum(features[i][1:]) >= int(user[3]):
            price_performance.append(sum(features[i][1:])/int(features[i][0]))
        else:
            price_performance.append(-1)
    else:
            price_performance.append(-1)

if max(price_performance) == -1:
    print(-1)
else:
    print(price_performance.index(max(price_performance))+1)
