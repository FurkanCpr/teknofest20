from rabbit_communication import RabbitCommunication
import time
import threading
from datetime import datetime

class AreaScanner(object):
    def __init__(self, uav_number, ip, port):
        self.x_list = []
        self.y_list = []
        self.uav_number = uav_number
        self.comm = RabbitCommunication(host=ip, port=port)
        self.cmd_queue_name = 'uav_command_queue_' + str(uav_number)
        self.comm.register_to_queue('uav_imu_queue_'+ str(uav_number), self.uav_msg_callback)

    def start_listening_area(self):
        self.comm.start_listening()

    def uav_msg_callback(self, uav_msg):
        self.uav_msg = uav_msg  

    def start(self):
        while True:
            # print("Area Scanner")
            time.sleep(.5)
            
            """
            for i in range(0, self.uav_number)
                x_list.append(self.uav_msg['uav_link'][i]['uav_'+str(i)]['location'][0])
                y_list.append(self.uav_msg['uav_link'][i]['uav_'+str(i)]['location'][1])
            """