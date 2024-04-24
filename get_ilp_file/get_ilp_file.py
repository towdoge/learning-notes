import gurobipy as gb
import os
import sys
import pandas as pd

work_dir = os.getcwd() if len(sys.argv) <= 1 else sys.argv[1]
os.chdir(work_dir)
SPLIT_STR = "\\" if "win" in sys.platform else "/"
work_dir = os.getcwd()
file_names = [
    f
    for f in os.listdir(work_dir)
    if f[-3:] == ".lp" and ("~" not in f) and "label" not in f
]
file_names.sort(key=lambda f: os.path.getmtime(work_dir + SPLIT_STR + f))
file_name = file_names[-1]
if os.path.exists("file_name.txt"):
    input_file_name = pd.read_csv("file_name.txt", names=["file"])
    if len(input_file_name) > 0:
        file_name = input_file_name.file.values[0]
        if file_name[-3:] != ".lp":
            file_name += ".lp"

# file_name = 'slack.lp'
print(work_dir)
print(file_name)

model = gb.gurobi.read(file_name)
model.optimize()
if model.Status == gb.GRB.INFEASIBLE:
    model.computeIIS()
    model.write("infeasible.ilp")
