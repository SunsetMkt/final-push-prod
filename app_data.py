#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
)

CONFIG_PATH = "config.json"
STATE_PATH = "state.json"

CONFIG_TEMPLATE = {
    "username": "TARGET_GITHUB_USERNAME",
    "inactivity_days": 60,
    "payload_path": "payload.enc",
    "output_path": "README.md",
    "one_shot": False,
    "handle_404": True,
}
STATE_TEMPLATE = {
    "last_activity": None,
    "inactivity_days": 0,
    "triggered": False,
    "triggered_at": None,
    "last_check": None,
}


def get_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def validate_state(state):
    required_fields = {
        "last_activity": (str, type(None)),
        "inactivity_days": int,
        "triggered": bool,
        "triggered_at": (str, type(None)),
        "last_check": (str, type(None)),
    }

    for key, expected_type in required_fields.items():
        if key not in state:
            raise KeyError(f"Missing state field: {key}")

        if not isinstance(state[key], expected_type):
            raise TypeError(
                f"State field '{key}' must be {expected_type.__name__}, "
                f"got {type(state[key]).__name__}"
            )

    return state


def get_state():
    try:
        state = get_json(STATE_PATH)
    except Exception as e:
        logging.warning(e)
        state = None
    logging.info(f"Loaded state: {state}")
    try:
        return validate_state(state)
    except (KeyError, TypeError) as e:
        # invalid state is acceptable
        logging.warning(e)
        logging.warning(f"Using default state: {STATE_TEMPLATE}")
        return copy.deepcopy(STATE_TEMPLATE)


def save_state(state):
    logging.info(f"Saving state: {state}")
    save_json(STATE_PATH, state)


def validate_config(config):
    required_fields = {
        "username": str,
        "inactivity_days": int,
        "payload_path": str,
        "output_path": str,
        "one_shot": bool,
        "handle_404": bool,
    }

    for key, expected_type in required_fields.items():
        if key not in config:
            raise KeyError(f"Missing config field: {key}")

        if not isinstance(config[key], expected_type):
            raise TypeError(
                f"Config field '{key}' must be {expected_type.__name__}, "
                f"got {type(config[key]).__name__}"
            )

    # inactivity_days should < 90 and >= 1
    if config["inactivity_days"] < 1 or config["inactivity_days"] > 90:
        raise ValueError(
            f"Config field 'inactivity_days' must be between 1 and 90, got {config['inactivity_days']}"
        )

    return config


def get_config():
    config = get_json(CONFIG_PATH)
    logging.info(f"Loaded config: {config}")
    # invalid config is not acceptable
    return validate_config(config)


def get_bytes(filename):
    with open(filename, "rb") as f:
        return f.read()


def save_bytes(filename, data):
    with open(filename, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    logging.info(get_config())
    logging.info(get_state())
