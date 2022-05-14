import os
import bluetooth
from time import sleep

class BT():
    def __init__(self):
        
        os.system("bluetoothctl discoverable on")
        
        self.mac_rpi0_samu = "B8:27:EB:48:52:95"    #RPI0
        self.mac_rpi3_samu = "B8:27:EB:10:0D:19"    #RPI1
        self.mac_rpi4_samu = "DC:A6:32:6B:3A:AB"    #RPI2
        
        self.mac_rpi4_zeti = "DC:A6:32:78:BC:C7"    #RPI3
        self.mac_rpi4_mate = "DC:A6:32:25:D2:CC"    #RPI4
        
    def receive(self):
        server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
          
        port = 1
        server_sock.bind(("",port))
        server_sock.listen(1)
          
        client_sock,address = server_sock.accept()
          
        data = client_sock.recv(1024)
          
        client_sock.close()
        server_sock.close()
          
        return address[0], data;
      
    def send(self, targetBluetoothMacAddress, message):
        try:
            sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            sock.connect((targetBluetoothMacAddress, 1))
            sock.send(message)
            sock.close()
            print("Message " + str(message) + " sent to " + str(targetBluetoothMacAddress))
            return True
        except:
            print("Failed to send message " + str(message) + " to " + str(targetBluetoothMacAddress))
            return False
        
    def sync(self):
        return self.receive()

    def start(self):
        self.send(self.mac_rpi0_samu, "go")
        self.send(self.mac_rpi3_samu, "go")
