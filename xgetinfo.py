import psutil
import platform
import os

def get_system_info():
    return {
        "Operating System": platform.system(),
        "Node Name": platform.node(),
        "Kernel Version": platform.release(),
        "Processor Architecture": platform.machine(),
        "Boot Time": psutil.boot_time(),
    }

def get_cpu_info():
    return {
        "CPU Usage (%)": psutil.cpu_percent(interval=1, percpu=True),
        "Number of Cores": psutil.cpu_count(logical=False),
        "CPU Frequencies (MHz)": [freq.current for freq in psutil.cpu_freq(percpu=True)],
    }

def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        "Physical Memory Usage (MB)": memory.used / (1024 * 1024),
        "Swap Memory Usage (MB)": psutil.swap_memory().used / (1024 * 1024),
        "Available Memory (MB)": memory.available / (1024 * 1024),
    }

def get_processes():
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info']):
        try:
            process_info = {
                "Process ID": process.info['pid'],
                "Name": process.info['name'],
                "Status": process.info['status'],
                "CPU Usage (%)": process.info['cpu_percent'],
                "Memory Usage (MB)": process.info['memory_info'].rss / (1024 * 1024),
            }
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def get_network_info():
    return {
        "Network Connections": psutil.net_connections(),
        "Network Interfaces": psutil.net_if_addrs(),
    }

def get_disk_info() -> dict:
    disk_partitions = sorted(psutil.disk_partitions(), key=lambda x: x.mountpoint)
    disk_usage = psutil.disk_usage('/')
    disk_io_counters = psutil.disk_io_counters()

    disk_info = {}

    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info[partition.mountpoint] = {
            "Total (GB)": usage.total / (1024 ** 3),
            "Used (GB)": usage.used / (1024 ** 3),
            "Free (GB)": usage.free / (1024 ** 3),
            "FSType": partition.fstype,
        }

    disk_info["/"] = {
        "Total (GB)": disk_usage.total / (1024 ** 3),
        "Used (GB)": disk_usage.used / (1024 ** 3),
        "Free (GB)": disk_usage.free / (1024 ** 3),
        "Disk I/O Counters": {
            "Read Bytes": disk_io_counters.read_bytes,
            "Write Bytes": disk_io_counters.write_bytes,
        }
    }

    return disk_info


def get_full_analysis_html():
    # create the analysys directory
    analysis_dir = 'analysis'
    if not os.path.exists(analysis_dir):
        os.mkdir(analysis_dir)
    # create the html file name
    html_file = 'analysis.html'
    i = 1
    while os.path.exists(os.path.join(analysis_dir, html_file)):
        html_file = f'analysis({i}).html'
        i += 1
    # add the data to the file.
    with open(os.path.join(analysis_dir, html_file), 'w') as f:
        f.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>System Analysis</title>\n<style>\n.collapsible {background-color: #777; color: white; cursor: pointer; padding: 18px; width: 100%; border: none; text-align: left; outline: none; font-size: 15px;}\n.active, .collapsible:hover {background-color: #555;}\n.collapsible:after {content: "+"; font-size: 13px; color: white; float: right; margin-left: 5px;}\n.active:after {content: "-";}\n.content {padding: 0 18px; max-height: 0; overflow: hidden; transition: max-height 0.2s ease-out;}\n</style>\n</head>\n<body>')
        f.write('<h1>System</h1>\n<button class="collapsible">System</button>\n<div class="content"><ul>')
        for key, value in get_system_info().items():
            f.write(f'<li><strong>{key}</strong>: {value}</li>\n')
        f.write('</ul></div>\n\n<h1>CPU</h1>\n<button class="collapsible">CPU</button>\n<div class="content"><ul>')
        for key, value in get_cpu_info().items():
            f.write(f'<li><strong>{key}</strong>: {value}</li>\n')
        f.write('</ul></div>\n\n<h1>Memory</h1>\n<button class="collapsible">Memory</button>\n<div class="content"><ul>')
        for key, value in get_memory_info().items():
            f.write(f'<li><strong>{key}</strong>: {value}</li>\n')
        f.write('</ul></div>\n\n<h1>Processes</h1>\n<button class="collapsible">Processes</button>\n<div class="content"><ul>')
        for process in get_processes():
            f.write('<li>')
            for key, value in process.items():
                f.write(f'<strong>{key}</strong>: {value}<br>')
            f.write('</li>\n')
        f.write('</ul></div>\n\n<h1>Network Connections</h1>\n<button class="collapsible">Network</button>\n<div class="content"><ul>')
        for key, value in get_network_info().items():
            if key == "Network Connections":
                for connection in value:
                    f.write(f'<li>Process ID: {connection.pid}<br>Local Address: {connection.laddr}<br>Remote Address: {connection.raddr}<br>Status: {connection.status}</li>\n')
            else:
                f.write(f'<li><strong>{key}</strong>: {value}</li>\n')
        f.write('</ul></div>\n\n<h1>Disk Information</h1>\n<button class="collapsible">Disk</button>\n<div class="content"><ul>')
        for key, value in get_disk_info().items():
            f.write(f'<li><strong>{key}</strong>')
            for key2, value2 in value.items():
                f.write(f'<strong>{key2}</strong>: {value2}')
            f.write('</li>\n')
        f.write('</ul></div>\n</body>\n</html>\n<script>\nvar coll = document.getElementsByClassName("collapsible");\nvar i;\n\nfor (i = 0; i < coll.length; i++) {\n  coll[i].addEventListener("click", function() {\n    this.classList.toggle("active");\n    var content = this.nextElementSibling;\n    if (content.style.maxHeight){\n      content.style.maxHeight = null;\n    } else {\n      content.style.maxHeight = content.scrollHeight + "px";\n    } \n  });\n}\n</script>')
        print("Successfully created the full analysis HTML file.\nOpen it with your favorite web browser.\n")




