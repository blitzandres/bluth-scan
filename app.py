from flask import Flask
from flask_socketio import SocketIO
from scanner import BluetoothScanner

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "bluth-scan-secret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

scanner = None


def device_found(device):
    print(f"[+] Found: {device['name']} | {device['address']} | RSSI: {device['rssi']}")
    socketio.emit("device", device)


@app.route("/")
def index():
    with open("static/index.html") as f:
        return f.read()


@socketio.on("connect")
def on_connect():
    global scanner
    print("[WS] Client connected")
    if scanner is None:
        scanner = BluetoothScanner(on_device_found=device_found)
        scanner.start()
        print("[*] Bluetooth scan started")


@socketio.on("disconnect")
def on_disconnect():
    print("[WS] Client disconnected")


if __name__ == "__main__":
    print("[*] BluthScan starting at http://localhost:5050")
    socketio.run(app, host="0.0.0.0", port=5050, debug=False)
