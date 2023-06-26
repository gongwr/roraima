import os
import sys

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles

static_dir = os.path.dirname(os.path.abspath(__file__))

possible_topdir = os.path.normpath(os.path.join(os.path.abspath(__file__),
                                                os.pardir, os.pardir, os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'roraima', '__init__.py')):
    sys.path.insert(0, possible_topdir)

static_dir = os.path.join(possible_topdir, 'static')


def create_app():
    app = FastAPI(title="Roraima API Server",
                  openapi_url="/api/v1/openapi.json",
                  docs_url=None, redoc_url=None)
    app.mount('/static', StaticFiles(directory=static_dir), name='static')

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/hello/{name}")
    async def say_hello(name: str):
        return {"message": f"Hello {name}"}

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="/static/redoc/bundles/redoc.standalone.js",
        )

    return app


app_ = create_app()


def main():
    import uvicorn
    uvicorn.run("roraima.cmd.api:app_", reload=True)


if __name__ == "__main__":
    main()
