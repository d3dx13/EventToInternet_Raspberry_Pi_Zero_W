import serial.tools.list_ports
import serial

ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))
    ser = serial.Serial(port, baudrate=9600)
    print(ser.write(b'0100'))
    print(ser.readline())
