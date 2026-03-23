# Advanced RTDE Monitor - URCap for PolyScope X

A comprehensive URCap for real-time robot data monitoring and control using RTDE (Real-Time Data Exchange) protocol with WebSocket streaming.

## Features

### Real-Time Data Monitoring

Organized into four draggable data cards:

| Card | Signals |
|------|---------|
| **Position & Joints** | TCP Pose (X, Y, Z, RX, RY, RZ), Joint Positions (J0–J5) |
| **I/O Signals** | Digital I/O bits, Standard Analog (AI0/AI1, AO0/AO1), Tool I/O (AI types, AI0/AI1, output voltage/current/mode, DO modes), Registers |
| **Temperature** | Joint Temperatures (J0–J5), Tool Temperature |
| **Dynamics & Voltage** | Timestamp, Execution Time, Joint Velocities/Currents, TCP Speed/Force/Acceleration/Offset, Main/Robot/Joint Voltages, TCP Force Scalar |

### Control

- **Digital Output**: Select and toggle digital outputs (DO 0–7) via dropdown
- **Monitoring Toggle**: Start/Stop real-time data streaming with a toggle switch
- **Data Rate Display**: Live message rate (msg/s) indicator

### Draggable Data Cards

Data cards can be horizontally dragged to reorder:

![Draggable Data Cards](images/jog-card.gif)

### Technical Highlights

- **WebSocket Streaming**: Real-time data updates at 125Hz RTDE frequency
- **Dual Architecture**: Python backend (FastAPI) + Angular frontend
- **Docker Container**: Isolated backend service with RTDE connection
- **Automatic Reconnection**: Robust error handling and connection recovery
- **Draggable Cards**: Horizontally draggable data cards (Angular CDK Drag & Drop)
- **Manual Change Detection**: Optimized rendering for high-frequency data updates

## Requirements

- **SDK Version**: v0.20.19
- **PolyScope X**: Tested on v10.13
- **Robot Controller**: UR with RTDE support

## Installation

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

## Project Structure

```
advanced-rtde/
├── .cursor/
│   └── skills/
│       └── panel-height-guide/
│           └── SKILL.md                # Cursor AI skill for optimal panel height
│
├── advanced-rtde-backend/              # Python backend service
│   ├── src/
│   │   ├── main.py                     # FastAPI app with WebSocket & REST endpoints
│   │   ├── connector.py                # RTDE connection handler
│   │   ├── rtdeIO.xml                  # RTDE I/O recipe configuration (42 signals)
│   │   ├── RTDE_Outputs.csv            # RTDE output field reference
│   │   └── utils.py                    # Helper functions
│   ├── requirements.txt
│   └── Dockerfile
│
├── advanced-rtde-frontend/             # Angular 21 frontend
│   ├── src/app/components/
│   │   └── rtde-communicator/
│   │       ├── rtde-communicator.component.ts      # Main component with drag & drop
│   │       ├── rtde-communicator.component.html    # Template with 4 data cards
│   │       ├── rtde-communicator.component.scss    # Layout & responsive styling
│   │       ├── rtde-communicator.behavior.worker.ts
│   │       ├── rtde-communicator.node.ts
│   │       └── backend.service.ts                  # WebSocket & HTTP client
│   ├── package.json
│   └── tsconfig.json
│
├── package.json                        # Root package configuration
└── manifest.yaml                       # URCap metadata & container ingress config
```

## RTDE Signals

The backend subscribes to 42 RTDE output fields configured in `rtdeIO.xml`:

<details>
<summary>Full signal list</summary>

**Motion & Position**
- `timestamp`, `actual_execution_time`
- `actual_q`, `actual_qd`, `actual_current` (VECTOR6D)
- `actual_TCP_pose`, `actual_TCP_speed`, `actual_TCP_force`, `actual_TCP_acceleration` (VECTOR6D)
- `tcp_offset` (VECTOR6D), `tcp_force_scalar`

**I/O**
- `actual_digital_input_bits`, `actual_digital_output_bits` (UINT64)
- `actual_configurable_digital_input_bits`, `actual_configurable_digital_output_bits` (UINT64)
- `analog_io_types`, `standard_analog_input0/1`, `standard_analog_output0/1`, `io_current`
- `tool_analog_input_types`, `tool_analog_input0/1`
- `tool_output_voltage`, `tool_output_current`, `tool_output_mode`
- `tool_digital_output0_mode`, `tool_digital_output1_mode`
- `output_int_register_0`

**Status**
- `robot_mode`, `joint_mode`, `safety_mode`, `safety_status`
- `runtime_state`, `robot_status_bits`

**Temperature & Voltage**
- `joint_temperatures` (VECTOR6D), `tool_temperature`
- `actual_main_voltage`, `actual_robot_voltage`, `actual_joint_voltage` (VECTOR6D)

</details>

The backend also supports writing outputs via two recipes: `std_outputs` and `conf_outputs`.

## Usage

### Starting Data Monitor

1. Open the URCap in PolyScope X
2. Navigate to the "Rtde Communicator" page
3. Toggle **"Start Monitoring"** to begin WebSocket streaming
4. Data cards display real-time values organized by category
5. Drag cards horizontally to reorder them

### Digital Output Control

1. Select a digital output from the dropdown (DO 0–7)
2. Click **"Set High[1]"** or **"Set Low[0]"** to change the output state

### Stopping Monitor

Toggle **"Stop Monitoring"** to disconnect the WebSocket and stop data streaming.

## Development

### Backend

```bash
cd advanced-rtde-backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 52761
```

Key endpoints:
- `WebSocket /ws` — Real-time RTDE data streaming
- `GET /random` — Test endpoint returning a random number
- `POST /digital-output` — Set digital output state

### Frontend

```bash
cd advanced-rtde-frontend
npm install
npm start
```

Tech stack:
- **Angular 21** with Angular Elements (Custom Elements)
- **@universal-robots/contribution-api** v0.20.19
- **Angular CDK** for drag & drop
- **RxJS** for reactive data streams

### Adding RTDE Signals

1. Add the field to `advanced-rtde-backend/src/rtdeIO.xml`:

```xml
<recipe key="state">
    <field name="your_new_field" type="DOUBLE"/>
</recipe>
```

2. The backend automatically streams all fields in the `state` recipe
3. Access the value in the frontend template: `{{ robotData?.your_new_field }}`

## Cursor AI Skill

This project includes a Cursor AI skill at `.cursor/skills/panel-height-guide/` that provides optimal panel height values for PolyScope X Application Node panels. When creating new panels, Cursor automatically applies the correct `calc(100vh - 160px)` height pattern to fill the display without gaps or clipping.

## Troubleshooting

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
npm run clean-dist
npm run clean-target
npm install
npm run build
```

## Version History

### v1.1.0 (Current)
- Expanded to 42 RTDE output signals (position, I/O, temperature, dynamics, voltage)
- Draggable data cards with horizontal reordering
- Live data rate indicator (msg/s)
- Toggle switch for monitoring control
- Cursor AI skill for panel height optimization

### v1.0.0
- SDK v0.20.19 support
- Angular 21 upgrade
- Tool Analog Input monitoring (AI0, AI1)
- WebSocket real-time streaming
- Tested on PolyScope X v10.13

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache-2.0

## Links

- [PolyScope X SDK Documentation](https://docs.universal-robots.com/PolyScopeX_SDK_Documentation/)
- [RTDE Guide](https://www.universal-robots.com/articles/ur/interface-communication/real-time-data-exchange-rtde-guide/)
- [URCap Development](https://www.universal-robots.com/plus/software-platform/)

## Contact

For issues and questions, please open an issue on [GitHub](https://github.com/FuNingHu/advanced-rtde-x-extended).

---

**Note**: This URCap requires PolyScope X v10.11.0 or later with RTDE support enabled.
