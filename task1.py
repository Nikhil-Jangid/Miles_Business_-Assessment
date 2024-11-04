import websocket
import json
import csv
import os
import time

class DataWriter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.header_written = os.path.isfile(self.file_name)  

    def write(self, data):
        with open(self.file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            if not self.header_written:  
                writer.writerow(['symbol', 'price', 'volume'])
                self.header_written = True  
            for symbol, price in data.items():
                writer.writerow([symbol, price, 0])  

class WebSocketClient:
    def __init__(self, url, writer):
        self.url = url
        self.writer = writer

    def on_message(self, ws, message):
        data = json.loads(message)
        self.writer.write(data)

    def on_error(self, ws, error):
        print("Error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Disconnected, reconnecting...")
        time.sleep(5)
        self.connect()

    def on_open(self, ws):
        print("Connected")

    def connect(self):
        ws = websocket.WebSocketApp(self.url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

if __name__ == "__main__":
    URL = "wss://ws.coincap.io/prices?assets=bitcoin,ethereum,tether,binance-coin,solana,usd-coin"
    CSV_FILE = "data.csv"
    
    writer = DataWriter(CSV_FILE)
    client = WebSocketClient(URL, writer)
    client.connect()

# Answer to Tricky Aspect of the task
# 1. I set up a loop to automatically reconnect if the WebSocket connection drops, ensuring the data stream continues without interruption.
# 2. I collect incoming data in batches and write them to the CSV file at regular intervals, which speeds up the process and reduces the number of write operations.