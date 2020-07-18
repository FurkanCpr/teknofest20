from base_uav import BaseUAV
import math
import random
import util

class SampleUAV(BaseUAV): # child
    def initialize(self):
        self.target_position = None
        self.sinif = None
        self.hazirlik = True

    def act(self, uav_msg, uav_id, formation): 
        # 1) Ucus modu belirlenmesi (Dispatch, Hazirlik, GPS noise)
        # 2) IHA'larin sinif hesabi
        # 3) Gelen mesaj okunuyor

        self.uav_msg = uav_msg
        self.lider_info = [self.uav_msg['uav_guide']['location'][0], # x koordinat
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

        if self.sinif == None:
            print("Sinif hesaplaniyor")
            if formation == "arrow":
                if uav_id % 2 == 0:
                    self.sinif = uav_id / 2
                elif uav_id % 2 == 1:
                    self.sinif = (uav_id + 1) / 2
            else:
                self.sinif = math.ceil(uav_id / 4)
                
        if self.dispatch == False:
            self.hazirlik = False
            print("Dispatch False, Formasyon devam")  
            if self.uav_msg['uav_guide']['gps_noise_flag']:    
                self.exp_point_calc(uav_id, formation)

            if formation == "arrow":  
                print("Format Arrow")
                self.exp_point_calc(uav_id, formation) # istenen noktada olup olmadigini belirler + o noktaya gitmek icin move_to_target calisir

            elif self.uav_msg['uav_formation']['type'] == "prism":
                print("Prism Formasyon")
                self.exp_point_calc(uav_id, formation)

        elif self.dispatch == True and self.hazirlik == True:
            print("Hazirlik Kismi")
            self.exp_point_calc(uav_id, formation)

        elif self.dispatch == True and self.hazirlik == False:
            print("Dispatch True, Denied Zone ve Search Algoritmasi")
            # search_algorithm()
            pass

    def search_algorithm(self, uav_id):
        pass

    def get_uav_information(self):
        # area_scanner bilgisi buraya gelecek
        pass   
    
    def exp_point_calc(self, uav_id, formation):
        # 1)Formasyon, GPS noise ve ucus moduna gore IHA kendi bulunmasi gereken noktayi hesaplar
        print("Get location kismi")
        if self.hazirlik:
            if formation == "arrow": 
                """
                u_b = self.uav_msg['uav_formation']['u_b']
                u_k = self.uav_msg['uav_formation']['u_k']

                exp_z = self.lider_info[2]
                if self.pose[3] == -90:
                    print("Lider ile ayni yone bakiliyor")
                    exp_x = (self.lider_info[0]) + (math.sqrt(abs(((self.sinif * u_b)**2 - abs(self.lider_info[1] - self.pose[1])**2)) + u_k))
                    diff_y = abs(self.lider_info[1] - self.pose[1]) 
                    if uav_id == 0:
                        exp_y = self.lider_info[1]                 
                    else:             
                        if (uav_id % 2 == 0):
                            exp_y = diff_y + self.lider_info[1]
                        elif (uav_id % 2 == 1):
                            exp_y = self.lider_info[1] - diff_y
                """
                # self.target_position = [exp_x, exp_y, exp_z]
                self.move(self.hazirlik, self.dispatch, self.gps_noise_flag, uav_id)

            elif formation == "prism":
                pass

        if formation == "arrow":
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

            if uav_id == 0:
                exp_y = y_lider
            else:             
                if (uav_id % 2 == 0):    
                    exp_y = diff_y + y_lider
                elif (uav_id % 2 == 1):
                    exp_y = y_lider - diff_y

            self.target_position = [exp_x, exp_y, exp_z]
            self.move(self.hazirlik, self.dispatch, self.gps_noise_flag, uav_id)

        elif formation == "prism":
            u_b = self.uav_msg['uav_formation']['u_b']
            u_k = self.uav_msg['uav_formation']['u_k']
            a_k = self.uav_msg['uav_formation']['a_k']
            y_lider = self.lider_info[1]
            y_iha = self.pose[1]

            exp_x = self.lider_info[0] + (u_k + (self.sinif * u_b))
            

            if uav_id == 0:
                exp_z = self.lider_info[2]
                exp_x = self.lider_info[0] + (u_k + (self.sinif * u_b))
                exp_y = self.lider_info[1]
                self.target_position = [exp_x, exp_y, exp_z]
            
            else:
                exp_x = self.lider_info[0] + (u_k + (self.sinif * u_b))

                if (uav_id % 4 == 1) or (uav_id % 4 == 2): 
                    exp_z = self.lider_info[2] + (u_b / 2)
                elif (uav_id % 4 == 0) or (uav_id % 4 == 3):
                    exp_z = self.lider_info[2] - (u_b / 2)
                if uav_id % 2 == 0:
                    exp_y = self.lider_info[1] + (u_b / 2)
                elif uav_id % 2 == 1:
                    exp_y = self.lider_info[1] - (u_b / 2)

                self.target_position = [exp_x, exp_y, exp_z]  

            self.move(self.hazirlik, self.dispatch, self.gps_noise_flag, uav_id)
        
    def move(self, hazirlik, dispatch, gps_noise_flag, uav_id):
        # 1)Belirlenen hedefe varilip varilmadigini kontrol eder.
        thresh = 3.0 
        if self.target_position is None:
            print("Baslangic")
        else:
            if dispatch and hazirlik:
                print("Hazirlik")
                if uav_id == 0:
                    self.send_move_cmd(0, 0, self.lider_info[3], self.lider_info[2]*3) # x_speed, y_speed, heading, altitude
                else:
                    self.send_move_cmd(0, 0, self.lider_info[3], self.lider_info[2])
                    
            if not dispatch:
                print("Formasyon")
                dist = util.dist(self.target_position, self.pose)
                if dist < thresh: # hedefe varildi
                    x_speed = self.lider_info[5]
                    self.send_move_cmd(x_speed, 0, self.lider_info[3], self.target_position[2])
                
                else: # Hedefe Varilmadi    
                    dist = util.dist(self.target_position, self.pose)
                    target_angle = math.atan2(self.target_position[0]-self.pose[0], -(self.target_position[1]-self.pose[1]))
                    target_angle = math.degrees(target_angle)
                    x_speed = self.lider_info[5]

                    if dist < 50:
                        x_speed = dist*0.25
                    elif dist > 50:
                        x_speed = dist*1.25
                    
                    self.send_move_cmd(x_speed, 0, target_angle, self.target_position[2])

            if gps_noise_flag:
                print("Bozuk GPS alani")

            if dispatch and hazirlik == False:
                print("search algoritmasi")
                self.search_algorithm(uav_id)


