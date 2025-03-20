import ast
import os
from sys import platform
import pandas as pd

# set global split str
SPLIT_STR = "\\" if "win" in platform else "/"
cols = ["path", "file", "function", "start_line", "args_num", "lines","doc","whether_called"]
df_list = []


def count_lines(node):
    lines = node.end_lineno - node.lineno
    args_num = len(node.args.args)
    print(f"Function {node.name} " f"has {node.end_lineno - node.lineno} lines")
    return node.name, node.lineno, lines, args_num


def get_lines(file_path):
    file_name = file_path.split(SPLIT_STR)[-1]
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            name, start_line, lines, args_num = count_lines(node)
            docstring = ast.get_docstring(node, clean=False)
            whether_doc = docstring is not None
            whether_called = False
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Call) and isinstance(sub_node.func,
                                                                 ast.Name) and sub_node.func.id == name:
                    whether_called = True
                    break

            df_list.append([file_path, file_name, name, start_line, args_num, lines, whether_doc,whether_called])

def get_lines_for_all_files(work_dir):
    import numpy as np

    items = os.listdir(work_dir)
    for item in items:
        item_path = os.path.join(work_dir, item)
        if os.path.isdir(item_path):
            get_lines_for_all_files(item_path)
        elif item[-3:] == ".py":
            get_lines(item_path)


if __name__ == "__main__":
    work_dir = "D:\\project\\git\\xxx"
    get_lines_for_all_files(work_dir)
    if not df_list:
        print("no py file or no function")
    else:
        df = pd.DataFrame(df_list, columns=cols)
        df.to_csv("function_lines.csv", encoding="utf-8-sig", index=False)
        print(os.getcwd())
