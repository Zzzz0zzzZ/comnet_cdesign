import json

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from routers.user import router as user_router
from tortoise.contrib.fastapi import register_tortoise

with open("./configs/config.txt", "r") as f:
    config = json.loads(f.read())

app = FastAPI()

# 处理跨域
# 配置允许域名
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

# 处理跨域
# 配置允许域名列表、允许方法、请求头、cookie等
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user")

# 注册数据库连接
register_tortoise(
    app,
    db_url=config["db_url"],
    modules={"models": ["models.user"]},
    # generate_schemas=True
)


# 重定向到接口文档页面
@app.get("/")
async def main_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    # local
    uvicorn.run(app, port=8889, log_config="./configs/uvicorn_config.json", debug=True)
    # online
    # uvicorn.run(app, host='0.0.0.0', port=7957, log_config="./configs/uvicorn_config.json", debug=True)
