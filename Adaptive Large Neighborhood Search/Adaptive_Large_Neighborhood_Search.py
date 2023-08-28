# Adaptive Large Neighborhood Search
import numpy as np
import random as rd
import copy

distmat = np.array([[0, 350, 290, 670, 600, 500, 660, 440, 720, 410, 480, 970],
                    [350, 0, 340, 360, 280, 375, 555, 490, 785, 760, 700, 1100],
                    [290, 340, 0, 580, 410, 630, 795, 680, 1030, 695, 780, 1300],
                    [670, 360, 580, 0, 260, 380, 610, 805, 870, 1100, 1000, 1100],
                    [600, 280, 410, 260, 0, 610, 780, 735, 1030, 1000, 960, 1300],
                    [500, 375, 630, 380, 610, 0, 160, 645, 500, 950, 815, 950],
                    [660, 555, 795, 610, 780, 160, 0, 495, 345, 820, 680, 830],
                    [440, 490, 680, 805, 735, 645, 495, 0, 350, 435, 300, 625],
                    [720, 785, 1030, 870, 1030, 500, 345, 350, 0, 475, 320, 485],
                    [410, 760, 695, 1100, 1000, 950, 820, 435, 475, 0, 265, 745],
                    [480, 700, 780, 1000, 960, 815, 680, 300, 320, 265, 0, 585],
                    [970, 1100, 1300, 1100, 1300, 950, 830, 625, 485, 745, 585, 0]])


def disCal(path):  # calculate distance
    distance = 0
    for i in range(len(path) - 1):
        distance += distmat[path[i]][path[i + 1]]
    distance += distmat[path[-1]][path[0]]
    return distance


def selectAndUseDestroyOperator(destroyWeight,
                                currentSolution):  # select and use destroy operators
    destroyOperator = -1
    sol = copy.deepcopy(currentSolution)
    destroyRoulette = np.array(destroyWeight).cumsum()
    r = rd.uniform(0, max(destroyRoulette))
    for i in range(len(destroyRoulette)):
        if destroyRoulette[i] >= r:
            if i == 0:
                destroyOperator = i
                removedCities = randomDestroy(sol)
                destroyUseTimes[i] += 1
                break
            elif i == 1:
                destroyOperator = i
                removedCities = max3Destroy(sol)
                destroyUseTimes[i] += 1
                break
    return sol, removedCities, destroyOperator


def selectAndUseRepairOperator(repairWeight, destroyedSolution,
                               removeList):  # select and use repair operators
    repairOperator = -1
    repairRoulette = np.array(repairWeight).cumsum()
    r = rd.uniform(0, max(repairRoulette))
    for i in range(len(repairRoulette)):
        if repairRoulette[i] >= r:
            if i == 0:
                repairOperator = i
                randomInsert(destroyedSolution, removeList)
                repairUseTimes[i] += 1
                break
            elif i == 1:
                repairOperator = i
                greedyInsert(destroyedSolution, removeList)
                repairUseTimes[i] += 1
                break
    return destroyedSolution, repairOperator


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


def randomInsert(sol, removeList):  # randomly insert 3 cities
    insertIndex = rd.sample(range(0, distmat.shape[0]), 3)
    for i in range(len(insertIndex)):
        sol.insert(insertIndex[i], removeList[i])


def greedyInsert(sol, removeList):  # greedy insertion
    dis = float("inf")
    insertIndex = -1
    for i in range(len(removeList)):
        for j in range(len(sol) + 1):
            solNew = copy.deepcopy(sol)
            solNew.insert(j, removeList[i])
            if disCal(solNew) < dis:
                dis = disCal(solNew)
                insertIndex = j
        sol.insert(insertIndex, removeList[i])
        dis = float("inf")


T = 100
a = 0.97
b = 0.5
wDestroy = [1 for i in range(2)]  # weights of the destroy operators
wRepair = [1 for i in range(2)]  # weights of the repair operators
destroyUseTimes = [0 for i in
                   range(2)]  # The number of times the destroy operator has been used
repairUseTimes = [0 for i in
                  range(2)]  # The number of times the repair operator has been used
destroyScore = [1 for i in range(2)]  # the score of destroy operators
repairScore = [1 for i in range(2)]  # the score of repair operators
solution = [i for i in range(distmat.shape[0])]  # initial solution
bestSolution = copy.deepcopy(solution)  # best solution
iterx, iterxMax = 0, 100

if __name__ == '__main__':
    while iterx < iterxMax:  # while stop criteria not met
        x = 0
        while T > 10:
            x += 1
            print(iterx)
            destroyedSolution, remove, destroyOperatorIndex = selectAndUseDestroyOperator(
                wDestroy, solution)
            newSolution, repairOperatorIndex = selectAndUseRepairOperator(wRepair,
                                                                          destroyedSolution,
                                                                          remove)

            if disCal(newSolution) <= disCal(solution):
                solution = newSolution
                if disCal(newSolution) <= disCal(bestSolution):
                    bestSolution = newSolution
                    destroyScore[
                        destroyOperatorIndex] += 1.5  # update the score of the operators
                    repairScore[repairOperatorIndex] += 1.5
                else:
                    destroyScore[destroyOperatorIndex] += 1.2
                    repairScore[repairOperatorIndex] += 1.2
            else:
                if rd.random() < np.exp(- disCal(
                        newSolution) / T):  # the simulated annealing acceptance criteria
                    solution = newSolution
                    destroyScore[destroyOperatorIndex] += 0.8
                    repairScore[repairOperatorIndex] += 0.8
                else:
                    destroyScore[destroyOperatorIndex] += 0.6
                    repairScore[repairOperatorIndex] += 0.6

            wDestroy[destroyOperatorIndex] = wDestroy[destroyOperatorIndex] * b + (
                        1 - b) * \
                                             (destroyScore[destroyOperatorIndex] /
                                              destroyUseTimes[destroyOperatorIndex])
            wRepair[repairOperatorIndex] = wRepair[repairOperatorIndex] * b + (1 - b) * \
                                           (repairScore[repairOperatorIndex] /
                                            repairUseTimes[repairOperatorIndex])
            # update the weight of the operators
            print(x, T, destroyScore, repairScore, iterx)
            print(bestSolution)
            print(disCal(bestSolution))
            T = a * T
        iterx += 1
        T = 100

    print(bestSolution)
    print(disCal(bestSolution))
