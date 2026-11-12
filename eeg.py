#!/usr/bin/env python3
# tx_ads1298_debug.py
import serial, socket, re, time, json

SERIAL_PORT = '/dev/ttyUSB0'   # change for your system
BAUD_RATE = 115200
UDP_IP = '192.168.10.12'
UDP_PORT = 5005
INT_RE = re.compile(r'(-?\d+)')

def open_serial():
    import time
    while True:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print(f"[TX] Opened {SERIAL_PORT} @ {BAUD_RATE}")
            return ser
        except Exception as e:
            print(f"[TX] Serial open error: {e}; retrying in 2s")
            time.sleep(2)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ser = open_serial()
    seq = 0
    try:
        while True:
            raw = ser.readline().decode('utf-8', errors='ignore').strip()
            if not raw:
                continue
            seq += 1
            m = INT_RE.search(raw)
            value = int(m.group(1)) if m else None
            packet = {"seq": seq, "t": time.time(), "raw": raw}
            if value is not None:
                packet["value"] = value
            payload = json.dumps(packet)
            sock.sendto(payload.encode('utf-8'), (UDP_IP, UDP_PORT))
            print(f"[TX] Sent -> {UDP_IP}:{UDP_PORT} : {payload}")
    except KeyboardInterrupt:
        print("[TX] stopped")
    finally:
        try: ser.close()
        except: pass
        sock.close()

if __name__ == '__main__':
    main()
