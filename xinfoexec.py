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
from bannersnmenu.bannerxtool import *
from bannersnmenu.clear  import *
from bannersnmenu.mainprint import *
from bannersnmenu.bannerlocal import *
from bannersnmenu.bannerext import *

def main():
    clear_terminal()
    print_banner()
    banner_printed_local = False
    banner_printed_remote = False
    while True:
        try:
            print_main_menu()
            choice = input("Select an option (1-3): ")

            if choice == '3':
                print("Exiting program...")
                break
            elif choice == '1':
                if not banner_printed_local:
                    print_local_banner()
                    banner_printed_local = True
                print_menu()
                choice_local = input("Select an option (1-7): ")

                if choice_local == '8':
                    banner_printed_local = False
                    break
                elif choice_local in {'1', '2', '3', '4', '5', '6', '7'}:
                    info_functions = {
                        '1': print_system_info,
                        '2': print_cpu_info,
                        '3': print_memory_info,
                        '4': print_processes,
                        '5': print_network_info,
                        '6': print_disk_info,
                        '7': get_full_analysis_html,
                    }

                    info_func = info_functions.get(choice_local)
                    if info_func:
                        info_func()
                    else:
                        print("Invalid choice. Please select a number from 1 to 7.")
                else:
                    print("Invalid choice. Please select a number from 1 to 7.")
            elif choice == '2':
                if not banner_printed_remote:
                    print_external_banner()
                    banner_printed_remote = True
                print_external_menu()
                choice_locall = input("Select an option (1-6): ")

                if choice_locall == '6':
                    banner_printed_remote = False
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


