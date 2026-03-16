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
        'actual_TCP_pose': data.actual_TCP_pose,
        'actual_q': data.actual_q,
        'robot_mode': data.robot_mode,
        'output_int_register_0': data.output_int_register_0,
        'runtime_state': data.runtime_state,
        'safety_status': data.safety_status,
        'actual_digital_input_bits': data.actual_digital_input_bits,
        'actual_digital_output_bits': data.actual_digital_output_bits,
        'tool_analog_input0': data.tool_analog_input0,
        'tool_analog_input1': data.tool_analog_input1,
    })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, rtde_connect: RTDEConnect = Depends(get_rtde_connection)):
    await manager.connect(websocket)
    print(f"WebSocket client connected. Total connections: {len(manager.active_connections)}")
    
    # Send initial test message
    try:
        test_data = rtde_connect.receive()
        if test_data:
            test_message = create_message(test_data)
            await websocket.send_text(test_message)
            print(f"Sent initial test message to client")
        else:
            print("Warning: Could not get initial test data from RTDE")
    except Exception as e:
        print(f"Error sending initial test message: {e}")
    
    message_count = 0
    try:
        while True:
            try:
                data = rtde_connect.receive()
                if data:
                    message = create_message(data)
                    await manager.broadcast(message)
                    message_count += 1
                    if message_count % 50 == 0:  # Log every 50 messages
                        print(f"Sent {message_count} messages to {len(manager.active_connections)} clients")
                else:
                    print("Warning: No data received from RTDE")
                await asyncio.sleep(1 / rtde_connect.frequency)
            except Exception as receive_error:
                print(f"Error receiving data: {receive_error}")
                # Continue loop to wait for reconnection
                await asyncio.sleep(1.0)
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
