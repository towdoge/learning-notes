import gurobipy as gb
import os
import sys
import pandas as pd

work_dir = os.getcwd() if len(sys.argv) <= 1 else sys.argv[1]
os.chdir(work_dir)
SPLIT_STR = "\\" if "win" in sys.platform else "/"
work_dir = os.getcwd()
file_names = [f for f in os.listdir(work_dir) if f[-3:] == ".lp" and ("~" not in f)]
file_names.sort(key=lambda f: os.path.getmtime(work_dir + SPLIT_STR + f))
file_name = file_names[-1]
if os.path.exists("file_name.txt"):
    input_file_name = pd.read_csv("file_name.txt", names=["file"])
    if len(input_file_name) > 0:
        file_name = input_file_name.file.values[0]
        if file_name[-3:] != ".lp":
            file_name += ".lp"

print(work_dir)
print(file_name)

model = gb.gurobi.read(file_name)

# 记录所有变量和约束的信息
vars_info = {v.VarName: v for v in model.getVars()}
cons_info = {c.ConstrName: c for c in model.getConstrs()}

presolved_model = model.presolve()

prev_vars_info = {v.VarName: v for v in presolved_model.getVars()}
prev_cons_info = {c.ConstrName: c for c in presolved_model.getConstrs()}

# 检查哪些变量被删除
removed_vars = [v.VarName for k, v in vars_info.items() if k not in prev_vars_info]
print('Removed variables:', removed_vars)

# 检查哪些约束被删除
removed_cons = [c.ConstrName for k, c in cons_info.items() if k not in prev_cons_info]
print('Removed constraints:', removed_cons)

presolved_model.write("presolved.lp")
model.optimize()
# model.write("model.lp")
