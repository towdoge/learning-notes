import numpy as np
import matplotlib.pyplot as plt
from mysql import *

MAXCOUNT = 10

def calDist(xid, yid, durationlist):
    for dura in durationlist:
        if dura['origin'] == xid and dura['destination'] == yid:
            return dura['duration']


def calPathDist(LocidList, durationlist):
    sum = 0
    for i in range(1, len(LocidList)):
        sum += calDist(LocidList[i], LocidList[i - 1], durationlist)
    return sum


# path1长度比path2短则返回true
def pathCompare(path1, path2, LocidList, durationlist):
    LocidList1 = []; LocidList2 = []
    for i in path1:
        LocidList1.append(LocidList[i])
    for i in path2:
        LocidList2.append(LocidList[i])
    if calPathDist(LocidList1, durationlist) <= calPathDist(LocidList2, durationlist):
        return True
    return False


def generateRandomPath(bestPath):
    a = np.random.randint(len(bestPath))
    while True:
        b = np.random.randint(len(bestPath))
        if np.abs(a - b) > 1:
            break
    if a > b:
        return b, a, bestPath[b:a + 1]
    else:
        return a, b, bestPath[a:b + 1]


def reversePath(path):
    rePath = path.copy()
    rePath = reversed(rePath)
    return list(rePath)


def updateBestPath(bestPath, LocidList, durationlist):
    count = 0
    while count < MAXCOUNT:
        start, end, path = generateRandomPath(bestPath)
        rePath = reversePath(path)
        # print('path:', path,'repath:', rePath, 'end:', end)
        if pathCompare(path, rePath, LocidList, durationlist):
            count += 1
            continue
        else:
            count = 0
            print('path:', path, 'repath:', rePath, 'end:', end)
            bestPath[start:end+1] = rePath
    return bestPath


def ProduceInput(routes):
    routes_pathindex = np.arange(0, len(routes))
    test = mysql()
    orderlist = test.findALLorder()
    duration = test.findALLduration()
    location = test.findAllloc()
    orderlist_route = []
    for order in orderlist:
        if str(order['OrderId']) in routes:
            orderlist_route.append(order)
    LocId = []
    for order in orderlist_route:
        LocId.append(test.findloc(order['Lat'], order['Lng']))

    return routes_pathindex, LocId, duration


if __name__ == '__main__':
    routes = ['40001', '40003', '40002', '40004', '40005', '40006', '40007', '40008']
    #注明：routes_pathindex是路径的下标，LocId保存的是所有点的位置，duration保存的是各个位置之间的距离单位
    (routes_pathindex, LocId, duration) = ProduceInput(routes)
    print(updateBestPath(routes_pathindex, LocId, duration))

