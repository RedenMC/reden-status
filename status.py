import os
import time

import requests
import json

if __name__ == "__main__":
    if not os.path.exists("data"):
        os.mkdir("data")
    time_now = int(time.time() * 1000)
    if os.path.exists("data/status.json"):
        status = json.load(open("data/status.json"))
        status = {k: v for k, v in status.items() if time_now - v["timestamp"] < 7 * 24 * 60 * 60 * 1000}
    else:
        status = {}
    yymmddhhmm = time.strftime("%Y-%m-%dT%H:%M", time.localtime(time.time()))
    res = None
    e = None
    ex = None
    status_code = -1
    for i in range(5):
        try:
            res = requests.get("https://redenmc.com/api/status")
            status_code = res.status_code
            res = res.json()
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
        print("Network failure.", ex)
        exit(1)
    else:
        status[yymmddhhmm] = {
            "timestamp": time_now,
            "status": status_code,
            "online_count": res["online"]
        }
        json.dump(status, open("data/status.json", "w"))
        print("Status updated. Time: " + yymmddhhmm + " Status: " + str(status_code) + " Online: "
              + str(res.json()["online"]) + " players.")
