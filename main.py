#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys
from datetime import datetime, timezone

import app_crypto
import app_data
import gh_api

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
)


def get_current_time():
    return datetime.now(tz=timezone.utc).replace(tzinfo=timezone.utc)


if __name__ == "__main__":
    logging.info("Starting")

    # Get key to test environment
    app_crypto.get_key()

    logging.info("Getting activity")

    config = app_data.get_config()
    state = app_data.get_state()

    last_activity = gh_api.fetch_last_activity(config["username"])
    days_since_last_activity = gh_api.get_days_since_last_activity(last_activity)

    state["last_check"] = get_current_time().isoformat()

    if last_activity:
        state["last_activity"] = last_activity.isoformat()
        state["inactivity_days"] = days_since_last_activity
    else:
        # None == more than 90 days
        state["last_activity"] = None
        state["inactivity_days"] = 91
        days_since_last_activity = 91

    app_data.save_state(state)

    logging.info("Determining if inactive")

    if days_since_last_activity > config["inactivity_days"]:
        logging.warning("Inactive, triggering")
        # Should trigger
        if config["one_shot"] and state["triggered"]:
            logging.info("Already triggered, skipping")
            sys.exit(0)

        payload = app_data.get_bytes(config["payload_path"])
        key = app_crypto.get_key()
        token = app_crypto.decrypt(payload, key)
        app_data.save_bytes(config["output_path"], token)
        state["triggered"] = True
        state["triggered_at"] = get_current_time().isoformat()
        app_data.save_state(state)
    else:
        logging.info("Not inactive, safe to exit")

    logging.info("Done")
