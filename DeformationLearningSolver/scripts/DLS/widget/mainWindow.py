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

from DLS.widget import optionWindow
from DLS.widget import aboutDialog
from DLS.widget import utils
from DLS.startup import setup
from DLS.core import miscFunc, samplingFunc

reload(miscFunc)
reload(samplingFunc)
#reload(optionWindow)
#reload(aboutDialog)
#reload(utils)

cfgfile = os.path.join(utils.SCRIPT_DIRECTORY, "config.ini")

########################################################################
class MainWindow(QMainWindow):
    """"""
    _TITLE = 'Deformation Learning Solver'

    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(MainWindow, self).__init__(parent)

        self.setObjectName(setup.getMainWindowName())        
        #self.parent = parent  # this's extremely important! without this line
                                # "Internal C++ object already deleted" happen
        self.initWidgets()

    #----------------------------------------------------------------------
    def initWidgets(self):
        """"""      
        self.setWindowTitle(self._TITLE)
        self.resize(100, 100)

        # Add actions
        openAbout = QAction("&About", self)
        openAbout.triggered.connect(self.showAbout)

        openOptions = QAction("&Options", self)
        openOptions.triggered.connect(self.showOption)

        resetSettings = QAction("&Reset", self)
        resetSettings.triggered.connect(self.resetSettings)

        selectAllBelow = QAction("Select All &Below", self)
        selectAllBelow.triggered.connect(self.selectAllBelowCmd)
        
        selectInfluenceJoints = QAction("Select Influence &Joints", self)
        selectInfluenceJoints.triggered.connect(self.selectInfluenceJointsCmd)        

        applyRigidSkin = QAction("Apply &Rigid Skin", self)
        applyRigidSkin.triggered.connect(self.applyRigidSkinCmd)
        
        deleteAnimations = QAction("Delete &Animations", self)
        deleteAnimations.triggered.connect(self.deleteAnimationsCmd)        

        applyDeltaMush = QAction("Apply &Delta Mush", self)
        applyDeltaMush.triggered.connect(self.applyDeltaMushCmd)

        # Add menu bar
        bar = self.menuBar()
        editMenu = bar.addMenu("&Edit")
        editMenu.addAction(openOptions)
        editMenu.addAction(resetSettings)

        toolMenu = bar.addMenu("&Tool")
        toolMenu.addAction(selectAllBelow)
        toolMenu.addAction(selectInfluenceJoints) 
        toolMenu.addAction(applyRigidSkin)
        toolMenu.addSeparator()
        toolMenu.addAction(deleteAnimations)
        toolMenu.addSeparator()
        toolMenu.addAction(applyDeltaMush)        

        helpMenu = bar.addMenu("&Help")
        helpMenu.addAction(openAbout)

        # Add base frame
        frame = QFrame(self)      
        layout = QVBoxLayout(self)
        frame.setLayout(layout)

        tabWidget = QTabWidget(self)
        tabWidget.setObjectName("allFuncs_tab")
        layout.addWidget(tabWidget)

        self.setCentralWidget(frame)

        # Add tabs dynamically
        for cls in utils.findAllTabs():
            tab = cls(self)
            self.addTab(tab, tabWidget)

        tabWidget.setCurrentIndex(0)

    #----------------------------------------------------------------------
    def addTab(self, tab, tabWidget):
        """
        adds tab object to tab UI, creating it's ui and attaching to main window
        """
        tabWidget.addTab(tab, tab.title())

    #----------------------------------------------------------------------
    def showAbout(self):
        """"""
        aboutDialog.AboutDialog(self).show()

    #----------------------------------------------------------------------
    def showOption(self):
        """"""
        optionWindow.OptionWindow(self).show()
            
    #----------------------------------------------------------------------
    def resetSettings(self):
        allFuncs_tab = self.findChild(QTabWidget, "allFuncs_tab")
        for i in xrange(allFuncs_tab.count()):
            allFuncs_tab.widget(i).resetSettings()  

    #----------------------------------------------------------------------        
    def selectAllBelowCmd(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Custom")
        skipTips = bool(int(settings.value("skipTips")))
        settings.endGroup()

        miscFunc.selectAllBelow(skipTips)
    
    #----------------------------------------------------------------------
    def selectInfluenceJointsCmd(self):
        miscFunc.selectInfluenceJoints()        

    #----------------------------------------------------------------------
    def applyRigidSkinCmd(self):
        miscFunc.applyRigidSkin()
    
    #----------------------------------------------------------------------
    def applyDeltaMushCmd(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Custom")
        useBuildInDeltaMush = bool(int(settings.value("useBuildInDeltaMush")))
        settings.endGroup()
        
        miscFunc.applyDeltaMush(useBuildIn=useBuildInDeltaMush)
    
    #----------------------------------------------------------------------
    def deleteAnimationsCmd(self):
        samplingFunc.deleteAnimations()        

    #----------------------------------------------------------------------
    def closeEvent(self, event):
        """"""
        allFuncs_tab = self.findChild(QTabWidget, "allFuncs_tab")
        for i in xrange(allFuncs_tab.count()):
            allFuncs_tab.widget(i).closeEvent(event)

        event.accept()


#----------------------------------------------------------------------
def main():
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()