import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

app = FastAPI()

# 私钥，用于签名 JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# 加密上下文，用于处理密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 创建一个用于携带 JWT 的 Bearer token 类型
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=5)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    # 此处为模拟用户数据库，实际应用中从数据库查询用户信息并验证密码
    fake_users_db = {
        "user1": {"username": "user1", "hashed_password": get_password_hash("password1")},
        "user2": {"username": "user2", "hashed_password": get_password_hash("password2")},
    }
    user = fake_users_db.get(username)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.get("hashed_password")):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        user = await authenticate_user(username=username, password='password1')
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(seconds=5)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
async def read_root(current_user: dict = Depends(get_current_user)):
    return {"Hello": f"World, {current_user['username']}!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
