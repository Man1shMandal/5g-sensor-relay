import serial
import socket
import re

SERIAL_PORT = "/dev/ttyACM0"   # update accordingly
BAUD_RATE = 115200

UDP_IP = "192.168.10.12"
UDP_PORT = 5005

def parse_weight(line):
    """
    Supported formats:
      'Weight: 1.234 kg'
      '1.234'
      '1.234 kg'
    Output -> 'weight=1.234'
    """
    # Match either "Weight: X kg" or just numbers
    match = re.search(r"([\-\d\.]+)", line)
    if match:
        value = match.group(1)
        return f"weight={value}"
    return None

def read_serial_data():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"[TX] Listening on {SERIAL_PORT} @ {BAUD_RATE}...")
            while True:
                raw_line = ser.readline().decode("utf-8", "ignore").strip()
                if raw_line:
                    print(f"[TX] Raw Serial: {raw_line}")
                    parsed = parse_weight(raw_line)
                    if parsed:
                        print(f"[TX] Parsed: {parsed}")
                        yield parsed
    except serial.SerialException as e:
        print(f"[TX] Serial Error: {e}")

def broadcast(data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data.encode("utf-8"), (UDP_IP, UDP_PORT))
        print(f"[TX] Broadcasted: {data}")

if __name__ == "__main__":
    for packet in read_serial_data():
        broadcast(packet)

