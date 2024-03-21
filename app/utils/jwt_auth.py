import hashlib
import os

import jwt
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.config import jwt_info
from app.db_core.db_connect import database_manager
from app.db_core.db_model import Users
from app.utils.permission import list_permission

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class JwtAuth:
    def __init__(self, secret_key: str, algorithm: str = "HS2256", expires_delta: timedelta = timedelta(hours=12)):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_delta = expires_delta
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expires_delta = expires_delta if expires_delta else self.expires_delta
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def parse_access_token(self, token: str) -> dict:
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        return payload

#
# def verify_jwt_token(token: str = Depends(oauth2_scheme)):
#     print("token-->", token)
#     return
#
# async def authenticate_user(username: str, password: str):
#     # 此处为模拟用户数据库，实际应用中从数据库查询用户信息并验证密码
#     fake_users_db = {
#         "user1": {"username": "user1", "hashed_password": get_password_hash("password1")},
#         "user2": {"username": "user2", "hashed_password": get_password_hash("password2")},
#     }
#     user = fake_users_db.get(username)
#     if not user:
#         return False
#     if not verify_password(password, user.get("hashed_password")):
#         return False
#     return user
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = JwtAuth(**jwt_info).parse_access_token(token=token)
#         user: str = payload.get("user_id")
#         if user is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
#         user = await authenticate_user(username=username, password='password1')
#         if user is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#         return user
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


async def verify_jwt_token(request: Request, token: str = Depends(oauth2_scheme), permission_id: int = None):
    try:
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        token: str = token[7:]
        payload = JwtAuth(**jwt_info).parse_access_token(token=token)
        user_id: str = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        db_session = database_manager.get_session()
        user = db_session.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        if permission_id:
            permission_ids = await list_permission(permission_id)
            if not all([i in user.permission.split(',') for i in permission_ids]):
                raise HTTPException(status_code=status.HTTP_403, detail="Permission Not Allowed")
        request.state.user = {"user_id": user_id}
        return request
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


async def password_hashing(password: str, salt: str = None) -> tuple:
    """
    Asynchronous function that hashes a given password with a salt for improved security.

    Parameters:
    password (str): The original password string to be hashed.
    salt (str, optional): A hexadecimal representation of a 16-byte salt value. If not provided,
    a random salt will be generated using os.urandom() and converted to its hexadecimal form.

    Returns:
    tuple: A tuple containing two elements. The first element is the hexadecimal representation of the salt value.
    The second element is the hash value computed by applying the SHA-256 algorithm to the concatenation of
    the salt (as bytes) and the encoded password, which helps mitigate rainbow table attacks.

    Note:
    This function utilizes a salted hashing technique to enhance password security.
    """

    # Generate a random salt if none is provided

    salt_bytes = os.urandom(16) if not salt else bytes.fromhex(salt)
    assert len(salt_bytes) == 16, "Salt must represent a 16-byte value when encoded in hexadecimal"

    # Compute the hash value of the concatenated salt (as bytes) and encoded password using the SHA-256 algorithm
    hash_value = hashlib.sha256(salt_bytes + password.encode()).hexdigest()
    return salt_bytes.hex(), hash_value
