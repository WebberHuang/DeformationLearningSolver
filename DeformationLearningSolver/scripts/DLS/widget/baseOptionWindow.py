__author__ = "Webber Huang"
__contact__ = "xracz.fx@gmail.com"
__website__ = "http://riggingtd.com"

from PySide.QtCore import *
from PySide.QtGui import *


########################################################################
class BaseOptionWindow(QMainWindow):
    """"""
    _TITLE = ''

    #----------------------------------------------------------------------
    def __init__(self, parent = None):
        """Constructor"""
        super(BaseOptionWindow, self).__init__(parent)
        #QMainWindow.__init__(self, parent)
        #self.initWidgets()
            
    #----------------------------------------------------------------------
    def initWidgets(self):
        NotImplemented      

    #----------------------------------------------------------------------
    def resetSettings(self):
        NotImplemented

    #----------------------------------------------------------------------
    def readSettings(self):
        NotImplemented

    #----------------------------------------------------------------------
    def writeSettings(self):
        NotImplemented
    
    #----------------------------------------------------------------------
    @Slot()
    def on_save_btn_clicked(self):
        self.writeSettings()        
        self.close()

    #----------------------------------------------------------------------
    @Slot()
    def on_cancel_btn_clicked(self):
        self.close()

    #----------------------------------------------------------------------
    def showUI(self):
        """"""
        self.readSettings()
        self.show()