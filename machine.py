from finsudp import *

class Machine():
    def __init__(self):
        self.ip = ""
        self.port = ""
        self.my_fins_address = "0.1.0"
        self.to_fins_address = "0.0.0"
        self.name = ""
        self.recieve_address = []
        self.send_complete_address = ""
        self.recieve_trigger_address = ""
        self.recieve_data = []
        self.recieve_bit_size = 0
        
    def get_data_from_adrress(self):
        finsudp = fins(self.ip, self.my_fins_address, self.to_fins_address)
        for i, adr in enumerate(self.recieve_address):
            self.recieve_data.append(finsudp.selectExchangeFunc(adr, self.recieve_bit_size[i])[0])
        print(self.recieve_data)

    def get_status(self):
        status_num = 0
        finsudp = fins(self.ip, self.my_fins_address, self.to_fins_address)
        data = finsudp.selectExchangeFunc(self.recieve_trigger_address, "INT16")
        if data:
            status_num = data[0]
        return int(status_num)
    
    def write_complete(self):
        write_data = 1
        finsudp = fins(self.ip, self.my_fins_address, self.to_fins_address)
        status_num = finsudp.write(self.send_complete_address, write_data.to_bytes(2,'big'))
