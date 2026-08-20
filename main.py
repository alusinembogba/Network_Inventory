import json
import time
import csv
import ipaddress
from datetime import datetime
from health_checker import test_devices,get_health_summary



def load_inventory():
    try:
        with open("inventory.json", "r") as file:
            devices = json.load(file)
            return devices
    except FileNotFoundError:
        return []
 
 
def show_inventory(inventory):
    print("\nNetwork Inventory")
    print('-'*20)
    print()
    
    if not inventory:
        print("No devices found.\n")
        return

    for device in inventory:
        print(device["hostname"])
        print(f"IP: {device['ip']}")
        print(f"Type: {device['device_type']}")
        print(f"Vendor: {device['vendor']}")
        print(f"Status: {device['status']}")
        print()   


def add_device(inventory):

    # -------------------------
    # HOSTNAME VALIDATION
    # -------------------------

    while True:

        hostname = input("Hostname: ").strip()

        if hostname.lower() == "cancel":
            print("Add cancelled.")
            return

        if not hostname:
            print("\nHostname cannot be empty.")
            print("Try again or enter 'cancel' to stop adding.")
            continue

        hostname_exists = False

        for device in inventory:
            if device["hostname"].lower() == hostname.lower():
                hostname_exists = True
                break

        if hostname_exists:
            print("\nError: Hostname already assigned to another device.")
            print("Try again or enter 'cancel' to stop adding.")
            continue

        break


    # -------------------------
    # IP VALIDATION
    # -------------------------

    while True:

        ip = input("IP Address: ").strip()

        if ip.lower() == "cancel":
            print("Add cancelled.")
            return

        if not validate_ip(ip):
            print(f"\nError: {ip} is not a valid IP address.")
            print("Try again or enter 'cancel' to stop adding.")
            continue

        ip_exists = False

        for device in inventory:
            if device["ip"] == ip:
                ip_exists = True
                break

        if ip_exists:
            print("\nError: IP already assigned to another device.")
            print("Try again or enter 'cancel' to stop adding.")
            continue

        break


    # -------------------------
    # DEVICE INFORMATION
    # -------------------------

    device_type = input("Device Type: ")
    vendor = input("Vendor: ")
    status = input("Status: ")


    # -------------------------
    # CREATE DEVICE
    # -------------------------

    new_device = {
        "hostname": hostname,
        "ip": ip,
        "device_type": device_type,
        "vendor": vendor,
        "status": status
    }

    inventory.append(new_device)

    print("\nDevice added successfully!\n")

    return True
    
    
def save_inventory(inventory):
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)  


def search_device(inventory):
    
    if not inventory:
        print("No devices found.\n")
        return 
    
    while True:
        print("\nSearch Options")
        print("1. Hostname")
        print("2. IP Address")
        try:
            option = int(input("Enter a number: "))
        except ValueError:
            print("Numbers only 1 or 2.")
        else: 
            if option == 1:
                
                hostname = input("Search hostname: ")
                
                device = next((dev for dev in inventory 
                               if dev["hostname"].lower() == hostname.lower()),
                              None
                )
                
                if device: 
                    print("\nCurrent Information")
                    print(f"Hostname: {device['hostname']}")
                    print(f"IP: {device['ip']}")
                    print(f"Device Type: {device['device_type']}")
                    print(f"Vendor: {device['vendor']}")
                    print(f"Status: {device['status']}")
                    print()
                    
                    return True
                else:
                    print("Device not found.\n")
                    print()  
                    return False
            elif option == 2:
                
                ip = input("Search IP Address: ")
                
                device = next((dev for dev in inventory 
                               if dev["ip"] == ip),
                              None
                )
                
                if device: 
                    print("\nCurrent Information")
                    print(f"Hostname: {device['hostname']}")
                    print(f"IP: {device['ip']}")
                    print(f"Device Type: {device['device_type']}")
                    print(f"Vendor: {device['vendor']}")
                    print(f"Status: {device['status']}")
                    print()
                    return True
                else:
                    print("Device not found.\n")
                    return False
                
            else:
                print("Enter an option 1 or 2.")
        
   
def delete_device(inventory):
    hostname = input("Search hostname: ")
    
    if not inventory:
        print("No devices found.\n")
        return  
    while True:
        option = input(f"Delete {hostname}? (y/n): ")

        if option.lower() == "y":
            
            for i, device in enumerate(inventory):
                
                if device["hostname"].lower() == hostname.lower():
                    deleted = inventory.pop(i)
                    print(f"Deleted: {deleted['hostname']}")
                    return True
                
            print("Device not found")
            return False
        elif option.lower() == "n":
            print()
            return False
            
        else:
            print("Enter a y for yes or n for no")
       

def update_device(inventory):  
    
    hostname = input("Search hostname: ")
    
    if not inventory:
        print("No devices found.\n")
        return      
    
    device = next((dev for dev in inventory 
                   if dev["hostname"].lower() == hostname.lower()),
                  None
    )
    
    if not device: 
        print("Device not found.\n")
        return False
    
       
    print("\nCurrent Information")
    print()
    print(f"Hostname: {device['hostname']}")
    print(f"IP: {device['ip']}")
    print(f"Device Type: {device['device_type']}")
    print(f"Vendor: {device['vendor']}")
    print(f"Status: {device['status']}")
    print()
    
    ip = input("New IP Address: ").strip() or device["ip"]
    
    if not validate_ip(ip):
        print("Error: Invalid IP address")
        return False
    
    for other_device in inventory:

        if other_device is device:
            continue
        
        if other_device["ip"] == ip:
            print("Error: ip already assigned to another device")
            return False
    
    device_type = input("New Device Type: ") or device["device_type"]
    vendor = input("New Vendor: ") or device["vendor"]
    status = input("New Status: ") or device["status"]
    
    
    updates = {
        "ip": ip,
        "device_type": device_type,
        "vendor": vendor,
        "status": status       
    }  

    device.update(updates)
    
    print(f"\nUpdated {device['hostname']}")
    print("\nUpdated Information")
    print(f"Hostname: {device['hostname']}")
    print(f"IP: {device['ip']}")
    print(f"Device Type: {device['device_type']}")
    print(f"Vendor: {device['vendor']}")
    print(f"Status: {device['status']}")
    print()   
    
    return True
        

def export_txt(inventory):
    
    filename = "inventory.txt"
    
    if not inventory:
        print("No device found\n")
        return
    
    with open(filename, "w") as file:
        file.write("\nNETWORK INVENTORY REPORT\n")
        file.write("="*30 + "\n")
        for device in inventory:
            file.write('\n')
            file.write(f"Hostname: {device['hostname']} \n")
            file.write(f"IP: {device['ip']} \n")
            file.write(f"Device Type: {device['device_type']} \n")
            file.write(f"Vendor: {device['vendor']} \n")
            file.write(f"Status: {device['status']} \n")
            file.write('\n')
            file.write("-"*30 + "\n")
    print(f"Exported to {filename}")

def export_csv(inventory):
    
    filename = "inventory.csv"
    
    if not inventory:
        print("No Devices found")
        return
    
    fieldnames = ["hostname", "ip", "device_type", "vendor", "status"]
    
    with open(filename,"w",newline="") as file:
        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()
        writer.writerows(inventory)
    print(f"Exported {len(inventory)} devices to {filename}")
 
 
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
  


def main():
    inventory = load_inventory()

    while True:
        print("\nNetwork Inventory System")
        print("-" * 25)
        print("1. Show Devices")
        print("2. Add Devices")
        print("3. Search Device")
        print("4. Delete Device")
        print("5. Update Device")
        print("6. Export TXT Report")
        print("7. Export CSV Report")
        print("8. Run Network Health Check")
        print("9. Exit")
        print()

        try:
            option = int(input("Enter the option: "))

        except ValueError:
            print("Must be a number!")

        else:
            if option == 1:
                show_inventory(inventory)
                time.sleep(2)

            elif option == 2:
                if add_device(inventory):
                    show_inventory(inventory)
                    save_inventory(inventory)

            elif option == 3:
                search_device(inventory)
                time.sleep(2)

            elif option == 4:
                if delete_device(inventory):
                    save_inventory(inventory)
                time.sleep(2)

            elif option == 5:
                if update_device(inventory):
                    save_inventory(inventory)
                time.sleep(2)

            elif option == 6:
                export_txt(inventory)
                time.sleep(2)
                
            elif option == 7:
                export_csv(inventory)
                time.sleep(2)
                
            elif option == 8:
                test_devices(inventory)
                reachable,unreachable, invalid = get_health_summary(inventory)
                
                print("\nNetwork Health Check")
                print("-" * 25)
                print(f"Checked: {datetime.now().strftime('%d %B %Y %H:%M:%S')}")
                print()
                for device in inventory:
                    
                    print(
                        f"{device['hostname']} | "
                        f"{device['ip']} | "
                        f"{device['status']} | "
                        f"{device['response_time']}"
                    )
                    print() 
                
                
                print("\nSummary")
                print("-"*10)
    
                print(f"Total devices: {len(inventory)}")
                print(f"Reachable: {reachable}")
                print(f"Unreachable: {unreachable}")        
                print(f"Invalid IP: {invalid}")
                        
                save_inventory(inventory)
                time.sleep(2)

            elif option == 9:
                print("\nExiting program...")
                break

            else:
                print("\nEnter an option (1-9)")
                
if __name__ == "__main__":
    main()
