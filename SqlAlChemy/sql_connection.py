from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from urllib.parse import quote_plus as urlquote


class SqlConnection:
    def __init__(self):
        self.host = "10.7.71.112"
        self.port = 3306
        self.user_name = "xx"
        self.password = "xx"
        self.database = "sqlalchemy"
        self.charset = "utf8"

        self.init_sql_info()
        self.engine = self.create_engine()

    def init_sql_info(self):
        pass

    def create_engine(self):
        _url = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(
            self.user_name,
            urlquote(self.password),
            self.host,
            self.port,
            self.database,
            self.charset,
        )
        try:
            engine = create_engine(_url)
            return engine
        except:
            return None

    def create_session(self):
        session = sessionmaker(bind=self.engine)
        return session()
