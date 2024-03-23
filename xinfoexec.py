from libinstaller import *
try:
    install_and_show_output("python3-nmap")
    install_and_show_output("python3-networkx")
    install_and_show_output("python3-matplotlib")
except subprocess.CalledProcessError as e:
    print(f"Error installing: {e}")
    
from xprintinfo import *
from xgetinfo import *
from xgetinforemote import *
from libchecker import *

def print_banner():
    banner = """
██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     
╚██╗██╔╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     
 ╚███╔╝    ██║   ██║   ██║██║   ██║██║     
 ██╔██╗    ██║   ██║   ██║██║   ██║██║     
██╔╝ ██╗   ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝

      
█████╗
╚════╝
     

 ██████╗ ███████╗████████╗██╗███╗   ██╗███████╗ ██████╗ 
██╔════╝ ██╔════╝╚══██╔══╝██║████╗  ██║██╔════╝██╔═══██╗
██║  ███╗█████╗     ██║   ██║██╔██╗ ██║█████╗  ██║   ██║
██║   ██║██╔══╝     ██║   ██║██║╚██╗██║██╔══╝  ██║   ██║
╚██████╔╝███████╗   ██║   ██║██║ ╚████║██║     ╚██████╔╝
 ╚═════╝ ╚══════╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 1.0
                                                        

Created by: X(@Xscriptor-xscriptorcode)
    """
    
    print(banner)

def print_main_menu():
    print("*_________________________________*")
    print("Main Menu:")
    print("1. Local Machine Information")
    print("2. External Machine Tests")
    print("3. Exit")
    print("*_________________________________*")

def print_menu():
    print("*_________________________________*")
    print("Menu:")
    print("1. System Information")
    print("2. CPU Information")
    print("3. Memory Information")
    print("4. Processes")
    print("5. Network Information")
    print("6. Disk Information")
    print("7. Exit")
    print("*_________________________________*")

def print_external_menu():
    print("*_________________________________*")
    print("External Machine Tests:")
    print("1. Scann your network")
    print("2. Scan subnet")
    print("3. Scan a target with the ip(OS information)")
    print("4. Scan a target with the ip(Vulnerabilities)")
    print("5. Scan and create a map")
    print("6. Exit")
    print("*_________________________________*")

def main():
    print_banner()
    check_and_install_libraries()
    while True:
        try:
            print_main_menu()
            choice = input("Select an option (1-3): ")

            if choice == '3':
                print("Exiting program...")
                break
            elif choice == '1':
                while True:
                    print_menu()
                    choice_local = input("Select an option (1-7): ")

                    if choice_local == '7':
                        break
                    elif choice_local in {'1', '2', '3', '4', '5', '6'}:
                        info_functions = {
                            '1': print_system_info,
                            '2': print_cpu_info,
                            '3': print_memory_info,
                            '4': print_processes,
                            '5': print_network_info,
                            '6': print_disk_info,
                        }

                        info_func = info_functions.get(choice_local)
                        if info_func:
                            info_func()
                        else:
                            print("Invalid choice. Please select a number from 1 to 7.")
                    else:
                        print("Invalid choice. Please select a number from 1 to 7.")
            elif choice == '2':
                while True:
                    print_external_menu()
                    choice_locall = input("Select an option (1-6): ")

                    if choice_locall == '6':
                        break
                    elif choice_locall in {'1', '2', '3', '4', '5'}:
                        if choice_locall == '1':
                            devices = scan_network_devices()
                            for device in devices:
                                print(f"IP: {device['ip']}, Hostname: {device['hostname']}, MAC: {device['mac']}, Vendor: {device['vendor']}")
                        elif choice_locall == '2':
                            subnet = input("Enter the subnet of your local network (e.g., 192.168.1.0/24): ")
                            scan_local_network(subnet)
                        elif choice_locall == '3':
                            ip_address = input("Enter the IP address of the remote machine: ")
                            scan_remote_system(ip_address)
                        elif choice_locall == '4':
                            ip_address = input("Enter the IP address of the remote machine: ")
                            scan_for_vulnerabilities(ip_address)
                        elif choice_locall == '5':
                            ip_address = input("Enter the IP address with /24 at the end if it's kist your network then: 192.168.1.0/24: ")
                            output_file = input("Enter the file name to save the network map: ")
                            create_network_map(ip_address, output_file)
                        else:
                            print("Invalid choice. Please select a number from 1 to 2.")
                    else:
                        print("Invalid choice. Please select a number from 1 to 7.")
            else:
                print("Invalid choice. Please select a number from 1 to 6.")
        except ValueError:
            print("\nError. Exiting program...")
        except KeyboardInterrupt:
            print("\nExiting program...")

if __name__ == "__main__":
    main()
