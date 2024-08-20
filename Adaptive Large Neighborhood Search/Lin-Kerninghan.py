import numpy as np
import random
import math

class LKH:
    def __init__(self, distance_matrix, T=0.9, max_k=5):
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.tour = None
        self.T = T
        self.max_k = max_k
        self.current_k = self.max_k  # 初始k值

    def initialize_tour(self):
        # 初始解可以使用多种启发式方法，这里使用最近邻算法
        self.tour = [i for i in range(self.num_cities)]
        current_city = 0
        while len(self.tour) < self.num_cities:
            next_city = np.argmin([self.distance_matrix[current_city][c] for c in range(self.num_cities) if c not in self.tour])
            self.tour.append(next_city)
            current_city = next_city


    def nearest_neighbor(self,cities, city_index):
        """
        使用k-d树
        如果问题涉及到动态更新城市位置或需要频繁查询城市之间的距离
        那么使用k-d树或其他空间索引结构可能会提高效率
        :param cities:
        :param city_index:
        :return:
        """
        from scipy.spatial import KDTree
        cities  # cities是一个二维数组，每一行是一个城市的坐标
        self.kd_tree = KDTree(cities)  # 构建k-d树
        # 使用k-d树找到最近的邻居
        distances, indices = self.kd_tree.query([self.cities[city_index]], k=2,
                                                return_distance=True)
        return indices[0][1]  # 返回最近邻居的索引

    def tour_distance(self):
        return sum(self.distance_matrix[self.tour[i % self.num_cities]][self.tour[(i + 1) % self.num_cities]] for i in range(self.num_cities))

    def adjust_search_intensity(self, iteration, max_iterations):
        """
        根据迭代次数调整搜索强度。

        :param iteration: 当前迭代次数。
        :param max_iterations: 总迭代次数。
        """
        # 随着迭代次数的增加，逐渐减小k值，降温搜索强度
        if iteration < max_iterations:
            self.current_k = int(self.max_k * (1 - self.T ** iteration))

    def swap_edges(self, a, b, c=None):
        # 交换两个或三个边缘的节点
        new_tour = self.tour.copy()
        if c is not None:
            # 三交换
            new_tour = new_tour[:a] + list(reversed(new_tour[a:b])) + new_tour[b:c] + list(reversed(new_tour[c:b])) + new_tour[c:]
        else:
            # 两交换
            new_tour = new_tour[:a] + [new_tour[b], new_tour[a]] + new_tour[b+1:]
        return new_tour

    # todo: 轮盘法，或者其他方法，切换search方法
    def perturb_tour(self):
        # 随机扰动当前路径以探索新的解空间
        a, b = sorted(random.sample(range(self.num_cities), 2))
        if random.random() < 0.5:  # 50% 概率选择两交换
            self.tour = self.swap_edges(a, b)
        else:  # 50% 概率选择三交换
            c = random.randint(a, b)
            self.tour = self.swap_edges(a, b, c)

    def local_search(self):
        # 局部搜索，尝试两交换和三交换
        best_tour = self.tour.copy()
        best_distance = self.tour_distance()
        for _ in range(100):  # 可以设置一个迭代次数
            for k in range(self.num_cities - 2):
                for i in range(k + 1, self.num_cities - 1):
                    for j in range(i + 1, self.num_cities):
                        new_tour = self.swap_edges(k, i, j)
                        new_distance = self.tour_distance(new_tour)
                        if new_distance < best_distance:
                            best_tour = new_tour
                            best_distance = new_distance
            self.tour = best_tour
        return best_tour, best_distance

    def k_opt_move(tour, k, distance_matrix):
        """
        执行k-opt移动来探索解空间。
        :param tour: 当前路径，一个城市索引的列表。
        :param k: k-opt中的k值，k > 2。
        :param distance_matrix: 城市间的距离矩阵。
        :return: 一个新的路径，如果k-opt移动改善了路径，则返回；否则返回None。
        """
        if k <= 2:
            raise ValueError("k must be greater than 2 for k-opt move.")

        # 检查路径长度是否足够进行k-opt
        if k > len(tour) - 1:
            raise ValueError("k is too large for the given tour length.")

        # 随机选择k个连续的城市进行反转
        start_index = random.randint(0, len(tour) - k)
        new_tour = tour[:start_index] + tour[start_index:start_index + k][::-1] + tour[
                                                                                  start_index + k:]

        # 计算原始路径和新路径的距离
        original_distance = sum(
            distance_matrix[tour[i % len(tour)]][tour[(i + 1) % len(tour)]] for i in
            range(len(tour)))
        new_distance = sum(distance_matrix[new_tour[i % len(new_tour)]][
                               new_tour[(i + 1) % len(new_tour)]] for i in
                           range(len(new_tour)))

        # 如果新路径的距离更短，则接受这个新路径
        if new_distance < original_distance:
            return new_tour
        else:
            return None

    def accept_worse_solution(self, current_distance, new_distance):
        """
        根据模拟退火准则接受更差的解。

        :param current_distance: 当前解的距离。
        :param new_distance: 新解的距离。
        :return: 如果接受新解，返回True；否则返回False。
        """
        if new_distance < current_distance:
            return True
        else:
            delta_e = new_distance - current_distance
            return random.random() < math.exp(-delta_e / self.current_temp)

    def run(self, iterations=100):
        self.initialize_tour()
        best_tour = self.tour.copy()
        best_distance = self.tour_distance()

        for _ in range(iterations):
            # self.perturb_tour()
            # current_tour, current_distance = self.local_search()
            new_tour = self.k_opt_move(best_tour)
            new_distance = self.tour_distance(new_tour)
            if self.accept_worse_solution(best_distance, new_distance):
                best_tour = new_tour
                best_distance = new_distance

            self.adjust_search_intensity() # 降温

        return best_tour, best_distance

# 示例：使用随机生成的距离矩阵
np.random.seed(42)
distance_matrix = np.random.rand(10, 10) * 100
distance_matrix = (distance_matrix + distance_matrix.T) / 2  # 确保矩阵是对称的

# 求解TSP问题
lkh = LKH(distance_matrix)
best_tour, best_distance = lkh.run(iterations=100)
print("Best Tour:", best_tour)
print("Best Distance:", best_distance)