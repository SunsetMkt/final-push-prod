#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time
from datetime import datetime, timezone

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
)


GITHUB_EVENTS_API = "https://api.github.com/users/{username}/events/public"

# Safety limits for GitHub Actions
MAX_RATE_LIMIT_WAIT = 600  # seconds
MAX_RETRIES = 3


def _sleep_until(reset_timestamp):
    now = time.time()
    wait = int(reset_timestamp - now) + 1
    if wait <= 0:
        return
    if wait > MAX_RATE_LIMIT_WAIT:
        msg = (
            f"Rate limit reset in {wait}s, exceeding max wait ({MAX_RATE_LIMIT_WAIT}s)"
        )
        logging.error(msg)
        raise RuntimeError(msg)
    logging.info(f"Rate limited, waiting {wait}s")
    time.sleep(wait)


def get_recent_activities(username, session=None, handle_404=True):
    """
    Fetch recent public GitHub activities for a user.
    Returns a list (possibly empty).

    This API only returns events from the last 90 days.
    """
    logging.info(f"Fetching recent activities for {username}")
    url = GITHUB_EVENTS_API.format(username=username)
    sess = session or requests.Session()

    retries = 0
    while True:
        resp = sess.get(
            url,
            headers={"Accept": "application/vnd.github+json"},
            timeout=30,
        )

        if handle_404:
            # User not found == factual empty activity
            if resp.status_code == 404:
                logging.warning(f"GitHub user not found: {username}")
                return []

        # Rate limit handling
        if resp.status_code in (403, 429):
            reset = resp.headers.get("X-RateLimit-Reset")
            remaining = resp.headers.get("X-RateLimit-Remaining")

            if reset and remaining == "0":
                retries += 1
                if retries > MAX_RETRIES:
                    raise RuntimeError("Exceeded max retries due to rate limiting")

                _sleep_until(int(reset))
                continue

        # Other failures
        resp.raise_for_status()

        return resp.json()


def get_last_activity_time(activities):
    """
    Given a list of GitHub activities, return the most recent activity time
    as a timezone-aware UTC datetime, or None if empty.

    None == more than 90 days
    """
    if not activities:
        return None

    times = []
    for a in activities:
        ts = a.get("created_at")
        if not ts:
            continue
        times.append(
            datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        )

    return max(times) if times else None


def fetch_last_activity(username, handle_404=True):
    """
    High-level helper.
    Returns last activity time (UTC datetime) or None.

    None == more than 90 days
    """
    activities = get_recent_activities(username, handle_404=handle_404)
    return get_last_activity_time(activities)


def get_days_since_last_activity(last_activity):
    if not last_activity:
        return None
    return (datetime.now(tz=timezone.utc) - last_activity).days


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    args = parser.parse_args()

    last_activity = fetch_last_activity(args.username)
    logging.info(last_activity)
    logging.info(get_days_since_last_activity(last_activity))
