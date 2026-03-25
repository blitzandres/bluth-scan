# BluthScan — Neural Bluetooth Topology Engine

Real-time Bluetooth scanner that visualizes discovered devices as a living 3D neural graph using [3d-force-graph](https://github.com/vasturiano/3d-force-graph).

## How it works

- Python backend scans for BLE devices using `bleak`
- New devices are pushed instantly via WebSocket (Flask-SocketIO)
- Frontend renders them as glowing 3D nodes connected to the central hub
- Node color = signal strength (green → cyan → orange → red)
- Particles flow along connection lines

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run (macOS requires Bluetooth permission for Terminal)
python app.py

# 3. Open browser
open http://localhost:5050
```

> **macOS note:** Go to System Settings → Privacy & Security → Bluetooth → allow Terminal (or your Python env).

## Stack

| Layer | Tech |
|-------|------|
| BT scanning | `bleak` (cross-platform BLE) |
| Backend | Flask + Flask-SocketIO + eventlet |
| 3D engine | `3d-force-graph` (Three.js / WebGL) |
| Transport | WebSocket |

## Next steps (coming)

- Click node → action menu (ping, fingerprint, probe)
- RSSI history timeline per device
- Export graph as JSON / PNG
- Filter by device name / signal strength
