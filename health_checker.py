import subprocess
import time
import ipaddress
import logging
import logger_config

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def ping_device(ip):
    
    if not validate_ip(ip):
        logging.error(f"Invalid IP address: {ip}")
        return "INVALID_IP", None
    
    start_time = time.time()
    
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "1000", ip],
        capture_output=True
    )
    
    end_time = time.time()
    
    response_time = (end_time - start_time) * 1000
    
    if result.returncode == 0:
        logging.info(
            f"Device {ip} is reachable. "
            f"Response time: {round(response_time, 2)}ms"
        )
        return "REACHABLE", response_time
    else:
        logging.warning(
            f"Device {ip} is unreachable."
        )
        return "UNREACHABLE", response_time
    
def test_devices(devices):
    
    for device in devices:
        status, response_time = ping_device(device["ip"])
        device["status"] = status
        if status == "INVALID_IP":
            device["response_time"] = "N/A"
        else:
            device["response_time"] = f"{round(response_time, 2)}ms"
        
        
def get_health_summary(devices):
    reachable = 0
    unreachable = 0
    invalid = 0

    for device in devices:
        if device["status"] == "REACHABLE":
            reachable += 1
        elif device["status"] == "UNREACHABLE":
            unreachable += 1
        elif device["status"] == "INVALID_IP":
            invalid += 1
            
    return reachable, unreachable, invalid

        