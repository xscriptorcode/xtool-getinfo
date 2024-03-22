import psutil
import platform

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

def get_disk_info():
    disk_partitions = psutil.disk_partitions()
    disk_usage = psutil.disk_usage('/')
    disk_io_counters = psutil.disk_io_counters()

    disk_info = {
        "Disk Partitions": [],
        "Disk Usage": {
            "Total Space (GB)": disk_usage.total / (1024 ** 3),
            "Used Space (GB)": disk_usage.used / (1024 ** 3),
            "Free Space (GB)": disk_usage.free / (1024 ** 3),
            "Percentage Used": disk_usage.percent,
        },
        "Disk I/O Counters": {
            "Read Count": disk_io_counters.read_count,
            "Write Count": disk_io_counters.write_count,
            "Read Bytes": disk_io_counters.read_bytes,
            "Write Bytes": disk_io_counters.write_bytes,
        }
    }

    for partition in sorted(disk_partitions, key=lambda x: x.mountpoint):
        usage = psutil.disk_usage(partition.mountpoint)
        partition_info = {
            "Mountpoint": partition.mountpoint,
            "File System Type": partition.fstype,
            "Total Space (GB)": usage.total / (1024 ** 3),
            "Used Space (GB)": usage.used / (1024 ** 3),
            "Free Space (GB)": usage.free / (1024 ** 3),
            "Percentage Used": usage.percent,
        }
        disk_info["Disk Partitions"].append(partition_info)

    return disk_info
