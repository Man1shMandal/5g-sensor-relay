# 5G Sensor Relay

Small Python scripts that read sensor data from a microcontroller over USB serial and forward it as UDP packets to another machine.

Nothing in the code is 5G specific: the scripts send plain UDP over whatever IP link the host has (a 5G modem, Wi-Fi or Ethernet). Each script reads one line at a time from the serial port, optionally parses it into a `key=value` string, and sends it to a fixed IP and port.

## Scripts

| Script | Serial input | UDP payload |
| --- | --- | --- |
| `main.py` | any line | the line as-is |
| `DHT11Tx.py` | `Humidity: 54.00 % Temperature: 24.10 °C` | `humidity=54.00, temperature=24.10` |
| `trans.py` | load cell, e.g. `Weight: 1.234 kg` | `weight=1.234` |
| `tra.txt` | ultrasonic, e.g. `Distance: 123.4 cm` | `distance=123.4` (a .py file saved with a .txt extension) |
| `transsss.py` | `0` / `1` from a digital sensor (9600 baud) | `brain_status=0` or `1` |
| `ee.py` | one signed integer per line from an ADS1298 EEG front end | the raw value |
| `eeg.py` | same as above | JSON: `{"seq", "t", "raw", "value"}` with a sequence number and timestamp; retries the serial port until it opens |
| `tra.py` | keyboard | whatever you type; asks for the destination IP and port at start (handy for testing the link) |

`serial_monitor.py.save` is just a note with the command to list serial ports.

## Hardware

- A Linux host such as a Raspberry Pi, connected to the network you want to send over
- An Arduino or similar board printing sensor readings on USB serial (DHT11, load cell, ultrasonic, PIR/digital sensor, or an ADS1298 board)
- A second machine listening for UDP

## Stack

- Python 3
- pyserial
- Standard library `socket`, `re`, `json`

## Run

```bash
pip install pyserial
ls /dev/ttyACM* /dev/ttyUSB*      # find the board
python3 DHT11Tx.py                # or any other script
```

To try the text-only link test:

```bash
python3 tra.py
```

On the receiving side, anything that listens on UDP works, for example:

```bash
nc -ul 5005
```

## Config

Each script has its settings as constants at the top. Edit them before running:

- `SERIAL_PORT` - e.g. `/dev/ttyUSB0` or `/dev/ttyACM0`
- `BAUD_RATE` - must match the board's `Serial.begin()` (115200 in most scripts, 9600 in `transsss.py`)
- `UDP_IP` - receiver address (or a broadcast address)
- `UDP_PORT` - receiver port, 5005 by default
