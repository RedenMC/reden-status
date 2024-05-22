import os
import time

import requests
import json

if __name__ == "__main__":
    if not os.path.exists("data"):
        os.mkdir("data")
    if os.path.exists("data/status.json"):
        status = json.load(open("data/status.json"))
    else:
        status = {}
    time_now = int(time.time() * 1000)
    yymmddhhmm = time.strftime("%Y-%m-%dT%H:%M", time.localtime(time.time()))
    res = None
    e = None
    for i in range(5):
        try:
            res = requests.get("https://redenmc.com/api/status")
            break
        except Exception as e:
            ex = e
    if res is None:
        status[yymmddhhmm] = {
            "timestamp": time_now,
            "status": 0,
            "online_count": -1
        }
        json.dump(status, open("data/status.json", "w"))
        print("Network failure.", e)
        exit(1)
    else:
        status[yymmddhhmm] = {
            "timestamp": time_now,
            "status": res.status_code,
            "online_count": res.json()["online"]
        }
        json.dump(status, open("data/status.json", "w"))
        print("Status updated. Time: " + yymmddhhmm + " Status: " + str(res.status_code) + " Online: "
              + str(res.json()["online"]) + " players.")
