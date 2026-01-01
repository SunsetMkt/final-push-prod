#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import app_crypto
import app_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
)


if __name__ == "__main__":
    logging.info("Starting")
    config = app_data.get_config()
    payload = app_data.get_bytes(config["payload_path"])
    hash = app_crypto.get_sha256_bytes(
        app_crypto.decrypt(payload, app_crypto.get_key())
    )
    logging.info(f"Hash: {hash}")
    logging.info("Done")
