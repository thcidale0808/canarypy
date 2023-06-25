#!/usr/bin/env python
import logging
import os

import uvicorn


def run():
    port = int(os.getenv("CANARYPY_API_PORT", "8080"))
    reload = os.getenv("CANARYPY_API_RELOAD", "false").lower() == "true"
    log_level = os.getenv("CANARYPY_API_LOG_LEVEL", logging.INFO)
    debug = os.getenv("CANARYPY_API_DEBUG", "false").lower() == "true"
    host = os.getenv("CANARYPY_API_HOST", "0.0.0.0")
    uvicorn.run(
        "canarypy.api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
        debug=debug,
    )
