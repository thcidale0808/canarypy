#!/usr/bin/env python
import logging
import os

import uvicorn


def run():
    local = True
    port = int(os.getenv("PORT", "8080"))
    log_level = os.getenv("LOG_LEVEL", "info")
    logging.basicConfig(level=log_level.upper())
    logging.debug(f"Local run:\t{local}")

    uvicorn.run(
        "canarypy.api.main:app",
        host="0.0.0.0",
        port=port,
        reload=local,
        log_level=log_level,
        debug=True,
    )


if __name__ == "__main__":
    run()
