from bluepy import btle
from dataclasses import dataclass

@dataclass
class Result:
    temperature: float
    humidity: int
    voltage: float
    battery: int = 0

result = Result(0,0,0,0)
class Measure(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)
    
    def handleNotification(self, cHandle, data):
        try:
            global result
            temp=int.from_bytes(data[0:2],byteorder='little',signed=True)/100
            humidity=int.from_bytes(data[2:3],byteorder='little')
            voltage=int.from_bytes(data[3:5],byteorder='little') / 1000
            battery = round((voltage - 2) / (3.261 - 2) * 100, 2)
            result.temperature = temp
            result.humidity = humidity
            result.voltage = voltage
            result.battery = battery
            print(result)
        except Exception as e:
            print(e)


def connect(mac):
    p = btle.Peripheral(mac)
    p.writeCharacteristic(0x0038, b'\x01\x00', True) 
    p.writeCharacteristic(0x0046, b'\xf4\x01\x00', True)
    return p

def getresult():
    global result
    return (result.temperature,result.humidity,result.voltage,result.battery)
