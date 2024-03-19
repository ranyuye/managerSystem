from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from db_model import Base, Users


class DatabaseManager:
    def __init__(self, db_url='sqlite:///my_database.db'):
        self.engine = create_engine(db_url)
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

# 创建一个新的 User 实例并设置属性值
new_user = Users(
    name="Example User",
    email="user@example.com",
    role=1,
    team=None,  # 如果允许为空，则传入 None；否则，请提供一个有效的整数值
    pw_hash="...",
    pw_salt="...",
    permission="1"  # 根据你的模型类定义，这个字段已经是可选的，因为有默认值 "1"
)

# 获取一个会话实例
session = database_manager.get_session()

try:
    session.add(new_user)
    session.commit()
except Exception as e:
    session.rollback()
    print(f"Error occurred: {e}")

finally:
    session.close()
