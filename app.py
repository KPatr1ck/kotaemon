import os

from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware  # 引入 CORS 中间件
from theflow.settings import settings as flowsettings

load_dotenv()

KH_APP_DATA_DIR = getattr(flowsettings, "KH_APP_DATA_DIR", ".")
GRADIO_TEMP_DIR = os.getenv("GRADIO_TEMP_DIR", None)
# override GRADIO_TEMP_DIR if it's not set
if GRADIO_TEMP_DIR is None:
    GRADIO_TEMP_DIR = os.path.join(KH_APP_DATA_DIR, "gradio_tmp")
    os.environ["GRADIO_TEMP_DIR"] = GRADIO_TEMP_DIR

from ktem.main import App  # noqa

app = App()
demo = app.make()

# 获取 FastAPI 实例并添加 CORS 中间件
fastapi_app = demo.app  # 访问 Gradio 底层的 FastAPI 应用实例

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # 允许所有来源的跨域请求，或指定特定域名 ['https://example.com']
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法（GET, POST 等）
    allow_headers=["*"],  # 允许所有请求头
)

demo.queue().launch(
    favicon_path=app._favicon,
    inbrowser=False,
    server_name="0.0.0.0",
    server_port=9001,
    allowed_paths=[
        "libs/ktem/ktem/assets",
        GRADIO_TEMP_DIR,
    ],
)
