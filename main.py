import serial
import socket

# Serial Configuration
SERIAL_PORT = '/dev/ttyACM0'  # Update with your Arduino's port
BAUD_RATE = 115200

# Network Configuration
UDP_IP = '192.168.10.12'  # Broadcast address
UDP_PORT = 5005  # Port for broadcasting

def read_serial_data():
    """
    Reads data from the serial port and yields each line.
    """
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud rate...")
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"Received New: {line}")
                    yield line
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return

def broadcast_data(data):
    """
    Broadcasts data over the network using UDP.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data.encode('utf-8'), (UDP_IP, UDP_PORT))
        print(f"Broadcasted: {data}")

if __name__ == '__main__':
    for serial_data in read_serial_data():
        broadcast_data(serial_data)

