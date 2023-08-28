from pyomo.environ import *
from pyomo.opt import SolverFactory
from time import time
model = ConcreteModel()

opt2 = SolverFactory('gurobi_persistent')
opt2.set_instance(model)


num = 200000
# 创建 ConstraintList
model.constraints = ConstraintList()

model.x = Var(range(num))
model.y = Var(range(num))
# print(model.x.value)


def rule(a, b):
    return a * model.x[a] + b * model.y[b] <= 3 * (a + b)


# 实例化求解器并将模型传递给它
opt = SolverFactory('gurobi_persistent')


for i, j in enumerate(range(1,num)):
    model.constraints.add(rule(i, j))
    # opt.add_constraint(model.constraints[i+1])
# 向 ConstraintList 中添加约束条件
# model.constraints.add(expr=2 * model.x + 3 * model.y <= 4)
# model.constraints.add(expr=model.x + model.y == 1)



# 添加新的约束到 ConstraintList 中
# new_constraint = model.x <= 0.5
# # tmp = Constraint(expr=2*model.x + 3*model.y <= 3)
# model.constraints.add(new_constraint)


# 将 ConstraintList 中的约束添加到求解器中
# for constraint in model.constraints.values():
#     opt.add_constraint(constraint)

obj_expr =  sum(model.x) +  sum(model.y)
model.obj = Objective(expr=obj_expr, sense=minimize)

print('set instance')
s = time()
opt.set_instance(model)
print(time() - s)

print('add var ans constraints')
s = time()
for i in model.x.values():
    opt2.add_var(i)
for i in model.y.values():
    opt2.add_var(i)
for constraint in model.constraints.values():
    opt.add_constraint(constraint)
opt2.set_objective(model.obj)
print(time() - s)

model.write('test.lp')
opt.write('test_opt.lp')
opt2.write('test_opt2.lp')
# 求解模型
results = opt.solve()

# 输出结果
results.write()









