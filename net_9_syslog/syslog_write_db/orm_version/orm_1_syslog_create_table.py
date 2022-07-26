from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime

tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))  # 设置时区为东八区

engine = create_engine('sqlite:///sqlalchemy_syslog_sqlite3.db?check_same_thread=False',
                       # echo=True
                       )

Base = declarative_base()


class Syslog(Base):
    __tablename__ = 'syslog'

    id = Column(Integer, primary_key=True)
    device_ip = Column(String(64), nullable=False)
    facility = Column(Integer, nullable=False)
    facility_name = Column(String(64), nullable=False)
    severity_level = Column(Integer, nullable=False)
    severity_level_name = Column(String(64), nullable=False)
    logid = Column(Integer, nullable=False)
    log_source = Column(String(64), nullable=False)
    description = Column(String(128), nullable=False)
    text = Column(String(1024), nullable=False)
    time = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.device_ip} " \
               f"| Datetime: {self.time} " \
               f"| Severity Name: {self.severity_level_name})" 


if __name__ == '__main__':
    # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
    Base.metadata.create_all(engine, checkfirst=True)
