from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 先定义基础的声明式基类
Base = declarative_base()


class DatabaseManager:
    def __init__(self, db_uri='sqlite:///my_database.db'):
        self.engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.engine)

        # 自动创建所有定义好的表（如果尚未创建）
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """获取一个新的会话实例"""
        return self.Session()

    def create_table(self, model_class):
        """手动创建单个表（可选，因为在初始化时已自动创建所有表）"""
        model_class.metadata.create_all(self.engine)
