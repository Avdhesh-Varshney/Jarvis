# ipadd.py
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Connect to an external server (doesn't actually connect)
        s.connect(('10.254.254.254', 1))  
        local_ip = s.getsockname()[0]
    except:
        local_ip = '127.0.0.1'  # Default to localhost if no network
    finally:
        s.close()
    return local_ip

# You can print the local IP for debugging
print("Local IP Address:", get_local_ip())