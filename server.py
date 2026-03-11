import os
import subprocess
from flask import Flask, render_template, jsonify
import psutil
from functions import get_temp, tapo_on, tapo_off, is_raspberry_pi
import asyncio

#create app
app = Flask(__name__)

#server info and check if running on raspberry pi
print("\033[92mStarting server...\033[0m")
if is_raspberry_pi: print("\033[93m🍓 Running on Raspberry Pi\033[0m")
else: print("\033[94m💻 Not running on Raspberry Pi\033[0m")

#routes
@app.route("/")
def home():
    data = {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk1": psutil.disk_usage('/'),
        "disk2": None,
        "temp": get_temp()
    }

    try:
        data["disk2"] = psutil.disk_usage('/media/mary/1ED2-42BD')
    except FileNotFoundError:
        data["disk2"] = "nic"
    return render_template("index.html", data=data, is_raspberry_pi=is_raspberry_pi)

@app.route("/led/on")
def led_on():
    asyncio.run(tapo_on())
    return jsonify({"status": "LED zapnuta!"})

@app.route("/led/off")
def led_off():
    asyncio.run(tapo_off())
    return jsonify({"status": "LED vypnuta!"})

#run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)