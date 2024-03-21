from app.db_core.db_connect import database_manager
from app.db_core.db_model import Permissions


async def list_permission(root_permission_id: int):
    session = database_manager.get_session()
    result, flag, root_id = [], True, root_permission_id
    while flag:
        query = session.query(Permissions).filter(Permissions.pm_id == root_id).first()
        if not query:
            break
        flag, root_id = (True, query.pm_group) if query.pm_group else (False, None)
    return result


def require_permission(permission_level: int):
    """
    装饰器仅用于标识路由所需的权限级别，无需实现权限检查逻辑，
    因为已经在全局中间件中处理。
    """
    def decorator(func):
        func.permission_required = permission_level
        return func
    return decorator
