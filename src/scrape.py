from datetime import datetime, timedelta
import logging
import requests
import json
import backoff
import time

# env vars
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
DATA_PATH = os.getenv("DATA_PATH")

logging.basicConfig(level=logging.INFO)
logging.getLogger("backoff").addHandler(logging.StreamHandler())


@backoff.on_exception(backoff.expo, requests.exceptions.Timeout, max_time=600)
@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_time=300,
    jitter=backoff.full_jitter,
)
def get_url(url, params={}):
    res = requests.get(url, params)
    if res.status_code in [429] or res.status_code >= 500:
        res.raise_for_status()
    return res


def process_result(res, outfile):
    json_response = res.json()
    print("records retreived:", len(json_response["data"]), flush=True)
    with open(outfile, "a+") as file:
        for data in json_response["data"]:
            json.dump(data, file)
            file.write("\n")


def iterate_subreddit(subreddit, datestart, dateend, days_delta=1):
    while datestart < dateend:
        print(datestart, datestart + timedelta(days=days_delta), flush=True)
        after_ts = int(datestart.timestamp())
        before_ts = int((datestart + timedelta(days=days_delta)).timestamp())
        res = get_url(
            "https://api.pushshift.io/reddit/search/submission/",
            params={
                "subreddit": subreddit,
                "sort": "desc",
                "sort_type": "created_utc",
                "after": after_ts,
                "before": before_ts,
                "size": 2000,
            },
        )
        process_result(res, outfile=f"{DATA_PATH}/{subreddit}.txt")
        datestart += timedelta(days=days_delta)
        time.sleep(2)
    print("done")


iterate_subreddit("nosleep", datetime(2010, 1, 1), datetime(2019, 11, 1))
