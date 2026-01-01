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
    logging.info("Generating key")
    key = Fernet.generate_key()
    # Save as payload.key
    # Put this somewhere safe!
    with open("payload.key", "wb") as key_file:
        key_file.write(key)

f = Fernet(key)

logging.info("Encrypting payload")

with open("payload.md", "rb") as payload_file:
    payload = payload_file.read()

token = f.encrypt(payload)

with open("payload.enc", "wb") as token_file:
    token_file.write(token)

logging.info("Done")
