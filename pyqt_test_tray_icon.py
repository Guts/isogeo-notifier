import sys, time
from PyQt4 import QtCore, QtGui
import uiToast

window = None   # global

# Usage: Toast('Message')
class Toast(QtGui.QMainWindow):
    def __init__(self, msg):
        global window               # some space outside the local stack
        window = self               # save pointer till killed to avoid GC
        QtGui.QWidget.__init__(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui = uiToast.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.display.setText(msg)

        self.toastThread = ToastThread()    # start thread to remove display
        self.connect(self.toastThread, QtCore.SIGNAL("finished()"), self.toastDone)
        self.toastThread.start()
        self.show()

    def toastDone(self):
        global window
        window = None               # kill pointer to window object to close it and GC

class ToastThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        time.sleep(2.0)             # wait and die

if __name__ == '__main__':
    """standalone execution
    """
    tot = Toast("YOUHOU")