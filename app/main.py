from typing import Any

import uvicorn
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from app.utils.jwt_auth import JwtAuth, verify_jwt_token
from app.endpoints import router
#
#
# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
#     access_token_expires = timedelta(seconds=5)
#     access_token = create_access_token(
#         data={"sub": user["username"]}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

app = FastAPI(title="Manager System", docs_url="/api_docs")
app.include_router(router)


async def jwt_authentication_middleware(request: Request, call_next):
    authorization_header = request.headers.get("Authorization")
    if authorization_header:
        token = authorization_header.split(" ")[1]  # 假设格式为 "Bearer <token>"
        try:
            await verify_jwt_token(request, token)
        except HTTPException as e:
            return JSONResponse(content={"detail": e.detail}, status_code=e.status_code)

    response = await call_next(request)
    return response

# @app.middleware('http')
# async def handle_exception(request: Request, call_next):
#     try:
#         response = await call_next(request)
#     except HTTPException as e:
#         return JSONResponse(content={"detail": e.detail}, status_code=e.status_code)
#
#     return response


# @app.middleware("http")
# async def handle_user_permission(request: Request, call_next):
#     print("request-path", request.url.path)
#     exclude_path = ["/test2", "/api_docs", "/", "/openapi.json"]
#     if request.url.path in exclude_path:
#         return await call_next(request)
#     if not request.headers.get("accept-language1", None):
#         return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={})
#
#     return await call_next(request)


@app.get("/test1")
async def read_root():
    return {"Hello": f"World! {1}"}


async def skip_user_permission(request: Request, call_next):
    return await call_next(request)


@app.get("/test2")
async def read_root1():
    return {"Hello": f"World! {1}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
