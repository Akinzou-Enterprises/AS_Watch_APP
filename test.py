import time
import serial

result = time.localtime()
print("result:", result)
print("\nyear:", result.tm_mon)
print("tm_hour:", result.tm_hour)
print(str(result.tm_year - 2000))