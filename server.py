import subprocess
from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)

def get_temp(): 
    temp = subprocess.check_output(["vcgencmd", "measure_temp"])
    temp = temp.decode()
    temp = temp.replace("temp=","").replace("'C\n","")
    return temp

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
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
