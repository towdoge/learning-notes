import os

HOSTNAME = '10.7.71.112'
PORT = '3306'
DATABASE = 'sqlalchemy'
USERNAME = 'atl-aps'
PASSWORD = 'atl-aps'

# 创建数据库引擎
_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=USERNAME, password=PASSWORD, host=HOSTNAME, port=PORT, db=DATABASE)

# 自动生成 table_struct
os.system(f'sqlacodegen {_url} > table_struct.py')

# 当数据库表格没有主键的时候，自动生成的model 会生成一个Table，而不是一个类
"""
t_rbac_role_data = Table(
    "rbac_role_data",
    metadata,
    Column("role_id", VARCHAR(64), nullable=False, comment="角色id"),
    Column("branch_code", VARCHAR(32), nullable=False, comment="所属部门（组织）code"),
    Column("data_type", VARCHAR(16), comment="FACTORY 工厂"),
    comment="RBAC-角色对应数据权限",
)
"""