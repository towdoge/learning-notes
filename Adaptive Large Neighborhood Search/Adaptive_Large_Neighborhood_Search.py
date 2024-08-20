# Adaptive Large Neighborhood Search
import numpy as np
import random as rd
import copy
from datetime import time

from sklearn.manifold import MDS
import matplotlib.pyplot as plt

# 设置随机种子以获得可重复的结果（可选）
np.random.seed(10)

city_num = 40
# 生成25个城市的随机坐标
cities_x = np.random.uniform(0, 1000, city_num)
cities_y = np.random.uniform(0, 1000, city_num)

# 打印城市坐标
print("城市坐标:")
for i, (x, y) in enumerate(zip(cities_x, cities_y)):
    print(f"城市 {i+1}: x = {x:.2f}, y = {y:.2f}")

# 创建距离矩阵
distmat = np.zeros((city_num, city_num))

# 计算欧几里得距离
for i in range(city_num):
    for j in range(i + 1, city_num):
        distance = np.sqrt(
            (cities_x[i] - cities_x[j]) ** 2 + (cities_y[i] - cities_y[j]) ** 2
        )
        distmat[i, j] = distance
        distmat[j, i] = distance  # 由于距离是对称的

# 打印距离矩阵
print("\n距离矩阵:")
print(distmat)

# 计算MDS坐标
mds = MDS(dissimilarity="precomputed", n_components=2, random_state=42)
coordinates = mds.fit_transform(distmat)
x_coords, y_coords = coordinates[:, 0], coordinates[:, 1]


def disCal(path):  # calculate distance
    distance = 0
    for i in range(len(path) - 1):
        distance += distmat[path[i]][path[i + 1]]
    distance += distmat[path[-1]][path[0]]
    return distance


def selectAndUseDestroyOperator(destroyWeight, currentSolution):
    """
    select and use destroy operators
    :param destroyWeight:
    :param currentSolution:
    :return:
    """
    destroyOperator = -1
    sol = copy.deepcopy(currentSolution)
    destroyRoulette = np.array(destroyWeight).cumsum()
    r = rd.uniform(0, max(destroyRoulette))
    for i in range(len(destroyRoulette)):
        if destroyRoulette[i] >= r:
            destroyOperator = i
            if i == 0:
                removedCities = randomDestroy(sol)
            elif i == 1:
                removedCities = max3Destroy(sol)
            elif i == 2:
                sol = swapDestroy(sol)
                removedCities = []
            destroyUseTimes[i] += 1
            break
    return sol, removedCities, destroyOperator


def selectAndUseRepairOperator(repairWeight, destroyedSolution, removeList):
    """
    select and use repair operators
    :param repairWeight:
    :param destroyedSolution:
    :param removeList:
    :return:
    """
    repairOperator = -1
    repairRoulette = np.array(repairWeight).cumsum()
    r = rd.uniform(0, max(repairRoulette))
    for i in range(len(repairRoulette)):
        if repairRoulette[i] >= r:
            repairOperator = i
            if i == 0:
                randomInsert(destroyedSolution)
            elif i == 1:
                greedyInsert(destroyedSolution)
            elif i == 2:
                destroyedSolution = nearestInsertion(destroyedSolution)
            repairUseTimes[i] += 1
            break
    return destroyedSolution, repairOperator


# 交换破坏算子
def swapDestroy(sol):
    i, j = rd.sample(range(len(sol)), 2)  # 随机选择两个不同的索引
    sol[i], sol[j] = sol[j], sol[i]  # 交换城市
    return sol




def randomDestroy(sol):  # randomly remove 3 cities
    solNew = copy.deepcopy(sol)
    removed = []
    removeIndex = rd.sample(range(0, distmat.shape[0]), 3)
    for i in removeIndex:
        removed.append(solNew[i])
        sol.remove(solNew[i])
    return removed


def max3Destroy(sol):  # remove city with 3 longest segments
    solNew = copy.deepcopy(sol)
    removed = []
    dis = []
    for i in range(len(sol) - 1):
        dis.append(distmat[sol[i]][sol[i + 1]])
    dis.append(distmat[sol[-1]][sol[0]])
    disSort = copy.deepcopy(dis)
    disSort.sort()
    for i in range(3):
        if dis.index(disSort[len(disSort) - i - 1]) == len(dis) - 1:
            removed.append(solNew[0])
            sol.remove(solNew[0])
        else:
            removed.append(solNew[dis.index(disSort[len(disSort) - i - 1]) + 1])
            sol.remove(solNew[dis.index(disSort[len(disSort) - i - 1]) + 1])
    return removed


def randomInsert(sol):  # randomly insert 3 cities
    notVisited = [city for city in range(distmat.shape[0]) if
                  city not in sol]
    insertIndex = rd.sample(range(0, distmat.shape[0]), len(notVisited))
    for i in range(len(insertIndex)):
        sol.insert(insertIndex[i], notVisited[i])


def greedyInsert(sol):  # greedy insertion
    notVisited = [city for city in range(distmat.shape[0]) if
                  city not in sol]
    dis = float("inf")
    insertIndex = -1
    for i in range(len(notVisited)):
        for j in range(len(sol) + 1):
            solNew = copy.deepcopy(sol)
            solNew.insert(j, notVisited[i])
            if disCal(solNew) < dis:
                dis = disCal(solNew)
                insertIndex = j
        sol.insert(insertIndex, notVisited[i])
        dis = float("inf")


# 最近插入修复算子
def nearestInsertion(sol):
    notVisited = [city for city in range(distmat.shape[0]) if
                  city not in sol]
    bestSolution = sol[:]
    for city in notVisited:
        bestDistance = float('inf')
        bestPos = -1
        for i in range(len(bestSolution) + 1):
            testSol = bestSolution[:]
            testSol.insert(i, city)
            testDistance = disCal(testSol)
            if testDistance < bestDistance:
                bestDistance = testDistance
                bestPos = i
        bestSolution.insert(bestPos, city)  # 插入城市到最佳位置
    return bestSolution

# 之前的代码保持不变，这里添加绘图相关的代码
def plot_path(solution, x_coords, y_coords):
    plt.clf()  # 清除之前的图形
    plt.scatter(x_coords, y_coords, c="red", label="Cities")  # 绘制城市

    # 绘制路径
    for i in range(len(solution) - 1):
        plt.plot(
            [x_coords[solution[i]], x_coords[solution[i + 1]]],
            [y_coords[solution[i]], y_coords[solution[i + 1]]],
            "b-",
        )
    # 关闭路径形成环
    plt.plot(
        [x_coords[solution[-1]], x_coords[solution[0]]],
        [y_coords[solution[-1]], y_coords[solution[0]]],
        "b-",
    )

    plt.legend()
    plt.title("TSP Solution at Iteration {}".format(iterx))
    plt.xlabel("MDS Dimension 1")
    plt.ylabel("MDS Dimension 2")
    plt.grid(True)
    plt.draw()  # 立即绘制图形
    plt.pause(0.01)  # 暂停一点时间以便观察


T = 100
a = 0.97
b = 0.5
num_for_operators = 3
wDestroy = [1 for i in range(num_for_operators)]  # weights of the destroy operators
wRepair = [1 for i in range(num_for_operators)]  # weights of the repair operators
# The number of times the destroy operator has been used
destroyUseTimes = [0 for i in range(num_for_operators)]
# The number of times the repair operator has been used
repairUseTimes = [0 for i in range(num_for_operators)]
destroyScore = [1 for i in range(num_for_operators)]  # the score of destroy operators
repairScore = [1 for i in range(num_for_operators)]  # the score of repair operators
solution = [i for i in range(distmat.shape[0])]  # initial solution
bestSolution = copy.deepcopy(solution)  # best solution
iterx, iterxMax = 0, 100

if __name__ == "__main__":
    while iterx < iterxMax:  # while stop criteria not met
        x = 0
        while T > 10:
            x += 1
            print('iterx {}'.format(iterx))
            destroyedSolution, remove, destroyOperatorIndex = (
                selectAndUseDestroyOperator(wDestroy, solution)
            )
            newSolution, repairOperatorIndex = selectAndUseRepairOperator(
                wRepair, destroyedSolution, remove
            )

            if disCal(newSolution) <= disCal(solution):
                solution = newSolution
                if disCal(newSolution) <= disCal(bestSolution):
                    bestSolution = newSolution
                    # update the score of the operators
                    destroyScore[destroyOperatorIndex] += 1.5
                    repairScore[repairOperatorIndex] += 1.5
                else:
                    destroyScore[destroyOperatorIndex] += 1.2
                    repairScore[repairOperatorIndex] += 1.2
            else:
                if rd.random() < np.exp(-disCal(newSolution) / T):
                    # the simulated annealing acceptance criteria
                    solution = newSolution
                    destroyScore[destroyOperatorIndex] += 0.8
                    repairScore[repairOperatorIndex] += 0.8
                else:
                    destroyScore[destroyOperatorIndex] += 0.6
                    repairScore[repairOperatorIndex] += 0.6

            wDestroy[destroyOperatorIndex] = wDestroy[destroyOperatorIndex] * b + (
                1 - b
            ) * (
                destroyScore[destroyOperatorIndex]
                / destroyUseTimes[destroyOperatorIndex]
            )
            wRepair[repairOperatorIndex] = wRepair[repairOperatorIndex] * b + (
                1 - b
            ) * (repairScore[repairOperatorIndex] / repairUseTimes[repairOperatorIndex])
            # update the weight of the operators
            print(x, T, destroyScore, repairScore, iterx)
            print(bestSolution)
            print(disCal(bestSolution))

            plot_path(solution, x_coords, y_coords)  # 绘制最佳路径
            T = a * T
        iterx += 1
        T = 100

    print(bestSolution)
    print(disCal(bestSolution))