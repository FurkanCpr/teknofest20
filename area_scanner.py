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
        self.comm = RabbitCommunication(host=ip, port=port)
        self.cmd_queue_name = 'uav_command_queue_' + str(uav_number)
        self.comm.register_to_queue('uav_imu_queue_'+ str(uav_number), self.uav_msg_callback)

    def start_listening(self):
        self.comm.start_listening()

    def uav_msg_callback(self, uav_msg):
        self.uav_msg = uav_msg  
        self.area_scan(self.x_list, self.y_list)

    def area_scan(self, x_list, y_list):
        # hesaplarin yapildigi kisim
        self.location_list = []

        for i in range(0, self.uav_number):
            self.distance_list.append(float(str(self.location_list[i][0]) + "." + str(self.location_list[i][1])))
            self.location_dict[i] = self.distance_list[i]

        self.distance_list = sorted(self.distance_list)
        print("asd", self.location_dict)
        #print(self.x_list)
        #print(self.y_list)
        #print("Hommage")
        """
        - are_list hesaplari
        - belirtilen araliktan ( communication range ) kucuk alanda
        bulunan ihalarin listesi
        """
        

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

    def read_list(self, uav_id, formation):
        # kendi id'si ile birlikte cagrilan iha'nin
        # hangi sinifta oldugunu belirleyip o ihaya gore return
        # sinif numarasi dondurecek
        # [[x,y], [x,y]]
        
        for i in range(0, self.uav_number):
            self.distance_list.append(float(str(self.location_list[i][0]) + "." + str(self.location_list[i][1])))
            self.location_dict[i] = self.distance_list[i]    

        self.distance_list = sorted(self.distance_list)
       
        uav_id = self.distance_list.index(self.location_dict[uav_id])
        
        if formation == "arrow":
            if uav_id % 2 == 0:
                sinif = uav_id / 2
            elif uav_id % 2 == 1:
                sinif = (uav_id + 1) / 2
        else:
            sinif = math.ceil(uav_id / 4)
        
        return sinif
        