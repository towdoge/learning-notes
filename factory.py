import abc

class Base(metaclass=abc.ABCMeta):
    def __init__(self):
        self.host = ''
        self.port = 0

    @abc.abstractmethod
    def init_settings(self):
        return

    def connect(self):
        print(self.host)
        print(self.port)

class Dev(Base):
    def init_settings(self):
        self.host = '111'
        self.port = '111'

class Production(Base):
    def init_settings(self):
        self.host = '222'
        self.port = '222'


dev = Dev()
dev.init_settings()
dev.connect()