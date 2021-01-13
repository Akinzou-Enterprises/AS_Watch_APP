from PyQt5 import QtWidgets, uic, QtCore, QtGui
import serial.tools.list_ports
import serial
from PyQt5.QtCore import QTimer
import time

app = QtWidgets.QApplication([])
dlg = uic.loadUi("GUI/AS_Watch_APP.ui")
dlg.setWindowIcon(QtGui.QIcon('GUI/icon.png'))
NowPorts = []


def send():
    dlg.SerialPrint.append("")
    actualise = False

    port = dlg.PortList.currentData()

    ser = serial.Serial(port, 115200, timeout=0.2)
    print_in_serial = "Sending to: " + str(port)
    ser.readline()
    dlg.SerialPrint.append(print_in_serial)
    dlg.SerialPrint.append("    Connecting...")
    command = "A"
    ser.write(command.encode())
    data = ser.readline().decode("utf-8")
    print(data)
    if data == "Connected!":
        print_in_serial = "      " + data
        dlg.SerialPrint.append(print_in_serial)

    else:
        dlg.SerialPrint.append("    Can't connect to device!")
        return

    if dlg.ActualiseTime.isChecked():
        dlg.SerialPrint.append("     Actualise time")
        result = time.localtime()
        print(result.tm_sec)
        command = "A0 " + str(result.tm_sec) + " " + str(result.tm_min) + " " + str(result.tm_hour)
        print(command.encode())
        ser.write(command.encode())
        data = ser.readline().decode("utf-8")
        time.sleep(1)
        command = "A2 " + str(result.tm_mday) + " " + str(result.tm_mon) + " " + str(result.tm_year - 2000) + " " + str(result.tm_wday + 1)
        print(command.encode())
        ser.write(command.encode())
        data = ser.readline().decode("utf-8")

    if dlg.SeaPressure.value():
        print_in_serial = "   Set sea pressure to: " + str(dlg.SeaPressure.value()) + " hPa"
        command = "A1 " + str(dlg.SeaPressure.value())
        dlg.SerialPrint.append("     Setting sea level pressure")
        dlg.SerialPrint.append(print_in_serial)

    time.sleep(0.5)
    ser.close()


def check_ports():
    global NowPorts
    ports = list(serial.tools.list_ports.comports())

    if ports != NowPorts:
        dlg.PortList.clear()
        for p in ports:
            print(p)
            dlg.PortList.addItem(str(p), p.device)

        dlg.PortList.setEnabled(True)
        dlg.ActualiseTime.setEnabled(True)
        dlg.Execute.setEnabled(True)
        dlg.SeaPressure.setEnabled(True)
        dlg.SerialPrint.setEnabled(True)

    if not ports:
        dlg.PortList.clear()
        dlg.PortList.addItem("Nothing is connected!")
        dlg.PortList.setEnabled(False)
        dlg.ActualiseTime.setEnabled(False)
        dlg.Execute.setEnabled(False)
        dlg.SeaPressure.setEnabled(False)
        dlg.SerialPrint.setEnabled(False)

    NowPorts = ports
    QTimer.singleShot(1000, check_ports)


dlg.Execute.clicked.connect(send)
check_ports()
dlg.show()
app.exec()
