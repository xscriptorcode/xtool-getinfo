import nmap
import networkx as nx
import matplotlib.pyplot as plt


def scan_remote_system(ip_address):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_address, arguments='-O')  # Utiliza '-O' para la detección del sistema operativo

    for host in nm.all_hosts():
        print(f"IP Address: {host}")  # Imprime la dirección IP del dispositivo

        host_info = nm[host]
        if 'osclass' in host_info:
            print("* Operating System Information *")
            for osclass in host_info.get('osclass', []):
                print(f"Vendor: {osclass['vendor']}, OS Family: {osclass['osfamily']}, Type: {osclass['type']}")
        else:
            print("No OS information available.")

        if 'osmatch' in host_info:
            print("* Detected Operating System Matches *")
            for match in host_info['osmatch']:
                print(f"Name: {match['name']}, Accuracy: {match['accuracy']}%, Line: {match['line']}")
        else:
            print("No OS matches found.")
        print()


def scan_local_network(subnet):
    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments='-sn')  # Utiliza '-sn' para el escaneo de hosts en la red

    print("Dispositivos encontrados en la red:")
    for host in nm.all_hosts():
        host_info = nm[host]
        if 'hostnames' in host_info:
            hostname = host_info['hostnames'][0]['name']
        else:
            hostname = "Unknown"

        if 'addresses' in host_info:
            ip_address = host_info['addresses'].get('ipv4', 'Unknown')
            mac_address = host_info['addresses'].get('mac', 'Unknown')
        else:
            ip_address = "Unknown"
            mac_address = "Unknown"

        print(f"IP: {ip_address}, Hostname: {hostname}, MAC: {mac_address}")

def scan_network_devices():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-sn')  # Escanea toda la subred para encontrar dispositivos

    devices = []

    for host in nm.all_hosts():
        device_info = {
            'ip': host,
            'hostname': nm[host]['hostnames'][0]['name'] if 'hostnames' in nm[host] else 'Unknown',
            'mac': nm[host]['addresses']['mac'] if 'mac' in nm[host]['addresses'] else 'Unknown',  # Dirección MAC del dispositivo
            'vendor': nm[host]['vendor'][0] if 'vendor' in nm[host] and isinstance(nm[host]['vendor'], list) else 'Unknown'  # Fabricante del dispositivo
        }
        devices.append(device_info)

    return devices

def scan_for_vulnerabilities(ip_address):
    nm = nmap.PortScanner()
    nm.scan(ip_address, arguments='-sV -p 1-1000')  # Escanea los puertos del 1 al 1000 con detección de servicios
    
    for host in nm.all_hosts():
        print(f"Host : {host} ({nm[host].hostname()})")
        print("State : %s" % nm[host].state())
        
        for proto in nm[host].all_protocols():
            print("Protocol : %s" % proto)
            
            port_info = nm[host][proto].items()
            for port, port_info in port_info:
                print(f"Port : {port} \tState : {port_info['state']} \tName : {port_info['name']} \tProduct : {port_info['product']} \tVersion : {port_info['version']}")


def create_network_map(ip_address, output_file):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_address, arguments='-sn')
    
    G = nx.Graph()
    
    for host in nm.all_hosts():
        G.add_node(host, label=nm[host].hostname())
    
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                G.add_edge(host, f"{host}:{port}")
    
    pos = nx.spring_layout(G)
    
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.savefig(output_file, format='jpg')
    plt.close()

    print(f"Map saved as: {output_file} in the current directory.")
