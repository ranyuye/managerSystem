from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from app.db_core.db_model import Base, Users


class DatabaseManager:
    def __init__(self):
        self.db_url = Path(__file__).parent.parent / 'db_core' / 'my_database.db'
        self.engine = create_engine(f"sqlite:///{str(self.db_url)}")
        self.Session = sessionmaker(bind=self.engine)

        # 自动创建所有定义好的表（如果尚未创建）
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """获取一个新的会话实例"""
        return self.Session()

    def create_table(self, model_class):
        """手动创建单个表（可选，因为在初始化时已自动创建所有表）"""
        model_class.metadata.create_all(self.engine)


database_manager = DatabaseManager()


def get_db_session():
    """
    获取与数据库的会话(Session)对象。

    返回:
        Session: SQLAlchemy ORM Session对象，可用于执行数据库操作。
    """
    db_session = database_manager.get_session()
    try:
        yield db_session  # 使用生成器实现上下文管理协议，配合with语句使用

        # 在with块的末尾自动提交事务
        try:
            db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            raise e
    finally:
        db_session.close()  # 在finally块中确保会话关闭以释放资源


SessionLocal = get_db_session()
