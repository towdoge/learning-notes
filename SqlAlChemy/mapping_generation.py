import inspect
import importlib.util
import logging
import re
import json


def get_all_class_in_file(file):
    """
    get all class in file
    :param file:
    :return:
    """
    # 导入py文件为模块
    spec = importlib.util.spec_from_file_location("module_name", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 获取模块中的所有成员
    members = inspect.getmembers(module)

    # 提取所有类
    classes = [
        obj
        for name, obj in inspect.getmembers(module)
        if inspect.isclass(obj) and obj.__module__ == module.__name__
    ]
    return classes


def get_sheet_name(name):
    pattern = r"(\d+\.\d+)"
    match = re.search(pattern, name)

    if match:
        version = match.group(1)
        return version
    return None


# get all class in sqlalchemy
file = "table_struct.py"
classes = get_all_class_in_file(file)
mapping = {}
error_info = []
for cls in classes:
    if not hasattr(cls, "__table_args__"):
        logging.error("****** {} no comment ******".format(cls.__name__))
        continue
    # get sheet name from comment in each class
    try:
        sheet_name = ""
        if type(cls.__table_args__) == dict:
            sheet_name = get_sheet_name(cls.__table_args__["comment"])
        else:
            for i in cls.__table_args__:
                if type(i) == dict and "comment" in i:
                    sheet_name = get_sheet_name(i["comment"])
        if not sheet_name:
            continue
    except Exception as e:
        raise Exception(e)
    if not sheet_name:
        print("****** {} no sheet name ******".format(cls.__name__))
        continue
    table_obj = cls.__name__
    cols = {}
    _filter = {}
    # get all columns in each table
    for column in cls.__table__.columns:
        col_name = column.name
        col_comment = column.comment
        if not col_comment:
            _error = "表格{} 的字段 {} 缺少注释".format(sheet_name, col_name)
            error_info.append(_error)
        # get some common filter
        if col_name == "valid":
            _filter[col_name] = "YES"
        if col_name == "version_id":
            _filter[col_name] = "version_id"
        if col_name == "analysis_id":
            _filter[col_name] = "analysis_id"
        # remove some common column that is useless
        if col_name in [
            "id",
            "creator",
            "creator_name",
            "create_time",
            "modifier",
            "modifier_name",
            "modify_time",
            "valid",
            "version_id",
            "analysis_id",
        ]:
            continue
        if "id" in col_name:
            continue

        cols[col_name] = col_comment
    # if same sheet name, output log
    while sheet_name in mapping:
        sheet_name += "_1"
        print("******error for sheet name {} ******".format(sheet_name))
    mapping[sheet_name] = {"table_obj": table_obj, "cols": cols, "filter": _filter}

    print(sheet_name, table_obj)

if error_info:
    print('--------------------------')
    tmp = "\n".join(error_info)
    print(tmp)
    raise Exception(tmp)

# sorted by sheet name
mapping = {k: mapping[k] for k in sorted(mapping)}

# output json file
with open("mapping.json", "w") as wl:
    json.dump(
        {str(k): mapping[k] for k in mapping},
        wl,
        indent=4,
        ensure_ascii=False,
    )
