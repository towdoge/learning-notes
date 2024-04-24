import os
import sys

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

print(work_dir)
print(file_name)

constraint_names = set()
with open(file_name, "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        try:
            if ":" == line.strip()[-1]:
                row = line.strip().split("(")[0]
                constraint_names.add(row)
        except:
            print("------{}".format(line))
    constraint_names = sorted(constraint_names)
for i in constraint_names:
    print(i)
