from rabbit_communication import RabbitCommunication
from area_scanner import AreaScanner

class BaseUAV(object): # parent
    def __init__(self, uav_id, ip, port):
        self.uav_id = uav_id
        self.comm = RabbitCommunication(host=ip, port=port)
        self.params = self.comm.send_request('scenario_parameters')
        self.initialize()
        self.cmd_queue_name = 'uav_command_queue_' + uav_id
        self.comm.register_to_queue('uav_imu_queue_'+ uav_id, self.uav_msg_callback)

    def start_listening(self):
        self.comm.start_listening()

    def uav_msg_callback(self, uav_msg): 
        self.uav_msg = uav_msg
        formation = self.uav_msg['uav_formation']['type']
        self.act(self.uav_msg, int(self.uav_id), formation) # son True Hazirlik anlamina geliyor

    def send_move_cmd(self, x_speed, y_speed, heading, altitude, task='D'):
        cmd = {"x_speed": x_speed, "y_speed": y_speed, "altitude": altitude, "heading": heading, "task": task}
        self.comm.send(self.cmd_queue_name, cmd)

    def initialize(self):
        # bu metod asil takim kodu tarafindan ezilecek
        print("BASE init")
        pass

    def act(self):
        print("ACT in BASE")
        # bu metod asil takim kodu tarafindan ezilecek
        pass