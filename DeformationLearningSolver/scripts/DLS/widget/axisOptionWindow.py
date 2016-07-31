__author__ = "Webber Huang"
__contact__ = "xracz.fx@gmail.com"
__website__ = "http://riggingtd.com"

import os

try:
    from PySide import QtGui, QtCore
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

from DLS.widget import utils
from DLS.widget import baseOptionWindow

#reload(baseOptionWindow)


uifile = os.path.join(utils.SCRIPT_DIRECTORY, "ui/axisWindow.ui")
cfgfile = os.path.join(utils.SCRIPT_DIRECTORY, "config.ini")


########################################################################
class AxisOptionWindow(baseOptionWindow.BaseOptionWindow):
    """"""
    _TITLE = 'Axis Options'
    
    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(AxisOptionWindow, self).__init__(parent)
        #utils.loadUi(uifile, self)    
        #self.initWidgets()
    
    #----------------------------------------------------------------------
    def initWidgets(self):
        """"""
        self.readSettings()
        
        self.setWindowTitle(self._TITLE)
        cp = QDesktopWidget().screenGeometry().center()
        self.move(cp)
        
        # Add actions        
        actionReset = self.findChild(QAction, "actionReset")
        if actionReset != None:
            actionReset.triggered.connect(self.resetSettings)
     
    #----------------------------------------------------------------------
    def isX(self):
        """"""
        x_chk = self.findChild(QCheckBox, "x_chk")
        if x_chk != None:
            return x_chk.isChecked()
        return True
    
    #----------------------------------------------------------------------
    def setX(self, val):
        """"""
        x_chk = self.findChild(QCheckBox, "x_chk")
        if x_chk != None:
            x_chk.setChecked(val)

    #----------------------------------------------------------------------
    def isY(self):
        """"""
        y_chk = self.findChild(QCheckBox, "y_chk")
        if y_chk != None:
            return y_chk.isChecked()
        return True
    
    #----------------------------------------------------------------------
    def setY(self, val):
        """"""
        y_chk = self.findChild(QCheckBox, "y_chk")
        if y_chk != None:
            y_chk.setChecked(val)

    #----------------------------------------------------------------------
    def isZ(self):
        """"""
        z_chk = self.findChild(QCheckBox, "z_chk")
        if z_chk != None:
            return z_chk.isChecked()
        return True
    
    #----------------------------------------------------------------------
    def setZ(self, val):
        """"""
        z_chk = self.findChild(QCheckBox, "z_chk")
        if z_chk != None:
            z_chk.setChecked(val)    


########################################################################
class TranslateAxisOptionWindow(AxisOptionWindow):
    """"""
    _TITLE = 'Translate Axis Options'

    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(TranslateAxisOptionWindow, self).__init__(parent)
        utils.loadUi(uifile, self)    
        self.initWidgets()
    
    #----------------------------------------------------------------------
    def resetSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Default")
        self.setX(bool(int(settings.value("translateX"))))
        self.setY(bool(int(settings.value("translateY"))))
        self.setZ(bool(int(settings.value("translateZ"))))
        settings.endGroup()

    #----------------------------------------------------------------------
    def readSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Custom")
        self.setX(bool(int(settings.value("translateX"))))
        self.setY(bool(int(settings.value("translateY"))))
        self.setZ(bool(int(settings.value("translateZ"))))  
        settings.endGroup()
    
    #----------------------------------------------------------------------
    def writeSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Custom")
        settings.setValue("translateX", int(self.isX()))
        settings.setValue("translateY", int(self.isY()))
        settings.setValue("translateZ", int(self.isZ()))
        settings.endGroup()  


########################################################################
class RotateAxisOptionWindow(AxisOptionWindow):
    """"""
    _TITLE = 'Rotate Axis Options'

    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(RotateAxisOptionWindow, self).__init__(parent)
        utils.loadUi(uifile, self)    
        self.initWidgets()
    
    #----------------------------------------------------------------------
    def resetSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Default")
        self.setX(bool(int(settings.value("rotateX"))))
        self.setY(bool(int(settings.value("rotateY"))))
        self.setZ(bool(int(settings.value("rotateZ"))))
        settings.endGroup()

    #----------------------------------------------------------------------
    def readSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Custom")
        self.setX(bool(int(settings.value("rotateX"))))
        self.setY(bool(int(settings.value("rotateY"))))
        self.setZ(bool(int(settings.value("rotateZ"))))  
        settings.endGroup()
    
    #----------------------------------------------------------------------
    def writeSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Custom")
        settings.setValue("rotateX", int(self.isX()))
        settings.setValue("rotateY", int(self.isY()))
        settings.setValue("rotateZ", int(self.isZ()))
        settings.endGroup()


########################################################################
class ScaleAxisOptionWindow(AxisOptionWindow):
    """"""
    _TITLE = 'Scale Axis Options'

    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(ScaleAxisOptionWindow, self).__init__(parent)
        utils.loadUi(uifile, self)    
        self.initWidgets()
    
    #----------------------------------------------------------------------
    def resetSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Default")
        self.setX(bool(int(settings.value("scaleX"))))
        self.setY(bool(int(settings.value("scaleY"))))
        self.setZ(bool(int(settings.value("scaleZ"))))
        settings.endGroup()

    #----------------------------------------------------------------------
    def readSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Custom")
        self.setX(bool(int(settings.value("scaleX"))))
        self.setY(bool(int(settings.value("scaleY"))))
        self.setZ(bool(int(settings.value("scaleZ"))))  
        settings.endGroup()
    
    #----------------------------------------------------------------------
    def writeSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Custom")
        settings.setValue("scaleX", int(self.isX()))
        settings.setValue("scaleY", int(self.isY()))
        settings.setValue("scaleZ", int(self.isZ()))
        settings.endGroup()  

#----------------------------------------------------------------------
def main():
    import sys
    app = QApplication(sys.argv)
    window = ScaleAxisOptionWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()