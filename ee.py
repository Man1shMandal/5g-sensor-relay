import serial
import socket

# Serial Configuration
SERIAL_PORT = '/dev/ttyUSB0'   # <-- Change to match your port
BAUD_RATE = 115200

# Network Configuration
UDP_IP = '192.168.10.12'       # Receiver machine IP
UDP_PORT = 5005

def read_serial_data():
    """
    Continuously reads the signed EEG values from Arduino ADS1298.
    Arduino prints ONE number per line.
    """
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening on {SERIAL_PORT} (baud={BAUD_RATE})")

            while True:
                raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
                if raw_line:
                    print(f"Serial: {raw_line}")   # Shows raw EEG value
                    yield raw_line

    except serial.SerialException as e:
        print(f"Serial Error: {e}")
        return


def broadcast_data(data):
    """
    Sends raw EEG integer value via UDP.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(data.encode('utf-8'), (UDP_IP, UDP_PORT))
        print(f"Broadcasted: {data}")


if __name__ == "__main__":
    for value in read_serial_data():
        broadcast_data(value)
