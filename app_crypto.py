#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import logging
import os

from cryptography.fernet import Fernet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
)


def str_to_bytes(payload):
    return payload.encode("utf-8")


def bytes_to_str(payload):
    return payload.decode("utf-8")


def get_sha256_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def get_key():
    key_env = os.getenv("PAYLOAD_KEY")
    if not key_env:
        msg = "No key found, please set PAYLOAD_KEY in Actions secrets"
        logging.error(msg)
        raise RuntimeError(msg)
    return str_to_bytes(key_env)


def decrypt(payload, key):
    """
    decrypt with fernet

    :param payload: bytes
    :param key: bytes
    """
    logging.info(f"Decrypting payload {get_sha256_bytes(payload)} with key")
    f = Fernet(key)
    token = f.decrypt(payload)
    return token


def encrypt(payload, key):
    """
    encrypt with fernet

    :param payload: bytes
    :param key: bytes
    """
    logging.info(f"Encrypting payload {get_sha256_bytes(payload)} with key")
    f = Fernet(key)
    token = f.encrypt(payload)
    return token
