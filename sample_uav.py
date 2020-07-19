from base_uav import BaseUAV
from area_scanner import AreaScanner

import math
import random
import util

class SampleUAV(BaseUAV): # child
    def initialize(self, uav_id, ip, port, uav_number):
        self.uav_id = uav_id
        self.sinif = None
        self.ip = ip
        self.port = port
        self.uav_number = uav_number
        self.target_position = None
        self.hazirlik = True
        self.are_scanner_object = AreaScanner(self.uav_number, self.ip, self.port)
        
    def act(self, uav_msg, formation): 
        # 1) Ucus modu belirlenmesi (Dispatch, Hazirlik, GPS noise)
        # 2) IHA'larin sinif hesabi
        # 3) Gelen mesaj okunuyor
        self.formation = formation
        self.uav_msg = uav_msg
        self.lider_info =[self.uav_msg['uav_guide']['location'][0], # x koordinat
                          self.uav_msg['uav_guide']['location'][1], # y koordinat
                          self.uav_msg['uav_guide']['altitude'],
                          self.uav_msg['uav_guide']['heading'],
                          self.uav_msg['uav_guide']['speed']['y'], # y deki hiz
                          self.uav_msg['uav_guide']['speed']['x'], # x deki hiz
                          self.uav_msg['uav_guide']['gps_noise_flag']]
        
        self.pose = [self.uav_msg['active_uav']['location'][0],
                     self.uav_msg['active_uav']['location'][1],
                     self.uav_msg['active_uav']['altitude'],
                     self.uav_msg['active_uav']['heading']]
        
        self.gps_noise_flag = self.uav_msg['uav_guide']['gps_noise_flag']
        self.dispatch = self.uav_msg['uav_guide']['dispatch']
        
        if not self.dispatch:
            self.hazirlik = False # Hazirlik durumu bittiginde ( dispatch False ) hazirlik False olacak.

        if self.dispatch == False:
            self.hazirlik = False
            print("Dispatch False, Formasyon devam")  
            if self.uav_msg['uav_guide']['gps_noise_flag']:    
                self.exp_point_calc()

            if self.formation == "arrow":  
                print("Format Arrow")
                self.exp_point_calc() # istenen noktada olup olmadigini belirler + o noktaya gitmek icin move_to_target calisir

            elif self.uav_msg['uav_formation']['type'] == "prism":
                print("Prism Formasyon")
                self.exp_point_calc()

        elif self.dispatch == True and self.hazirlik == True:
            self.preparing()
            # self.exp_point_calc()

        elif self.dispatch == True and self.hazirlik == False:
            print("Dispatch True, Denied Zone ve Search Algoritmasi")
            # search_algorithm()
            pass

    def search_algorithm(self):
        pass

    def preparing(self):
        # 1)lidere en yakin olan ihalar listenelecek + 
        # 2)Bu ihalar 0'dan uav_number'a kadar sayilara atanacak
        # 3)Sinif hesabi yapılacak
        # 4)gidilecek nokta belirlenecek +
        # 5)hareket +
        print("Eski UAV ID : ", self.uav_id)
        new_uav_id = self.are_scanner_object.read_list(self.uav_id, self.formation)
        print("Yeni UAV ID : ", new_uav_id)
        # yeni sinif degerleri atanacak + 
        # self.sinif = new_uav_id
        if self.sinif:
            if self.formation == "arrow": 
                if not self.target_position:
                    u_b = self.uav_msg['uav_formation']['u_b']
                    u_k = self.uav_msg['uav_formation']['u_k']
                    a_b = self.uav_msg['uav_formation']['a_b']
                    if not self.uav_id == 0:
                        if self.uav_id % 2 == 0:
                            exp_y = self.lider_info[1] + self.sinif*(u_b*math.sin(a_b))
                        else:
                            exp_y = self.lider_info[1] - self.sinif*(u_b*math.sin(a_b))
                        exp_x = self.lider_info[0] + (u_k + (self.sinif*(u_b*math.cos(a_b))))
                    else: # uav_id 0 iken
                        exp_x = self.lider_info[0] + u_k
                        exp_y = self.lider_info[1]

                    self.target_position = [exp_x, exp_y, self.lider_info[2]]
                
                thresh = 70
                dist = util.dist(self.target_position, self.pose)
                x_speed = self.lider_info[5]
                if dist < thresh: 
                    x_speed = self.lider_info[5]
                    self.send_move_cmd(x_speed, 0, self.lider_info[3], self.target_position[2])
                
                else:    
                    dist = util.dist(self.target_position, self.pose)
                    target_angle = math.atan2(self.target_position[0]-self.pose[0], -(self.target_position[1]-self.pose[1]))
                    target_angle = math.degrees(target_angle)
                    
                    if dist > 100:
                        x_speed = x_speed*1.5
                    self.send_move_cmd(x_speed, 0, target_angle, self.target_position[2])
            elif self.formation == "prism":
                pass
        else:
            print("Sinif degeri atanmadi")

    def formasyon(self):
        print("Formasyon")
        thresh = 70
        dist = util.dist(self.target_position, self.pose)
        x_speed = self.lider_info[5]
        if dist < thresh: 
            x_speed = self.lider_info[5]
            self.send_move_cmd(x_speed, 0, self.lider_info[3], self.target_position[2])
        
        else:    
            dist = util.dist(self.target_position, self.pose)
            target_angle = math.atan2(self.target_position[0]-self.pose[0], -(self.target_position[1]-self.pose[1]))
            target_angle = math.degrees(target_angle)
            
            if dist > 100:
                x_speed = x_speed*1.5
            self.send_move_cmd(x_speed, 0, target_angle, self.target_position[2])

    def area_scanner(self):
        # kendi uav id'me gore en yakinimdaki iha ile mesafem hesaplaniyor
        # bu mesafe 25 'ten kucuk ise ilk olarak o ihadan kacilacak
        """
        near_uav_coordinates, danger_state = self.are_scanner_object.danger(self.uav_id)
        if danger_state:
            self.avoidance(near_uav_coordinates)
        self.communication()
        """
        pass
        
    def avoidance(self, near_uav_coordinates):    
        # alanin icinde iha var ise o ihannin konumundan uzak bir konuma gitme komutu uretecek
        # carpisma olmamsi icin bir hareket outputu uretir
        # hesap icin near_uav_coordinates kullanilacak, bu noktalardan uzaga gidilecek
        pass 

    def formation_setup_after_GPS(self, location_points):
        # GPS bozuklugundan sonra 
        # location points alanda bulunan ihalarin konumlaridir
        # bu konumlara gore self.formation_setup_after_GPS fonksiyonu 
        pass

    def communication(self):
        # alandaki ihalarin bilgilerini alir
        self.uav_list_to_communicate = self.are_scanner_object.nearby_uavs(self.uav_id)
        # kendi iha noma gore return yakindaki_ihalarin_bilgileri
        # daha sonra bu iha_ nolari ila haberlesme icin istek atilacak
        pass
    
    def exp_point_calc(self):
        # 1)Formasyon, GPS noise ve ucus moduna gore IHA kendi bulunmasi gereken noktayi hesaplar
        if not self.target_position is None:
            self.area_scanner() # communication ve

        if self.formation == "arrow":
            if self.area_scanner():
                self.avoidance()
                pass

            u_b = self.uav_msg['uav_formation']['u_b']
            a_b = self.uav_msg['uav_formation']['a_b']
            u_k = self.uav_msg['uav_formation']['u_k']
            a_k = self.uav_msg['uav_formation']['a_k']

            y_lider = self.lider_info[1]
            y_iha = self.pose[1]
            z_lider = self.lider_info[2]

            exp_z = z_lider 
            exp_x = (self.lider_info[0]) + (math.sqrt(abs(((self.sinif * u_b)**2 - abs(y_lider - y_iha)**2)) + u_k))
            diff_y = abs(y_lider - y_iha)

            if self.uav_id == 0:
                exp_y = y_lider
            else:             
                if (self.uav_id % 2 == 0):    
                    exp_y = diff_y + y_lider
                elif (self.uav_id % 2 == 1):
                    exp_y = y_lider - diff_y

            self.target_position = [exp_x, exp_y, exp_z]
            self.move(self.hazirlik, self.dispatch, self.gps_noise_flag)

        elif self.formation == "prism":
            if self.area_scanner():
                self.avoidance()
                pass

            u_b = self.uav_msg['uav_formation']['u_b']
            u_k = self.uav_msg['uav_formation']['u_k']
            a_k = self.uav_msg['uav_formation']['a_k']
            y_lider = self.lider_info[1]
            y_iha = self.pose[1]
            exp_x = self.lider_info[0] + (u_k + (self.sinif * u_b))

            if self.uav_id == 0:
                exp_z = self.lider_info[2]
                exp_x = self.lider_info[0] + (u_k + (self.sinif * u_b))
                exp_y = self.lider_info[1]
                self.target_position = [exp_x, exp_y, exp_z]
            
            else:
                exp_x = self.lider_info[0] + (u_k + (self.sinif * u_b))

                if (self.uav_id % 4 == 1) or (self.uav_id % 4 == 2): 
                    exp_z = self.lider_info[2] + (u_b / 2)
                elif (self.uav_id % 4 == 0) or (self.uav_id % 4 == 3):
                    exp_z = self.lider_info[2] - (u_b / 2)
                if self.uav_id % 2 == 0:
                    exp_y = self.lider_info[1] + (u_b / 2)
                elif self.uav_id % 2 == 1:
                    exp_y = self.lider_info[1] - (u_b / 2)

                self.target_position = [exp_x, exp_y, exp_z]  
                self.move(self.hazirlik, self.dispatch, self.gps_noise_flag)
        
    def move(self, hazirlik, dispatch, gps_noise_flag):
        if self.target_position is None:
            print("Baslangic")
        else:
            if dispatch and hazirlik:
                print("Hazirlik")
                self.preparing()

            if not dispatch:
                print("Formasyon")
                self.formasyon()

            if gps_noise_flag:
                print("Bozuk GPS alani")
                self.communication()
                # self.self.formation_setup_after_GPS()

            if dispatch and hazirlik == False:
                print("search algoritmasi")
                self.search_algorithm()


