import os
import time

import requests
import json

if __name__ == "__main__":
    res = requests.get("https://redenmc.com/api/status")
    if not os.path.exists("data"):
        os.mkdir("data")
    if os.path.exists("data/status.json"):
        status = json.load(open("data/status.json"))
    else:
        status = {}
    time_now = int(time.time() * 1000)
    yymmddhhmm = time.strftime("%Y-%m-%dT%H:%M", time.localtime(time.time()))
    status[yymmddhhmm] = {
        "timestamp": time_now,
        "status": res.status_code,
        "online_count": res.json()["online"]
    }
    json.dump(status, open("data/status.json", "w"))
    print("Status updated. Time: " + yymmddhhmm + " Status: " + str(res.status_code) + " Online: "
          + str(res.json()["online"]) + " players.")

