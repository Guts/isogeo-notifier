import sys
from PyQt4 import Qt
app = Qt.QApplication(sys.argv)
systemtray_icon = Qt.QSystemTrayIcon(app, Qt.QIcon('/path/to/image'))
systemtray_icon.show()
systemtray_icon.showMessage('Title', 'Content')