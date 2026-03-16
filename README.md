# Advanced RTDE Monitor - URCap for PolyScope X

A comprehensive URCap for real-time robot data monitoring and control using RTDE (Real-Time Data Exchange) protocol with WebSocket streaming.

## 🎯 Features

### Real-Time Data Monitoring
- **TCP Pose**: X, Y, Z, RX, RY, RZ coordinates
- **Tool Analog Inputs**: AI0 and AI1 monitoring with domain configuration (Voltage/Current)
- **Runtime State**: Robot execution state
- **Safety Status**: Safety system status
- **Digital I/O**: Monitor and control digital inputs/outputs

### Technical Highlights
- **WebSocket Streaming**: Real-time data updates at 125Hz RTDE frequency
- **Dual Architecture**: Python backend (FastAPI) + Angular frontend
- **Docker Container**: Isolated backend service with RTDE connection
- **Automatic Reconnection**: Robust error handling and connection recovery

## 📋 Requirements

- **SDK Version**: v0.20.19
- **PolyScope X**: Tested on v10.13
- **Robot Controller**: UR with RTDE support

## 🚀 Installation

### 1. Install Dependencies

```bash
npm install
```

### 2. Build the URCap

```bash
npm run build
```

This will:
- Build the Angular frontend
- Build the Python backend Docker image
- Package everything into a `.urcapx` file

### 3. Deploy to Robot

**For simulator or local development:**
```bash
npm run install-urcap
```

**For specific robot IP/port:**
```bash
npm run install-urcap-port 45000
```

Or manually install the generated `.urcapx` file from `target/` folder through PolyScope X interface.

## 📁 Project Structure

```
advanced-rtde/
├── advanced-rtde-backend/          # Python backend service
│   ├── src/
│   │   ├── main.py                 # FastAPI application with WebSocket
│   │   ├── connector.py            # RTDE connection handler
│   │   ├── rtdeIO.xml              # RTDE I/O configuration
│   │   └── utils.py                # Helper functions
│   ├── requirements.txt            # Python dependencies
│   └── Dockerfile                  # Backend container image
│
├── advanced-rtde-frontend/         # Angular frontend
│   ├── src/app/components/
│   │   └── rtde-communicator/
│   │       ├── rtde-communicator.component.ts
│   │       ├── rtde-communicator.component.html
│   │       ├── backend.service.ts  # WebSocket client service
│   │       └── rtde-communicator.node.ts
│   ├── package.json                # Frontend dependencies
│   └── tsconfig.json               # TypeScript configuration
│
├── package.json                    # Root package configuration
└── manifest.yaml                   # URCap metadata
```

## 🔧 Usage

### Starting Data Monitor

1. Open the URCap in PolyScope X
2. Navigate to the "Rtde Communicator" page
3. Click **"Start Monitoring"** button
4. Real-time data will be displayed:
   - Runtime State
   - Safety Status
   - TCP Pose (X, Y, Z, RX, RY, RZ)
   - Tool Analog Inputs (AI0, AI1)

### Digital Output Control

1. Select a digital output from the dropdown (DO 0-7)
2. Click **"Set High[1]"** or **"Set Low[0]"** to change the output state

### Stopping Monitor

Click **"Stop Monitoring"** to disconnect the WebSocket and stop data streaming.

## 🛠️ Development

### Backend Development

The backend uses:
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server with WebSocket support
- **RTDE Protocol**: Direct communication with robot controller

```bash
cd advanced-rtde-backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 52761
```

### Frontend Development

The frontend uses:
- **Angular 21**: Modern web framework
- **URCap SDK v0.20.19**: UR's contribution API
- **RxJS**: Reactive data streams

```bash
cd advanced-rtde-frontend
npm install
npm start
```

### RTDE Configuration

Edit `advanced-rtde-backend/src/rtdeIO.xml` to add/remove RTDE signals:

```xml
<recipe key="state">
    <field name="actual_TCP_pose" type="VECTOR6D"/>
    <field name="tool_analog_input0" type="DOUBLE"/>
    <field name="tool_analog_input1" type="DOUBLE"/>
    <!-- Add more fields here -->
</recipe>
```

## 📊 Key Components

### Backend (Python)

**`main.py`**:
- WebSocket endpoint at `/ws`
- REST endpoints for random numbers and digital output control
- Connection manager for handling multiple WebSocket clients

**`connector.py`**:
- RTDE connection initialization and management
- Automatic reconnection on connection loss
- Data receiving and parsing

### Frontend (Angular)

**`rtde-communicator.component.ts`**:
- Component lifecycle management
- Direct subscription to WebSocket data streams
- Manual change detection for real-time updates

**`backend.service.ts`**:
- WebSocket client implementation
- Error handling and reconnection logic
- Observable streams for data distribution

## 🐛 Troubleshooting

### WebSocket Connection Issues

**Check container logs:**
```bash
docker logs -f <container_id>
```

Look for:
- `WebSocket client connected. Total connections: 1`
- `Sent 50 messages to 1 clients`

**Check browser console:**
- Should see "WebSocket connection opened successfully"
- Should see "Data updated: {...}" messages

### No Data Updates

1. Ensure robot controller is running (not in emergency stop)
2. Check RTDE service is available (port 30004)
3. Verify WebSocket connection is established
4. Check browser console for errors

### Build Errors

```bash
# Clean and rebuild
npm run clean-dist
npm run clean-target
npm install
npm run build
```

## 📝 Version History

### v1.0.0 (Current)
- ✅ SDK v0.20.19 support
- ✅ Angular 21 upgrade
- ✅ Tool Analog Input monitoring (AI0, AI1)
- ✅ WebSocket real-time streaming
- ✅ Improved error handling and connection management
- ✅ Manual change detection for reliable data updates
- ✅ Tested on PolyScope X v10.13

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

Apache-2.0

## 🔗 Links

- [PolyScope X SDK Documentation](https://docs.universal-robots.com/PolyScopeX_SDK_Documentation/)
- [RTDE Guide](https://www.universal-robots.com/articles/ur/interface-communication/real-time-data-exchange-rtde-guide/)
- [URCap Development](https://www.universal-robots.com/plus/software-platform/)

## 📧 Contact

For issues and questions, please open an issue on GitHub.

---

**Note**: This URCap requires PolyScope X v10.11.0 or later with RTDE support enabled.
