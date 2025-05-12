import pymysql
from pymysql import Error
import json
import asyncio
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import websockets

app = Flask(__name__)
socketio = SocketIO(app)

def get_db_connection():

    try:
        connection = pymysql.connect(
            host='localhost',  
            user='root',       
            password='1234',  
            database='sensor_db',  
            cursorclass=pymysql.cursors.DictCursor  
        )
        return connection
    
    except pymysql.MySQLError as e:
        print(f"Database connection error: {e}")
        return None
    
def create_db_and_table():
    connection = pymysql.connect(
        host="localhost",  
        user="root",       
        password="1234"    
    )

    try:
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS sensor_db") 
        cursor.execute("USE sensor_db")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            temperature1 FLOAT,
            humidity1 FLOAT,
            cds FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        print("DB, Table created.")

    except Error as e:
        print(f"Failed: {e}")

    finally:
        cursor.close()
        connection.close()

clients = set()

sensor_data = {
    "temperature": 0,
    "humidity": 0,
    "cds": 0
}

@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    if msg == "pong":
        print("클라이언트에서 pong 받음")

ping_attempts = {}

async def handler(websocket, path):
    clients.add(websocket)
    print(f"새로운 클라이언트 연결: {websocket.remote_address}")

    try:

        async for message in websocket:
            print(f"클라이언트 메시지 수신: {message}")

            try:

                print(f"Received data: {message}")

                data = json.loads(message)

                temperature1 = data.get("temperature1")
                humidity1 = data.get("humidity1")
                cds = data.get("cds")

                print(f"Parsed Data - temperature1: {temperature1}, humidity1: {humidity1}, cds: {cds}")

                if all(v is not None for v in [temperature1, humidity1, cds]):

                    sensor_data["temperature"] = temperature1
                    sensor_data["humidity"] = humidity1
                    sensor_data["cds"] = cds

                    connection = get_db_connection()
                    if connection:

                        with connection.cursor() as cursor:
                            sql = "INSERT INTO sensor_data (temperature1, humidity1, cds) VALUES (%s, %s, %s)"
                            cursor.execute(sql, (temperature1, humidity1, cds))
                            connection.commit()
                        connection.close()

                    socketio.emit('sensor_data', sensor_data)

            except json.JSONDecodeError:
                print("잘못된 JSON 형식의 메시지 수신")

    except websockets.exceptions.ConnectionClosed:
        print(f"클라이언트 연결 종료: {websocket.remote_address}")

    finally:
        clients.remove(websocket)

async def websocket_server():
    import websockets
    server = await websockets.serve(handler, "0.0.0.0", 49154)
    await server.wait_closed()

@app.route('/')
def index():
    return render_template('index.html')

def run_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_server())

if __name__ == '__main__':

    create_db_and_table()

    websocket_thread = threading.Thread(target=run_websocket_server)
    websocket_thread.daemon = True
    websocket_thread.start()

    socketio.run(app, host="0.0.0.0", port=5000)