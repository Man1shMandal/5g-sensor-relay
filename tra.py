import socket

def main():
    # Target machine info
    target_ip = input("Enter destination IP: ")
    target_port = int(input("Enter destination port: "))

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("\nType your message. Press Ctrl+C to exit.\n")

    try:
        while True:
            message = input("Message: ")
            sock.sendto(message.encode(), (target_ip, target_port))
            print("Sent.")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()

