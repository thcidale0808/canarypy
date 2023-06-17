from fastapi import FastAPI

from canarypy.api import __version__
from canarypy.api.routes import product, release, signal

TITLE = "CanaryPy API"
OPENAPI_URL = "/openapi.json"
FAVICON_URL = "/static/favicon.png"
DESCRIPTION = "'This the API for CanaryPy."


tags_metadata = [
    {
        "name": "canarypy",
        "description": "CanaryPy Rest API.",
    }
]

app = FastAPI(
    title=TITLE,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    description=DESCRIPTION,
    version=__version__,
    openapi_tags=tags_metadata,
)

app.include_router(product.router)
app.include_router(release.router)
app.include_router(signal.router)
