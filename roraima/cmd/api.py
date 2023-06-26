import os
import sys

import uvicorn

from oslo_config import cfg
from oslo_log import log as logging

from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles

from roraima.api.api_v1.api import api_router
from roraima.common import config

BASE_PATH = os.path.normpath(os.path.join(os.path.abspath(__file__),
                                          os.pardir, os.pardir, os.pardir))
if os.path.exists(os.path.join(BASE_PATH, 'roraima', '__init__.py')):
    sys.path.insert(0, BASE_PATH)

STATIC_PATH = os.path.join(BASE_PATH, 'static')

#CONF = cfg.CONF(default_config_files=[os.path.join(BASE_PATH, 'etc', 'roraima-api.conf')])
CONF = cfg.CONF
logging.register_options(CONF)


def create_roraima():
    config.parse_args()
    config.set_config_defaults()
    logging.setup(CONF, "roraima")
    root_router = APIRouter()
    app = FastAPI(title="Roraima API Server",
                  openapi_url="/api/v1/openapi.json",
                  docs_url=None, redoc_url=None)
    app.mount('/static', StaticFiles(directory=STATIC_PATH), name='static')

    @root_router.get("/")
    async def root():
        return {"message": "Hello World"}

    @root_router.get("/hello/{name}")
    async def say_hello(name: str):
        return {"message": f"Hello {name}"}

    @root_router.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="/static/redoc/bundles/redoc.standalone.js",
        )

    app.include_router(root_router)
    app.include_router(api_router, prefix="/api/v1")

    return app


app_ = create_roraima()


def main():
    uvicorn.run("roraima.cmd.api:app_", reload=True)


if __name__ == "__main__":
    main()
