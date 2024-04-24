# coding=utf-8
from __future__ import unicode_literals, absolute_import
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine, Column, String, Integer, DateTime
import pandas as pd
from table_struct import *
from sql_reading import *

ModelBase = declarative_base()  # <-基类


# name（字符串）：指定列字段的名称。
# type_（SQLAlchemy的数据类型）：指定列的数据类型，例如Integer、String、DateTime等。
# primary_key（布尔值）：指定列是否为主键。
# nullable（布尔值）：指定列是否允许为空。
# default：指定列的默认值。
# onupdate：指定在更新行时自动应用的值。
# server_default：指定在服务器端创建行时自动应用的默认值。
# index（布尔值）：指定是否为该列创建索引。
# unique（布尔值）：指定是否为该列创建唯一约束。
# autoincrement（布尔值）：指定是否自动递增。


HOSTNAME = "10.7.71.112"
PORT = "3306"
DATABASE = "sqlalchemy"
USERNAME = "atl-aps"
PASSWORD = "atl-aps"

# 创建数据库引擎
_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=USERNAME, password=PASSWORD, host=HOSTNAME, port=PORT, db=DATABASE
)
engine = create_engine(_url)


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# # 创建会话工厂
# Session = sessionmaker(bind=engine)
# # 创建会话
# session = Session()
with get_session() as session:

    try:
        #
        # # 添加数据
        user1 = AuthUser(username="Alic1e", password=25)
        # user2 = AuthUser(username='Bob1', password=30)
        query = session.query(AuthUser).get(user1.username)
        session.merge(user1)
        # session.add(user2)
        session.commit()

        # TmpObj = OptServiceParameter

        # if 'result_daily_newly_purchased_tool_cost' not in inspect(engine).get_table_names():
        #     TmpObj.__table__.create(engine)

        # query = session.query(TmpObj).with_entities(TmpObj)
        #
        # obj_df = pd.read_sql(query.statement, session.bind)
        # tmp = obj_df['algorithm_params'].values[1]
        # result = session.query(AuthUser).with_entities(AuthUser.username).filter(AuthUser.username == 'Alic1e')
        # a = pd.read_sql(result.statement, session.bind)
        # print(result)
        # print(a)
        # # result1 = session.query(TestTable).filter(TestTable.column1 =='1')
        # # b= pd.read_sql(result1.statement, session.bind)
        # # print(result1)
        # # print(b)
        # cols = ['factory_name', 'pack', 'product_name', 'old_month', 'merge_month',
        #         'merge_quantity']
        # User = aliased(ConfigMergeProductDemand)
        # # result2 = session.query(User).with_entities(*[getattr(User, i) for i in cols]).filter(User.version_id == '9c8c27fa-0228-4ed8-9b95-5004808be58d')
        # result2 = session.query(User).filter(User.version_id.in_(['9c8c27fa-0228-4ed8-9b95-5004808be58d']))
        # c = pd.read_sql(result2.statement, session.bind)
        # print(result2)
        # print(c)
        print("ttt")
    except Exception as e:
        session.rollback()  # 回滚事务
        print(f"An error occurred: {str(e)}")
    finally:
        session.close()

#
# # 查询数据
# users = session.query(AuthUser).all()
# for user in users:
#     print(user)
#
# # 更新数据
# user1.password = 26
# session.commit()
#
# # 删除数据
# session.delete(user2)
# session.commit()
#
# # 关闭会话
# session.close()


# MySQL-Python
#     mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
# pymysql
#     mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
# MySQL-Connector
#     mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
# cx_Oracle
#     oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]

# merge(obj, load=True, **kw)：将给定对象合并到会话中。如果对象已经存在于会话中，则返回会话中的对象。
# expunge(obj)：从会话中移除给定对象。
# flush(objects=None)：刷新会话中的挂起更改到数据库。
# rollback()：回滚当前会话中的所有挂起更改。
# commit()：提交当前会话中的所有挂起更改到数据库。
# execute(statement, params=None, bind=None, **kw)：执行给定的SQL语句。
# scalar(statement, params=None, bind=None, **kw)：执行给定的SQL语句，并返回第一行的第一个列值。
# get_bind(mapper=None, clause=None)：返回用于执行给定映射器或子句的绑定引擎。
# refresh(obj, attribute_names=None, lockmode=None)：刷新给定对象的属性值，从数据库中重新加载。
# expire(obj, attribute_names=None)：将给定对象的属性标记为过期，下次访问时将从数据库中重新加载。
# expunge_all()：从会话中移除所有对象。
# query_property()：返回与会话关联的查询属性。
# bulk_save_objects(objects, return_defaults=False)：批量保存给定的对象列表。
# bulk_insert_mappings(mapper, mappings, return_defaults=False)：批量插入给定的映射列表。
# bulk_update_mappings(mapper, mappings)：批量更新给定的映射列表。

# # 等于
# query.filter(User.name == 'ed')
#
# # 不等于
# query.filter(User.name != 'ed')
#
# # like和ilike
# query.filter(User.name.like('%ed%'))
# query.filter(User.name.ilike('%ed%')) # 不区分大小写
#
# # in
# query.filter(User.name.in_(['ed', 'wendy', 'jack']))
# query.filter(User.name.in_(
#     session.query(User.name).filter(User.name.like('%ed%'))
# ))
# # not in
# query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
#
# # is
# query.filter(User.name == None)
# query.filter(User.name.is_(None))
#
# # is not
# query.filter(User.name != None)
# query.filter(User.name.is_not(None))
#
# # and
# from sqlalchemy import and_
# query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
# query.filter(User.name == 'ed', User.fullname == 'Ed Jones')
# query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')
#
# # or
# from sqlalchemy import or_
# query.filter(or_(User.name == 'ed', User.name == 'wendy'))
#
# # match
# query.filter(User.name.match('wendy'))
