from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'instagram'
USERNAME = 'root'
PASSWORD = 'qwe123'

db_url = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    DATABASE
)


engine = create_engine(db_url)
Base = declarative_base(engine)

Session = sessionmaker(engine)
session = Session()

# if __name__ == '__main__':
#     print(dir(Base))
#     print(dir(session))
