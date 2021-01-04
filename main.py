from PyQt5 import QtWidgets, uic, QtCore, QtGui
import serial.tools.list_ports
import serial
from PyQt5.QtCore import QTimer
from datetime import datetime
import time

app = QtWidgets.QApplication([])
dlg = uic.loadUi("GUI/AS_Watch_APP.ui")
dlg.setWindowIcon(QtGui.QIcon('GUI/icon.png'))
NowPorts = []


def send():
    dlg.SerialPrint.append("")
    actualise = False

    port = dlg.PortList.currentData()

    ser = serial.Serial(port, 9600, timeout=1)
    print_in_serial = "Sending to: " + str(port) + ":"
    ser.readline()
    dlg.SerialPrint.append(print_in_serial)
    dlg.SerialPrint.append("    Connecting...")
    command = "A"
    ser.write(command.encode())
    data = "    " + ser.readline().decode("utf-8")
    print(data)
    if data:
        print(data)
        dlg.SerialPrint.append(data)

    if dlg.ActualiseTime.isChecked():
        print_in_serial = "   Actualise time to: " + str(datetime.now().strftime("%Y-%m-%e %H:%M:%S"))
        dlg.SerialPrint.append(print_in_serial)

    if dlg.SeaPressure.value():
        print_in_serial = "   Set sea pressure to: " + str(dlg.SeaPressure.value()) + " hPa"
        dlg.SerialPrint.append(print_in_serial)

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
