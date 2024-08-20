import os


HOSTNAME = "10.7.71.112"
PORT = "3306"
USERNAME = "xx"
PASSWORD = "xx"
DATABASE = "sqlalchemy"

# 创建数据库引擎
_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=USERNAME, password=PASSWORD, host=HOSTNAME, port=PORT, db=DATABASE
)

# 依据数据库自动生成 table_struct
os.system(f"sqlacodegen {_url} > table_struct_pro.py")

# 当数据库表格没有主键的时候，自动生成的model 会生成一个Table，而不是一个类
# 可以把所有列都当做主键，建立联合主键，在 __table_args__ 里面加上 PrimaryKeyConstraint
#  __table_args__ = (
#         PrimaryKeyConstraint(column1, column2),
#         {},
#     )
# like this
# """
# t_role_data = Table(
#     "role_data",
#     metadata,
#     Column("role_id", VARCHAR(64), nullable=False, comment="角色id"),
#     Column("branch_code", VARCHAR(32), nullable=False, comment="所属部门code"),
#     Column("data_type", VARCHAR(16), comment="FACTORY 工厂"),
#     comment="角色对应数据权限",
# )
# """
