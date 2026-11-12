import serial
import socket
import re

# -------------------------------
# SERIAL CONFIGURATION
# -------------------------------
SERIAL_PORT = "/dev/ttyUSB0"     # ✅ CHANGE if required
BAUD_RATE = 9600

# -------------------------------
# NETWORK CONFIGURATION
# -------------------------------
UDP_IP = "192.168.10.12"         # ✅ Receiver IP
UDP_PORT = 5005

# -------------------------------
# PARSE PIR DATA
# -------------------------------
def parse_pir(line):
    """
    Parses PIR data.
    Expected input:
    '1' → motion detected
    '0' → no motion

    Output format:
    motion=1 OR motion=0
    """
    match = re.search(r"[01]", line)
    if match:
        value = match.group(0)
        return f"brain_status={value}"
    return None

# -------------------------------
# READ SERIAL DATA
# -------------------------------
def read_serial_data():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"[TX] Listening on {SERIAL_PORT} @ {BAUD_RATE} baud...")

            while True:
                raw_line = ser.readline().decode("utf-8", "ignore").strip()

                if raw_line:
                    print(f"[TX] Raw Sensor Data: {raw_line}")

                    parsed = parse_pir(raw_line)

                    if parsed:
                        print(f"[TX] Parsed Sensor Data: {parsed}")
                        yield parsed

    except serial.SerialException as e:
        print(f"[TX] Serial Error: {e}")

# -------------------------------
# BROADCAST DATA
# -------------------------------
def broadcast(data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data.encode('utf-8'), (UDP_IP, UDP_PORT))
        print(f"[TX] Sent UDP Packet: {data}")

# -------------------------------
# MAIN LOOP
# -------------------------------
if __name__ == "__main__":
    for packet in read_serial_data():
        broadcast(packet)

