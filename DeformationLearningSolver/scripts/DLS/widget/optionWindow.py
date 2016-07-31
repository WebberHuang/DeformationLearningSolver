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

from DLS.startup import setup

#reload(baseOptionWindow)


uifile = os.path.join(utils.SCRIPT_DIRECTORY, "ui/optionWindow.ui")
cfgfile = os.path.join(utils.SCRIPT_DIRECTORY, "config.ini")


########################################################################
class OptionWindow(baseOptionWindow.BaseOptionWindow):
    """"""
    _TITLE = 'Options'
    
    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(OptionWindow, self).__init__(parent)
        utils.loadUi(uifile, self)    
        self.initWidgets()
    
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
        
        # Connect signal and slot
        pruneBelow_spn = self.findChild(QDoubleSpinBox, "pruneBelow_spn")
        if pruneBelow_spn != None:        
            pruneBelow_spn.valueChanged.connect(self.changePruneBelow_slider)
        
        pruneBelow_slider = self.findChild(QSlider, "pruneBelow_slider")
        if pruneBelow_slider != None:         
            pruneBelow_slider.valueChanged.connect(self.changePruneBelow_spn)
        
        # Set use build-in delta mush
        if setup.mayaVersion() >= 2016:
            self.setUseBuildInDeltaMushEnable(True) 

    #----------------------------------------------------------------------
    def getPruneBelow(self):
        """"""
        pruneBelow_spn = self.findChild(QDoubleSpinBox, "pruneBelow_spn")
        if pruneBelow_spn != None:
            return pruneBelow_spn.value()
        return 0.0
    
    #----------------------------------------------------------------------
    def setPruneBelow(self, val):
        """"""
        pruneBelow_spn = self.findChild(QDoubleSpinBox, "pruneBelow_spn")
        if pruneBelow_spn != None:
            pruneBelow_spn.setValue(val)
    
    #----------------------------------------------------------------------
    def isKeepOriginal(self):
        """"""
        keepOriginal_chk = self.findChild(QCheckBox, "keepOriginal_chk")
        if keepOriginal_chk != None:
            return keepOriginal_chk.isChecked()
        return True
    
    #----------------------------------------------------------------------
    def setKeepOriginal(self, val):
        """"""
        keepOriginal_chk = self.findChild(QCheckBox, "keepOriginal_chk")
        if keepOriginal_chk != None:
            keepOriginal_chk.setChecked(val)

    #----------------------------------------------------------------------
    def isDeleteDeltaMush(self):
        """"""
        deleteDeltaMush_chk = self.findChild(QCheckBox, "deleteDeltaMush_chk")
        if deleteDeltaMush_chk != None:
            return deleteDeltaMush_chk.isChecked()
        return False
    
    #----------------------------------------------------------------------
    def setDeleteDeltaMush(self, val):
        """"""
        deleteDeltaMush_chk = self.findChild(QCheckBox, "deleteDeltaMush_chk")
        if deleteDeltaMush_chk != None:
            deleteDeltaMush_chk.setChecked(val)
    
    #----------------------------------------------------------------------
    def setUseBuildInDeltaMush(self, val):
        """"""
        useBuildInDeltaMush_chk = self.findChild(QCheckBox, "useBuildInDeltaMush_chk")
        if useBuildInDeltaMush_chk != None:
            useBuildInDeltaMush_chk.setChecked(val)
    
    #----------------------------------------------------------------------
    def setUseBuildInDeltaMushEnable(self, val):
        """"""
        useBuildInDeltaMush_chk = self.findChild(QCheckBox, "useBuildInDeltaMush_chk")
        if useBuildInDeltaMush_chk != None:
            useBuildInDeltaMush_chk.setEnabled(val)    
    
    #----------------------------------------------------------------------
    def useBuildInDeltaMush(self):
        """"""
        useBuildInDeltaMush_chk = self.findChild(QCheckBox, "useBuildInDeltaMush_chk")
        if useBuildInDeltaMush_chk != None:
            return useBuildInDeltaMush_chk.isEnabled() and useBuildInDeltaMush_chk.isChecked()

    #----------------------------------------------------------------------
    def setSkipTips(self, val):
        """"""
        skipTips_chk = self.findChild(QCheckBox, "skipTips_chk")
        if skipTips_chk != None:
            skipTips_chk.setChecked(val)
    
    #----------------------------------------------------------------------
    def skipTips(self):
        """"""
        skipTips_chk = self.findChild(QCheckBox, "skipTips_chk")
        if skipTips_chk != None:
            return skipTips_chk.isChecked()      

    #----------------------------------------------------------------------
    def resetSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Default")
        self.setPruneBelow(float(settings.value("pruneBeblow")))
        self.setKeepOriginal(bool(int(settings.value("isKeepOriginal"))))
        self.setDeleteDeltaMush(bool(int(settings.value("isDeleteDeltaMush"))))
        self.setUseBuildInDeltaMush(bool(int(settings.value("useBuildInDeltaMush"))))
        self.setSkipTips(bool(int(settings.value("skipTips"))))
        settings.endGroup()
    
    #----------------------------------------------------------------------
    def readSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Custom")
        self.setPruneBelow(float(settings.value("pruneBeblow")))        
        self.setKeepOriginal(bool(int(settings.value("isKeepOriginal"))))
        self.setDeleteDeltaMush(bool(int(settings.value("isDeleteDeltaMush"))))
        self.setUseBuildInDeltaMush(bool(int(settings.value("useBuildInDeltaMush"))))
        self.setSkipTips(bool(int(settings.value("skipTips"))))
        settings.endGroup()
    
    #----------------------------------------------------------------------
    def writeSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Custom")
        settings.setValue("pruneBeblow", float(self.getPruneBelow()))
        settings.setValue("isKeepOriginal", int(self.isKeepOriginal()))
        settings.setValue("isDeleteDeltaMush", int(self.isDeleteDeltaMush()))
        settings.setValue("useBuildInDeltaMush",  int(self.useBuildInDeltaMush()))
        settings.setValue("skipTips", int(self.skipTips()))
        settings.endGroup()        
    
    #----------------------------------------------------------------------
    @Slot()
    def changePruneBelow_spn(self):
        """"""
        val = 0
        pruneBelow_slider = self.findChild(QSlider, "pruneBelow_slider")
        if pruneBelow_slider != None:
            val = float(pruneBelow_slider.value()) / 100000
        
        pruneBelow_spn = self.findChild(QDoubleSpinBox, "pruneBelow_spn")
        if pruneBelow_spn != None:        
            pruneBelow_spn.setValue(val)
    
    #----------------------------------------------------------------------
    @Slot()
    def changePruneBelow_slider(self):
        """"""
        val = 0
        pruneBelow_spn = self.findChild(QDoubleSpinBox, "pruneBelow_spn")
        if pruneBelow_spn != None:
            val = int(pruneBelow_spn.value() * 100000)
        
        pruneBelow_slider = self.findChild(QSlider, "pruneBelow_slider")
        if pruneBelow_slider != None:
            pruneBelow_slider.setValue(val)      

        
#----------------------------------------------------------------------
def main():
    import sys
    app = QApplication(sys.argv)
    window = OptionWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()