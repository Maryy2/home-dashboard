from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)

@app.route("/")
def home():
    data = {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)