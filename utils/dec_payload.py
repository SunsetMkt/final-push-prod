#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from cryptography.fernet import Fernet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
)

key = None

if os.path.exists("payload.key"):
    logging.info("Using existing key")
    with open("payload.key", "rb") as key_file:
        key = key_file.read()
else:
    logging.error("No key found")
    exit(1)

f = Fernet(key)

logging.info("Decrypting payload")

with open("payload.enc", "rb") as payload_file:
    payload = payload_file.read()

token = f.decrypt(payload)

with open("payload.md", "wb") as token_file:
    token_file.write(token)

logging.info("Done")
