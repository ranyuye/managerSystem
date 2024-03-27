import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from app.utils.jwt_auth import verify_jwt_token
from app.endpoints import router


app = FastAPI(title="Manager System", docs_url="/api_docs")
app.include_router(router)
#
#
# @app.middleware("http")
# async def handle_user_permission(request: Request, call_next):
#     print("request-path", request.url.path)
#     exclude_path = ["/test2", "/api_docs", "/", "/openapi.json", "/auth/login"]
#     if request.url.path in exclude_path:
#         return await call_next(request)
#     auth_token = request.headers.get("Authorization", None)
#     if not auth_token:
#         return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"code": 401, "detail": "UNAUTHORIZED"})
#     permission_required = getattr(request.scope.get("endpoint"), "permission_required", None)
#     try:
#         request = await verify_jwt_token(request, token=auth_token, permission_id=permission_required)
#     except HTTPException as e:
#         return JSONResponse(status_code=e.status_code, content={"code": e.status_code, "detail": e.detail})
#     return await call_next(request)


@app.get("/test1")
async def read_root():
    return {"Hello": f"World! {1}"}


@app.get("/test2")
async def read_root1():
    return {"Hello": f"World! {1}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
