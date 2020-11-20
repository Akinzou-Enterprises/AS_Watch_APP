from PyQt5 import QtWidgets, uic, QtCore, QtGui
import serial.tools.list_ports
from PyQt5.QtCore import QTimer
from datetime import datetime

app = QtWidgets.QApplication([])
dlg = uic.loadUi("GUI/AS_Watch_APP.ui")
dlg.setWindowIcon(QtGui.QIcon('GUI/icon.png'))
ints = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
NowPorts = []


def send():
    dlg.SerialPrint.append("")
    actualise = False
    SelectedPortList = list(dlg.PortList.currentText())
    port = 'COM'
    port += SelectedPortList[3]

    if SelectedPortList[4] in ints:
        port += SelectedPortList[4]

    PrintInSerial = "Sending to: " + str(port) + ":"
    dlg.SerialPrint.append(PrintInSerial)

    if dlg.ActualiseTime.isChecked():
        PrintInSerial = "   Actualise time to: " + str(datetime.now().strftime("%Y-%m-%e %H:%M:%S"))
        dlg.SerialPrint.append(PrintInSerial)

    if dlg.SeaPressure.value():
        PrintInSerial = "   Set sea pressure to: " + str(dlg.SeaPressure.value()) + " hPa"
        dlg.SerialPrint.append(PrintInSerial)

def checkPorts():
    global NowPorts
    ports = list(serial.tools.list_ports.comports())

    if ports != NowPorts:
        dlg.PortList.clear()
        for p in ports:
            dlg.PortList.addItem(str(p))

        dlg.PortList.setEnabled(True)
        dlg.ActualiseTime.setEnabled(True)
        dlg.Execute.setEnabled(True)
        dlg.SeaPressure.setEnabled(True)
        dlg.SerialPrint.setEnabled(True)

    if ports == []:
        dlg.PortList.clear()
        dlg.PortList.addItem("Nothing is connected!")
        dlg.PortList.setEnabled(False)
        dlg.ActualiseTime.setEnabled(False)
        dlg.Execute.setEnabled(False)
        dlg.SeaPressure.setEnabled(False)
        dlg.SerialPrint.setEnabled(False)

    NowPorts = ports
    QTimer.singleShot(1000, checkPorts)


dlg.Execute.clicked.connect(send)
checkPorts()
dlg.show()
app.exec()
