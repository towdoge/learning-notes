# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, Integer, String, Table
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True, comment='key')
    username = Column(String(255), comment='username')
    password = Column(String(255), comment='password')


class ConfigMergeProductDemand(Base):
    __tablename__ = 'config_merge_product_demand'
    __table_args__ = {'comment': '1.9合并需求生产'}

    id = Column(VARCHAR(64), primary_key=True, comment='主键id')
    factory_name = Column(VARCHAR(20), comment='工厂')
    pack = Column(VARCHAR(20), comment='pack')
    product_name = Column(VARCHAR(128), comment='电芯PN')
    old_month = Column(VARCHAR(20), comment='原需求月份')
    merge_month = Column(VARCHAR(20), comment='合并后月份')
    merge_quantity = Column(DECIMAL(12, 6), comment='合并数量')
    merge_remark = Column(VARCHAR(100), comment='合并原因')
    creator = Column(VARCHAR(64), comment='创建者')
    creator_name = Column(VARCHAR(64), comment='创建者姓名')
    create_time = Column(DateTime, comment='创建时间')
    modifier = Column(VARCHAR(64), comment='编辑者')
    modifier_name = Column(VARCHAR(64), comment='编辑者姓名')
    modify_time = Column(DateTime, comment='编辑时间')
    valid = Column(VARCHAR(10), comment='是否有效（YES有效，NO无效）')
    version_id = Column(VARCHAR(64), comment='数据版本id')
    analysis_id = Column(VARCHAR(64), comment='优化记录id')


t_test_table = Table(
    'test_table', metadata,
    Column('column1', String(255)),
    Column('column2', String(255))
)
