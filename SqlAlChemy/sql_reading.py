#!/usr/bin/env Python
# coding=utf-8
import logging
import pandas as pd
from sqlalchemy import inspect
from uuid import uuid3, NAMESPACE_DNS
from time import time
from sql_connection import SqlConnection
from table_struct import *
from table_setting import pro_sql_sheet_map


class SqlReading:
    def __init__(self, set_config):
        # for query data
        self.analysis_id = set_config.get("queryAnalysisId", "")
        # for output data
        self.output_analysis_id = set_config.get("analysisId", "")
        self.version_id = set_config.get("versionId", "")
        self.set_config = set_config

        self.sql_conn = SqlConnection()
        self.sheet_sql_mapping = pro_sql_sheet_map

    def set_output_time(self, time_str):
        """
        set output time as create time for all output
        :param time_str:
        :return:
        """
        self.time_str = time_str

    def add_filter_for_query(
        self, TmpObj, query, sql_info, version_id="", analysis_id=""
    ):
        """
        add filter for query by sql info filter
        :param TmpObj:
        :param query:
        :param sql_info:
        :param version_id:
        :param analysis_id:
        :return:
        """
        # add filter for query by "filter_equal"
        for column, value in sql_info.get("filter_equal", {}).items():
            # filter special version id by parameter
            if value == "version_id" and version_id:
                _filter_value = version_id
            # filter special analysis id by parameter
            elif value == "analysis_id" and analysis_id:
                _filter_value = analysis_id
            elif isinstance(value, int):
                _filter_value = value
            # if is attribute in self
            elif isinstance(value, str) and hasattr(self, value):
                _filter_value = getattr(self, value)
            # if str value
            elif isinstance(value, str):
                _filter_value = value
            else:
                continue
            query = query.filter(getattr(TmpObj, column) == _filter_value)

        for column, value in sql_info.get("filter_not_equal", {}).items():
            if isinstance(value, int):
                _filter_value = value
            # if is attribute in self
            elif isinstance(value, str) and hasattr(self, value):
                _filter_value = getattr(self, value)
            # if str value
            elif isinstance(value, str):
                _filter_value = value
            else:
                continue
            query = query.filter(getattr(TmpObj, column) != _filter_value)

        # add filter query by "filter_in"
        for column, value in sql_info.get("filter_in", {}).items():
            if isinstance(value, str) and hasattr(self, value):
                _filter_value = getattr(self, value)
            else:
                continue
            query = query.filter(getattr(TmpObj, column).in_(_filter_value))
        return query

    def read_sql_by_sheet_name(self, sheet_name, version_id="", analysis_id=""):
        """
        read data from sql by sheet_name
        :param sheet_name: read sheet name
        :param version_id: if filter by special version id, default self.version_id
        :param analysis_id: if filter by special analysis id, default self.analysis id
        :param whether_delete: whether delete the data at database
        :return: dataframe
        """
        if sheet_name not in self.sheet_sql_mapping:
            _error = "请检查sheet_sql_mapping 中表格的配置信息"
            raise Exception(_error)
        sql_info = self.sheet_sql_mapping[sheet_name]
        if sql_info["table_obj"] not in globals():
            _error = "请检查table_struct.py, 确定表{}结构已经定义".format(sheet_name)
            raise Exception(_error)
        # set TmpObj for tabel obj
        TmpObj = globals()[sql_info["table_obj"]]
        with self.sql_conn.create_session() as session:
            # query all columns if needed in "cols"
            query = session.query(TmpObj).with_entities(
                *[getattr(TmpObj, i) for i in sql_info["cols"]]
            )
            query = self.add_filter_for_query(
                TmpObj, query, sql_info, version_id, analysis_id
            )
            obj_df = pd.read_sql(query.statement, session.bind)
        # reset original columns name
        # change columns from quoted_name to str
        obj_df.columns = [str(i) for i in obj_df.columns]
        obj_df.rename(columns=sql_info["cols"], inplace=True)
        return obj_df

    def delete_sql_with_version(
        self, sheet_name, version_id="", analysis_id="", session=None
    ):
        """
        delete table with a version_id and analysis_id
        :param sheet_name:
        :param version_id:
        :param analysis_id:
        :param session:
        :return:
        """
        if sheet_name not in self.sheet_sql_mapping:
            _error = "请检查sheet_sql_mapping 中表格的配置信息"
            raise Exception(_error)
        sql_info = self.sheet_sql_mapping[sheet_name]
        if sql_info["table_obj"] not in globals():
            _error = "请检查table_struct.py, 确定表{}结构已经定义".format(sheet_name)
            raise Exception(_error)
        # set TmpObj for tabel obj
        TmpObj = globals()[sql_info["table_obj"]]
        # query all cols
        query = session.query(TmpObj).with_entities(TmpObj)

        query = self.add_filter_for_query(
            TmpObj, query, sql_info, version_id, analysis_id
        )
        obj_df = pd.read_sql(query.statement, session.bind)
        logging.info("delete {} data from {}".format(len(obj_df), sheet_name))
        query.delete()
        session.commit()
        # reset original columns name
        # change columns from quoted_name to str
        obj_df.columns = [str(i) for i in obj_df.columns]
        obj_df.rename(columns=sql_info["cols"], inplace=True)
        return obj_df

    def get_uuid(self, idx):
        """
        get uuid by time now and idx
        :param idx:
        :return:
        """
        # add idx, because only time() would be duplicated, code run too fast
        return uuid3(NAMESPACE_DNS, "{}_{}".format(str(time()), str(idx)))

    def insert_fix_cols_to_data(self, _data: list, add_uuid=True, modify=False):
        """
        add fix cols for each _data
        :param _data: [{column1: value, column2: value}, {}]
        :param add_uuid: add uuid_str for data
        :param modify: add modifier time for data
        :return:
        """
        for idx, data in enumerate(_data):
            data["creator"] = self.set_config.get("creatorId", "")
            data["creator_name"] = self.set_config.get("creatorName", "")
            data["create_time"] = self.time_str
            data["modifier"] = self.set_config.get("modifier", "")
            data["modifier_name"] = self.set_config.get("modifier_name", "")
            data["modifier_time"] = None
            if modify:
                data["modifier_time"] = self.time_str
            if "valid" not in data:
                data["valid"] = "YES"
            data["analysis_id"] = self.output_analysis_id
            data["version_id"] = self.version_id
            if add_uuid:
                data["id"] = str(self.get_uuid(idx))
        return _data

    def update_sql_info_for_output(self, sql_info: dict):
        """
        add fixed cols for table_obj
        :param sql_info:
        :return:
        """
        tmp = {
            "creator": "creator",
            "creator_name": "creator_name",
            "create_time": "create_time",
            "modifier": "modifier",
            "modifier_name": "modifier_name",
            "modifier_time": "modifier_time",
            "valid": "valid",
            "analysis_id": "analysis_id",
            "version_id": "version_id",
        }
        sql_info["cols"].update(tmp)
        return sql_info

    def insert_data_to_sql(
        self,
        sheet_name,
        data,
        add_fix_cols=False,
        add_uuid=True,
        modify=False,
        version_id="",
        analysis_id="",
        iter_step: int = 4000,
        session=None,
    ):
        """
        delete data for this version first, then insert data to sql
        :param sheet_name:
        :param data: [{column1: value, column2: value}, {}]
        :param add_fix_cols:if add fixed cols for output
        :param add_uuid: whether add id for _data
        :param modify: whether add modify time
        :param version_id: special version_id
        :param analysis_id: special analysis_id
        :param iter_step: iter stop for inserting to sql
        :param session: self.sql_conn.create_session()
        :return:
        """
        logging.info("there are {} data to sql for {}".format(len(data), sheet_name))
        sql_info = self.sheet_sql_mapping[sheet_name]
        if add_fix_cols:
            sql_info = self.update_sql_info_for_output(sql_info)
            data = self.insert_fix_cols_to_data(data, add_uuid, modify)
        map_info = {v: k for k, v in sql_info["cols"].items()}
        TmpObj = globals()[sql_info["table_obj"]]
        if sheet_name not in inspect(self.sql_conn.engine).get_table_names():
            TmpObj.__table__.create(self.sql_conn.engine)
        # delete data in database first for this version id and analysis_id
        self.delete_sql_with_version(
            sheet_name=sheet_name,
            version_id=version_id,
            analysis_id=analysis_id,
            session=session,
        )
        # insert iter_step rows into sql each time
        iter_step = int(iter_step)
        i = 0
        while i * iter_step < len(data):
            logging.info("insert {} iter time with step {}".format(i, iter_step))
            for idx, item in enumerate(data[i * iter_step : (i + 1) * iter_step]):
                tmp_obj = globals()[sql_info["table_obj"]]()
                for k, v in item.items():
                    setattr(tmp_obj, map_info[k], v)
                session.add(tmp_obj)
            session.commit()
            i += 1

    def init_sheet_sql_mapping(self):
        """
        add all sheet and sql mapping info
        {
            sheet_name:
            "table_obj" : object for this table in table struct by sqlalchemy
            "cols" : mapping for each column between excel and sql
            "filter_equal" : filter condition for this table
        }
        :return:
        """
        sheet_sql_mapping = pro_sql_sheet_map
        return sheet_sql_mapping

    def convert_df_to_sql_data(
        self, df: pd.DataFrame, fix_cols=None, dynamic_cols=None, filter_zero=False
    ):
        """
        transfer dataframe to sql data
        :param df:
        :param fix_cols: fix cols
        :param dynamic_cols: always means time and value
        :param filter_zero: True means not nonzero value into sql
        :return:
        """
        if fix_cols is None:
            fix_cols = df.columns
        if dynamic_cols is None:
            dynamic_cols = []
        # add column index if needed
        if "index" in fix_cols and "index" not in df.columns:
            df["index"] = df.index
        _data = []
        for idx, row in df.iterrows():
            _row = row.loc[fix_cols].to_dict()
            for k, v in _row.items():
                if pd.isna(v):
                    _row[k] = None
            # add dynamic cols
            all_is_zero = True
            for i in dynamic_cols:
                new_row = {}
                _value = row[i]
                _is_zero = self.is_instance_number(_value) and _value == 0
                if filter_zero and _is_zero:
                    continue
                all_is_zero = False
                new_row["time"] = i
                new_row["value"] = _value
                new_row.update(_row)
                # add _row for each value
                _data.append(new_row)
            # add at least one line if all value is zero, add first col as value zero
            if dynamic_cols and all_is_zero:
                _row["time"] = dynamic_cols[0]
                _row["value"] = 0
                _data.append(_row)
            # add _row if no dynamic cols
            elif not dynamic_cols:
                _data.append(_row)
        return _data
