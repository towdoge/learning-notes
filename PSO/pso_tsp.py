import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------- #
# 参数设置
# -------------------------------------- #

distance_matrix = np.array([[0, 350, 290, 670, 600, 500, 660, 440, 720, 410, 480, 970],
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


N = 200  # 种群数量
D = 12  # 城市数量
T = 600  # 迭代次数
c1 = 1.5  # 个体学习因子
c2 = 2  # 群体学习因子
w_max = 0.9  # 权重系数最大值
w_min = 0.4
v_max = 3  # 每个维度的最大速度
v_min = -1
gb = np.ones(T)

# -------------------------------------- #
# 适应度函数 最小化 TSP问题中的旅行距离
# -------------------------------------- #

def tsp_distance(path,distmat):  # calculate distance
    distance = 0
    for i in range(len(path) - 1):
        distance += distmat[path[i]][path[i + 1]]
    distance += distmat[path[-1]][path[0]]
    return distance

# -------------------------------------- #
# 初始化种群个体
# -------------------------------------- #

# N个粒子，每个粒子的位置是一个城市的排列顺序
x = np.zeros((N, D), dtype=int)
for i in range(N):
    x[i] = np.random.permutation(D)
# x[N-1] = [8, 11, 7, 10, 9, 0, 2, 1, 4, 3, 5, 6]
# 初始化个体最优
p = x.copy()  # 每个粒子的历史个体最优位置
p_best = np.ones((N, 1)) * np.inf  # 初始化每个粒子的最优值
for i in range(N):
    p_best[i] = tsp_distance(x[i], distance_matrix)

# 初始化全局��优
g_best = np.inf  # 记录真正的全局最优
x_best = np.zeros(D)  # 记录最优粒子的城市排列顺序

# -------------------------------------- #
# 迭代求解
# -------------------------------------- #

for t in range(T):
    for i in range(N):  # 遍历每个粒子

        # 更新个体最优
        if tsp_distance(x[i], distance_matrix) < p_best[i]:
            p_best[i] = tsp_distance(x[i], distance_matrix)
            p[i] = x[i].copy()

        # 更新全局最优
        if p_best[i] < g_best:
            g_best = p_best[i]
            x_best = p[i].copy()

        # 计算动态的惯性权重
        w = w_max - (w_max - w_min) * t / T

        # 更新速度
        v = w * x[i] + \
            c1 * np.random.rand(D) * (p[i] - x[i]) + \
            c2 * np.random.rand(D) * (x_best - x[i])

        # 边界条件处理
        v[v > v_max] = v_max
        v[v < v_min] = v_min

        # 更新位置
        x[i] = np.floor(x[i] + v)
        tt = [i + idx / len(x[i]) for idx, i in enumerate(x[i])]
        tmp = sorted(tt)
        vvv = [tmp.index(k) for k in tt]
        if len(set(vvv)) != len(vvv):
            print('error')
        x[i] = vvv.copy()
        print(x[i])
        print(tsp_distance(x[i], distance_matrix))
    # 一轮迭代完成之后更新全局最优
    gb[t] = g_best

# -------------------------------------- #
# 查看结果
# -------------------------------------- #

print('最优距离:', gb[T - 1])
plt.plot(range(T), gb)
plt.show()