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
    try:
        res = requests.get("https://redenmc.com/api/status")
        status[yymmddhhmm] = {
            "timestamp": time_now,
            "status": res.status_code,
            "online_count": res.json()["online"]
        }
        json.dump(status, open("data/status.json", "w"))
        print("Status updated. Time: " + yymmddhhmm + " Status: " + str(res.status_code) + " Online: "
              + str(res.json()["online"]) + " players.")
    except Exception as e:
        status[yymmddhhmm] = {
            "timestamp": time_now,
            "status": 0,
            "online_count": -1
        }
        json.dump(status, open("data/status.json", "w"))
        print("Network failure.", e)
    
