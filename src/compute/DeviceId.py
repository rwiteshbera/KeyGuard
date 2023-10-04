import hashlib
import platform
import socket
import uuid

def getDeviceId() -> str:
    # Collect device information
    os_info = platform.platform()
    hostname = socket.gethostname()
    mac_address = ':'.join(['{:02X}'.format((int(mac, 16) + 1) % 256) for mac in hex(uuid.getnode())[2:].split(':')])
    cpu_info = platform.processor()
    
    # Combine the information into a single string
    combined_info = f"{os_info}-{hostname}-{mac_address}-{cpu_info}"
    
    # Generate a unique hash of the combined information
    device_id = hashlib.sha256(combined_info.encode()).hexdigest()

    return device_id