import numpy as np
import copy
print("Loading data ...")
file = open("train.txt")
train_data = []
for line in file:
    tmp = line.split()[0: -1]
    n_tmp = [int(tmp[0]),int(tmp[1]),int(tmp[2])]
    train_data.append(n_tmp)
data_num = len(train_data)
print("%d TrainDataLoaded" % data_num)
file = open("test.txt")
test_data = []
for line in file:
    tmp = line.split()[0: -1]
    n_tmp = [int(tmp[0]),int(tmp[1]),int(tmp[2])]
    test_data.append(n_tmp)
test_num = len(test_data)
print("%d TestDataLoaded" % test_num)
print("Initializing ...")
miu = 0
max_u = 943
max_i = 1682
f = 10
gamma = 0.005
lambda4 = 0.02
bi = np.zeros((1,max_i))
bu = np.zeros((1,max_u))
q = np.zeros((f,max_i))
p = np.zeros((f,max_u))
for item in train_data:
    miu += item[2]
miu /= data_num
print("miu = %.3f" % miu)
e = 0
RMSE = 0
RMSE_pre = 0
k = 0
print("Start calc ...")
while(1):
    for data in train_data:
        u = data[0]
        i = data[1]
        r = data[2]
        r_p = miu + bi[:,i-1:i] +  bu[:,u-1:u] + np.dot(q[:,i-1:i].T, p[:,u-1:u])
        e = r - r_p
        RMSE += e * e
        bu[:,u-1:u] += gamma * (e - lambda4 * bu[:,u-1:u])
        bi[:,i-1:i] += gamma * (e - lambda4 * bi[:,i-1:i])
        q[:,i-1:i] += gamma * (e * p[:,u-1:u] - lambda4 * q[:,i-1:i])
        p[:,u-1:u] += gamma * (e * q[:,i-1:i] - lambda4 * p[:,u-1:u])
    RMSE = (RMSE / data_num) ** 0.5
    tRMSE = 0
    for data in test_data:
        u = data[0]
        i = data[1]
        r = data[2]
        r_p = miu + bi[:,i-1:i] +  bu[:,u-1:u] + np.dot(q[:,i-1:i].T, p[:,u-1:u])
        e = r - r_p
        tRMSE += e * e
    tRMSE = (tRMSE / test_num) ** 0.5
    k += 1
    print("round: %d , RMSE: %.4f , testRMSE: %.4f" % (k, RMSE, tRMSE))
    if np.abs(RMSE - RMSE_pre) < 0.001: break
    RMSE_pre = copy.deepcopy(RMSE)
print("Done.")
print("RMSE: %.4f , testRMSE: %.4f" % (RMSE, tRMSE))