from rabbit_communication import RabbitCommunication
import time
import threading
from datetime import datetime
import math

class AreaScanner(object):
    def __init__(self, uav_number, ip, port):
        self.distance_threshold = 25
        self.location_list = []
        self.location_dict = {}
        self.distance_list = [] # bu return edilecek liste 
        # tarafindan cagrilan ihanin id numarasina gore
        # etrafinda bulunan ihalar ile kendi mesafesinin
        # threshold degerinden kucuk olup olmadigina bakmak icin 
        self.uav_number = int(uav_number)
        self.dummy = True
        self.comm = RabbitCommunication(host=ip, port=port)
        self.cmd_queue_name = 'uav_command_queue_' + str(uav_number)
        self.comm.register_to_queue('uav_imu_queue_'+ str(uav_number), self.uav_msg_callback)

    def start_listening(self):
        self.comm.start_listening()

    def uav_msg_callback(self, uav_msg):
        self.uav_msg = uav_msg  
        self.area_scan()

    def area_scan(self):
        # hesaplarin yapildigi kisim
        pass

    def nearby_uavs(self, uav_id):
        # UAV 3 tarafindan cagrilmis ve alanda 4-5-6-3 olmus olsun.
        # bu fonksyion return olarak 4-5-6 verecek
        return self.uav_list_to_communicate

    def danger(self, uav_id):
        # IHA'lardan cagrilacak fonksiyon,
        # uav_id ye gore belirlenen threshold degeri icinde 
        # iha olup olmadigina bakicak.
        # var ise avoidance yapilacak iha nin koordinatlarini ve 
        # true dondurecek
        # return [x,y], True
        pass

    def read(self, uav_id, formation):
        # kendi id'si ile birlikte cagrilan iha'nin
        # hangi sinifta oldugunu belirleyip o ihaya gore return
        # sinif numarasi dondurecek
        pass
    
        