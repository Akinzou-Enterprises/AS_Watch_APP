import  serial

ser = serial.Serial('COM9', 9600, timeout=1)
Command = "b"

x = 2
while x:
    print(x)
    x -= 1
    ser.write(Command.encode())
    data = ser.readline()
    # if data == b'\r\n':
    #     continue
    if data:
        print(data)
