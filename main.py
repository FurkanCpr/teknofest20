import sys
from base_uav import BaseUAV 
import threading
from area_scanner import AreaScanner
from sample_uav import SampleUAV

default_ip = '127.0.0.1'
default_port = 5672

def get_uav_id():
    uav_number = sys.argv[1]
    try:
        uav_number = int(uav_number)
        print("uav_number : ", uav_number)
    except ValueError:
        print('ERROR: Invalid UAV id:' + sys.argv[1])
        sys.exit(1)
    return str(uav_number)

def get_ip():
    if len(sys.argv) > 2:
        return sys.argv[2]
    else:
        return default_ip

def get_port():
    if len(sys.argv) > 3:
        port_num = sys.argv[3]
        try:
            port_num = int(port_num)
        except ValueError:
            print('ERROR: invalid port number:' + sys.argv[3])
            sys.exit(2)

        return port_num
    else:
        return default_port

def uav_thread_func(uav_id, ip, port, uav_number):
    sample_object = SampleUAV(uav_id, ip, port, uav_number)
    sample_object.start_listening()

def uav_controller_func(uav_number, ip, port):
    area_scan_object = AreaScanner(uav_number, ip, port)
    area_scan_object.start_listening()

if __name__ == '__main__':
    import math
    uav_number = get_uav_id()
    ip = get_ip()
    port = get_port()
    step = int(math.floor(int(uav_number) / 2))
    i = 0
    uav_id = 0

    while i < step: 
        _ = threading.Thread(target=uav_thread_func, args=(str(uav_id), ip, port, int(uav_number)), name="UAV_{}_Thread".format(uav_id)).start()
        __ = threading.Thread(target=uav_thread_func, args=(str((uav_id + 4)), ip, port, int(uav_number)), name="UAV_{}_Thread".format(str(uav_id + 4))).start()       
        i += 1
        uav_id += 1
    eight_uav = threading.Thread(target=uav_thread_func, args=("8", ip, port, int(uav_number)), name="UAV_{}_Thread".format("8")).start()   
    print("Thread count : ", threading.enumerate())    