from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np

# 定义TSP问题
n = 5
d = np.array([[0, 1, 2, 3, 4],
              [1, 0, 1, 2, 3],
              [2, 1, 0, 1, 2],
              [3, 2, 1, 0, 1],
              [4, 3, 2, 1, 0]])

model = ConcreteModel()
model.x = Var(range(n), range(n), within=Binary)
model.obj = Objective(expr=sum(d[i,j]*model.x[i,j] for i in range(n) for j in range(n)))
model.con1 = ConstraintList()
for i in range(n):
    model.con1.add(sum(model.x[i,j] for j in range(n)) == 1)
model.con2 = ConstraintList()
for j in range(n):
    model.con2.add(sum(model.x[i,j] for i in range(n)) == 1)

# 定义列生成算法
def column_generation(model):
    opt = SolverFactory('gurobi')
    while True:
        # 求解松弛问题
        results = opt.solve(model, tee=False)
        print(results)
        # 检查是否存在非整数解
        int_sol = True
        for v in model.component_data_objects(Var, active=True):
            if abs(v.value - round(v.value)) > 1e-6:
                int_sol = False
                break
        # 如果存在非整数解，添加新的列
        if not int_sol:
            duals = np.zeros((n,n))
            for i,j in model.x.keys():
                duals[i,j] = model.con1[i].dual + model.con2[j].dual
            new_col = np.zeros(n)
            for i in range(n):
                new_col[i] = np.argmax(duals[i,:])
            model.x.add_component((len(model.x),range(n)), Var(within=Binary))
            model.obj.expr += sum(d[i,new_col[i]]*model.x[len(model.x)-1,i] for i in range(n))
            model.con1.add(sum(model.x[len(model.x)-1,j] for j in range(n)) == 1)
            model.con2.add(sum(model.x[i,len(model.x)-1] for i in range(n)) == 1)
        # 如果所有解都是整数解，结束
        else:
            break

# 调用列生成算法
column_generation(model)

# 输出最优解
print('Optimal solution:')
for i,j in model.x.keys():
    if round(model.x[i,j].value) == 1:
        print('x[',i,',',j,'] =', round(model.x[i,j].value))