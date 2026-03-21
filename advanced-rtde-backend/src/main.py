import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from connector import RTDEConnect
from utils import set_digital_outputs
import asyncio
import json

app = FastAPI()

ROBOT_HOST = 'urcontrol-rtde'
CONFIG_FILENAME = 'rtdeIO.xml'


class RTDEConnection:
    def __init__(self, robot_host: str, config_filename: str):
        self.connection = RTDEConnect(robot_host, config_filename)
    
    def get_connection(self):
        self.connection.check_and_reconnect()
        return self.connection


# Create a singleton instance of RTDEConnection
rtde_connection_instance = RTDEConnection(ROBOT_HOST, CONFIG_FILENAME)


# Dependency injection function
def get_rtde_connection():
    return rtde_connection_instance.get_connection()


class DigitalOutputRequest(BaseModel):
    digital_output: int
    value: int
    offset: int = 0


# WebSocket manager to keep track of active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting to connection, marking for removal: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()


def create_message(data):
    return json.dumps({
        'timestamp': data.timestamp,
        'actual_q': data.actual_q,
        'actual_qd': data.actual_qd,
        'actual_current': data.actual_current,
        'actual_TCP_pose': data.actual_TCP_pose,
        'actual_TCP_speed': data.actual_TCP_speed,
        'actual_TCP_force': data.actual_TCP_force,
        'tcp_offset': data.tcp_offset,
        'actual_digital_input_bits': data.actual_digital_input_bits,
        'actual_TCP_acceleration': data.actual_TCP_acceleration,
        'actual_configurable_digital_input_bits': data.actual_configurable_digital_input_bits,
        'joint_temperatures': data.joint_temperatures,
        'actual_execution_time': data.actual_execution_time,
        'robot_mode': data.robot_mode,
        'joint_mode': data.joint_mode,
        'safety_mode': data.safety_mode,
        'safety_status': data.safety_status,
        'actual_main_voltage': data.actual_main_voltage,
        'actual_robot_voltage': data.actual_robot_voltage,
        'actual_joint_voltage': data.actual_joint_voltage,
        'actual_digital_output_bits': data.actual_digital_output_bits,
        'actual_configurable_digital_output_bits': data.actual_configurable_digital_output_bits,
        'runtime_state': data.runtime_state,
        'robot_status_bits': data.robot_status_bits,
        'analog_io_types': data.analog_io_types,
        'standard_analog_input0': data.standard_analog_input0,
        'standard_analog_input1': data.standard_analog_input1,
        'standard_analog_output0': data.standard_analog_output0,
        'standard_analog_output1': data.standard_analog_output1,
        'io_current': data.io_current,
        'output_int_register_0': data.output_int_register_0,
        'tool_analog_input_types': data.tool_analog_input_types,
        'tool_analog_input0': data.tool_analog_input0,
        'tool_analog_input1': data.tool_analog_input1,
        'tool_output_voltage': data.tool_output_voltage,
        'tool_output_current': data.tool_output_current,
        'tool_temperature': data.tool_temperature,
        'tool_output_mode': data.tool_output_mode,
        'tool_digital_output0_mode': data.tool_digital_output0_mode,
        'tool_digital_output1_mode': data.tool_digital_output1_mode,
        'tcp_force_scalar': data.tcp_force_scalar,
    })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, rtde_connect: RTDEConnect = Depends(get_rtde_connection)):
    await manager.connect(websocket)
    print(f"WebSocket client connected. Total connections: {len(manager.active_connections)}")
    
    # Send initial test message
    try:
        rtde_connect.check_and_reconnect()
        test_data = rtde_connect.receive()
        if test_data:
            test_message = create_message(test_data)
            await websocket.send_text(test_message)
            print(f"Sent initial test message to client")
        else:
            print("Warning: Could not get initial test data from RTDE")
    except Exception as e:
        print(f"Error sending initial test message: {e}, will retry in main loop")
    
    message_count = 0
    reconnect_attempts = 0
    max_reconnect_log = 5
    try:
        while True:
            try:
                data = rtde_connect.receive()
                if data:
                    message = create_message(data)
                    await manager.broadcast(message)
                    message_count += 1
                    reconnect_attempts = 0
                    if message_count % 50 == 0:
                        print(f"Sent {message_count} messages to {len(manager.active_connections)} clients")
                else:
                    print("Warning: No data received from RTDE")
                await asyncio.sleep(1 / rtde_connect.frequency)
            except Exception as receive_error:
                reconnect_attempts += 1
                if reconnect_attempts <= max_reconnect_log:
                    print(f"Error receiving data (attempt {reconnect_attempts}): {receive_error}")
                elif reconnect_attempts == max_reconnect_log + 1:
                    print(f"Suppressing further error logs, will keep retrying...")
                try:
                    rtde_connect.check_and_reconnect()
                except Exception as reconnect_error:
                    if reconnect_attempts <= max_reconnect_log:
                        print(f"Reconnect failed: {reconnect_error}")
                await asyncio.sleep(3.0)
    except WebSocketDisconnect:
        print(f"WebSocket client disconnected after {message_count} messages")
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.get("/random-number")
async def get_random_number():
    return {"random_number": random.randint(1, 1000)}


@app.post("/set-digital-output")
async def set_digital_output(request: DigitalOutputRequest, rtde_connect: RTDEConnect = Depends(get_rtde_connection)):
    try:
        current_state = rtde_connect.receive().actual_digital_output_bits
        new_state, mask = set_digital_outputs(current_state, request.digital_output, request.value, request.offset)

        if request.offset == 0:  # Standard digital outputs
            rtde_connect.send("std_outputs", ["standard_digital_output_mask", "standard_digital_output"], [mask, new_state])
            # Reset the mask
            rtde_connect.send("std_outputs", ["standard_digital_output_mask", "standard_digital_output"], [0, new_state])
        elif request.offset == 8:  # Configurable digital outputs
            rtde_connect.send("conf_outputs", ["configurable_digital_output_mask", "configurable_digital_output"], [mask, new_state])
            # Reset the mask
            rtde_connect.send("conf_outputs", ["configurable_digital_output_mask", "configurable_digital_output"], [0, new_state])
        else:
            return {"status": "error", "message": f"Unknown offset: {request.offset}"} 

        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.on_event("shutdown")
def shutdown_event():
    rtde_connection_instance.get_connection().shutdown()
    
    
@app.get("/disconnect")
async def disconnect(rtde_connect: RTDEConnect = Depends(get_rtde_connection)):
    try:
        rtde_connect.shutdown()
        return {"status": "success", "message": "RTDE connection shut down successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
