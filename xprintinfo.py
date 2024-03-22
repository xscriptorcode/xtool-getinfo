from xgetinfo import *

def print_system_info():
    info_dict = get_system_info()
    print_info(info_dict)

def print_cpu_info():
    info_dict = get_cpu_info()
    print_info(info_dict)

def print_memory_info():
    info_dict = get_memory_info()
    print_info(info_dict)

def print_processes():
    info_dict = get_processes()
    print_info(info_dict)

def print_network_info():
    info_dict = get_network_info()
    print_info(info_dict)

def print_disk_info():
    info_dict = get_disk_info()
    print_info(info_dict)

def print_info(info_dict):
    for key, value in info_dict.items():
        print(f"{key}: {value}")
