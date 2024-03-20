import jwt
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

jwt_info = {"secret_key": "your-secret-key", "algorithm": "HS256"}

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


async def verify_jwt_token(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        payload = JwtAuth(**jwt_info).parse_access_token(token=token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        # 这里可以进一步验证用户是否有效，例如从数据库获取用户信息
        # user = await authenticate_user(username=username)
        # if not user:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        # 将用户名或其他需要的信息放入请求上下文中供后续使用
        request.state.user = {"username": username}
        return request
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


