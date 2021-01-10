import time
import serial

result = time.localtime()
print("result:", result)
print("\nyear:", result.tm_mon)
print("tm_hour:", result.tm_hour)
print(str(result.tm_mon) + " " + str(result.tm_min))
ser = serial.Serial('COM9', 115200, timeout=0.2)
command = "A0 17 19"
print(command)
ser.write(command.encode())