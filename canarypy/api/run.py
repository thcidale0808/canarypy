#!/usr/bin/env python
import logging
import os

import uvicorn


def run():
    port = int(os.getenv("CANARYPY_PORT", "8080"))
    reload = os.getenv("CANARYPY_RELOAD", "false").lower() == "true"
    log_level = os.getenv("CANARYPY_LOG_LEVEL", logging.INFO)
    debug = os.getenv("CANARYPY_DEBUG", "false").lower() == "true"
    uvicorn.run(
        "canarypy.api.main:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        log_level=log_level,
        debug=debug,
    )
