import logging
from table_struct import *
from sqlalchemy.orm import aliased, sessionmaker
from sqlalchemy import create_engine
import pandas as pd


class SqlReading:
    def __init__(self, set_config):
        self.version_id = set_config.get("versionId", "")
        self.analysis_id = set_config.get("analysisId", "")

        self.init_sql_info()
        self.engine = self.create_engine()

        self.sheet_sql_mapping = self.init_sheet_sql_mapping()

    def read_sql_by_sheet_name(self, sheet_name):
        """
        read data from sql by sheet_name in excel
        :param sheet_name:
        :return: dataframe
        """
        if sheet_name not in self.sheet_sql_mapping:
            _error = "请检查sheet_sql_mapping 中表格的配置信息"
            raise Exception(_error)
        # set alias  for tabel obj
        sql_info = self.sheet_sql_mapping[sheet_name]
        if sql_info["table_obj"] not in globals():
            _error = "请检查table_struct.py, 确定表{}结构已经定义".format(sheet_name)
            raise Exception(_error)
        # set alias name for tabel obj
        TmpObj = aliased(globals()[sql_info["table_obj"]])
        with self.create_session() as session:
            # get all columns needed by "cols"
            query = session.query(TmpObj).with_entities(
                *[getattr(TmpObj, i) for i in sql_info["cols"]]
            )
            for column, value in sql_info["filter"].items():
                if hasattr(self, value):
                    _filter_value = getattr(self, value)
                elif type(value) == str and str(value).lower in ["true", "yes"]:
                    _filter_value = True
                elif type(value) == str and str(value).lower in ["false", "no"]:
                    _filter_value = False
                else:
                    logging.error("unexpected value in filter in {}".format(sheet_name))
                    continue
                query = query.filter(getattr(TmpObj, column) == value)
            obj_df = pd.read_sql(query.statement, session.bind)
        obj_df.rename(columns=sql_info["cols"], inplace=True)
        return obj_df

    def init_sql_info(self):
        self.host = ""
        self.port = 3306
        self.user_name = ""
        self.password = ""
        self.database = ""
        self.charset = "utf8"

    def create_engine(self):
        _url = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(
            self.user_name, self.password, self.host, self.port, self.database,
            self.charset
        )
        engine = create_engine(_url)
        return engine

    def create_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

    def init_sheet_sql_mapping(self):
        """
        add all sheet and sql mapping info
        {
            sheet_name:
            "table_obj" : object for this table in table struct by sqlalchemy
            "cols" : mapping for each column between excel and sql
            "filter" : filter condition for this table
        }
        :return:
        """
        sheet_sql_mapping = {
            "sheet_name": {
                "table_obj": "ConfigMergeProductDemand",
                "cols": {
                    "factory_name": "工厂",
                    "pack": "PACK",
                    "product_name": "电芯PN",
                    "old_month": "原需求月份",
                    "merge_month": "合并后月份",
                    "merge_quantity": "合并数量(K)",
                },
                "filter": {
                    "valid": "YES",
                    "version_id": "version_id",
                    "analysis_id": "analysis_id"
                }
            },
        }
        return sheet_sql_mapping
