import serial
import socket
import re

# Serial Configuration
SERIAL_PORT = '/dev/ttyUSB0'    # Updated to your port
BAUD_RATE = 115200

# Network Configuration
UDP_IP = '192.168.10.12'
UDP_PORT = 5005

def parse_sensor_line(line):
    """
    Parses a line like:
    'Humidity: 54.00 %       Temperature: 24.10 °C'
    Returns a dict or the original line if parsing fails.
    """
    match = re.search(r'Humidity:\s*([\d.]+).*Temperature:\s*([\d.]+)', line)
    if match:
        humidity = match.group(1)
        temperature = match.group(2)
        return f"humidity={humidity}, temperature={temperature}"
    else:
        return line

def read_serial_data():
    """
    Reads data from the serial port and yields each line.
    """
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud...")
            while True:
                raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
                if raw_line:
                    print(f"Raw Serial: {raw_line}")
                    parsed = parse_sensor_line(raw_line)
                    print(f"Parsed: {parsed}")
                    yield parsed
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return

def broadcast_data(data):
    """
    Broadcasts data over UDP.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data.encode('utf-8'), (UDP_IP, UDP_PORT))
        print(f"Broadcasted: {data}")

if __name__ == '__main__':
    for serial_data in read_serial_data():
        broadcast_data(serial_data)

