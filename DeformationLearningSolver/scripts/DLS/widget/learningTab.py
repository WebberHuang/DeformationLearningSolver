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

import maya.cmds as cmds

from DLS.widget import baseTab
from DLS.widget import utils

from DLS.core import learningFunc


reload(learningFunc)
#reload(baseTab)
#reload(utils)


TAB = ''
uifile = os.path.join(utils.SCRIPT_DIRECTORY, "ui/learningTab.ui")
cfgfile = os.path.join(utils.SCRIPT_DIRECTORY, "config.ini")
ENABLE = True
INDEX = 1


########################################################################
class LearningTab(baseTab.BaseTab):
    """"""
    _TITLE = 'Learning'    
    
    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(LearningTab, self).__init__(parent)
        utils.loadUi(uifile, self)
        self.initWidgets()
    
    #----------------------------------------------------------------------
    def initWidgets(self):
        """"""
        self.readSettings()
        
        # Set transformation widgets        
        doubleVal = QDoubleValidator(decimals=3, parent=self)              
        
        # Set time range widgets
        timeSlider_rbtn = self.findChild(QRadioButton, "timeSlider_rbtn")
        if timeSlider_rbtn != None:
            timeSlider_rbtn.setChecked(True)
        
        startEnd_rbtn = self.findChild(QRadioButton, "startEnd_rbtn")
        if startEnd_rbtn != None:        
            startEnd_rbtn.setChecked(False)
        
        startTime_edit = self.findChild(QLineEdit, "startTime_edit")
        if startTime_edit != None:          
            startTime_edit.setEnabled(False)
            startTime_edit.setValidator(doubleVal)
         
        endTime_edit = self.findChild(QLineEdit, "endTime_edit")
        if endTime_edit != None:
            endTime_edit.setEnabled(False)
            endTime_edit.setValidator(doubleVal)
    
    #----------------------------------------------------------------------
    def getNumBones(self):
        """"""
        numBones_spn = self.findChild(QSpinBox, "numBones_spn")
        if numBones_spn != None:
            return numBones_spn.value()
        return 1
    
    #----------------------------------------------------------------------
    def setNumBones(self, val):
        """"""
        numBones_spn = self.findChild(QSpinBox, "numBones_spn")
        if numBones_spn != None:        
            numBones_spn.setValue(val) 
    
    #----------------------------------------------------------------------
    def getMaxInfs(self):
        """"""
        maxInfs_spn = self.findChild(QSpinBox, "maxInfs_spn")
        if maxInfs_spn != None:        
            return maxInfs_spn.value()
        return 4
    
    #----------------------------------------------------------------------
    def setMaxInfs(self, val):
        """"""
        maxInfs_spn = self.findChild(QSpinBox, "maxInfs_spn")
        if maxInfs_spn != None:          
            maxInfs_spn.setValue(val)    

    #----------------------------------------------------------------------
    def getEpsilon(self):
        """"""
        epsilon_spn = self.findChild(QDoubleSpinBox, "epsilon_spn")
        if epsilon_spn != None:          
            return epsilon_spn.value()
        return 1.0
    
    #----------------------------------------------------------------------
    def setEpsilon(self, val):
        """"""
        epsilon_spn = self.findChild(QDoubleSpinBox, "epsilon_spn")
        if epsilon_spn != None:          
            epsilon_spn.setValue(val)
    
    #----------------------------------------------------------------------
    def getMaxIters(self):
        """"""
        maxIters_spn = self.findChild(QSpinBox, "maxIters_spn")
        if maxIters_spn != None:        
            return maxIters_spn.value()
    
    #----------------------------------------------------------------------
    def setMaxIters(self, val):
        """"""
        maxIters_spn = self.findChild(QSpinBox, "maxIters_spn")
        if maxIters_spn != None:          
            maxIters_spn.setValue(val)

    #----------------------------------------------------------------------
    def getTargetMesh(self):
        """"""
        targetMesh_edit = self.findChild(QLineEdit, "targetMesh_edit")
        if targetMesh_edit != None:         
            return str(targetMesh_edit.text())
    
    #----------------------------------------------------------------------
    def setTargetMesh(self, val):
        """"""
        targetMesh_edit = self.findChild(QLineEdit, "targetMesh_edit")
        if targetMesh_edit != None:         
            targetMesh_edit.setText(val)
    
    #----------------------------------------------------------------------
    def isAlternativeUpdate(self):
        """"""
        alternativeUpdate_chk = self.findChild(QCheckBox, "alternativeUpdate_chk")
        if alternativeUpdate_chk != None:        
            return alternativeUpdate_chk.isChecked()
        return True
    
    #----------------------------------------------------------------------
    def setAlternativeUpdate(self, val):
        """"""
        alternativeUpdate_chk = self.findChild(QCheckBox, "alternativeUpdate_chk")
        if alternativeUpdate_chk != None:        
            alternativeUpdate_chk.setChecked(val)    

    #----------------------------------------------------------------------
    def getStartTime(self):
        """"""
        startTime_edit = self.findChild(QLineEdit, "startTime_edit")
        if startTime_edit != None:              
            return float(startTime_edit.text())
        return 0.0
    
    #----------------------------------------------------------------------
    def getEndTime(self):
        """"""
        endTime_edit = self.findChild(QLineEdit, "endTime_edit")
        if endTime_edit != None:        
            return float(endTime_edit.text())
        return 0.0
    
    #----------------------------------------------------------------------
    def isTimeSlider(self):
        """"""
        timeSlider_rbtn = self.findChild(QRadioButton, "timeSlider_rbtn")
        if timeSlider_rbtn != None:        
            return timeSlider_rbtn.isChecked()
        return True
    
    #----------------------------------------------------------------------
    def isStartEnd(self):
        """"""
        startEnd_rbtn = self.findChild(QRadioButton, "startEnd_rbtn")
        if startEnd_rbtn != None:            
            return startEnd_rbtn.isChecked()
    
    #----------------------------------------------------------------------
    def getTimeRange(self):
        """"""
        if self.isStartEnd():
            start = int(self.getStartTime())
            end = int(self.getEndTime())
            return start, end
            
        start = int(cmds.playbackOptions(q=1, min=1))
        end = int(cmds.playbackOptions(q=1, max=1))
        return start, end
    
    #----------------------------------------------------------------------
    def readSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)

        settings.beginGroup("Custom")
        self.setNumBones(int(settings.value("numBones")))
        self.setMaxInfs(int(settings.value("maxInfs")))
        self.setEpsilon(float(settings.value("epsilon")))
        self.setMaxIters(float(settings.value("maxIters")))
        settings.endGroup()
    
    #----------------------------------------------------------------------
    def writeSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)

        settings.beginGroup("Custom")
        settings.setValue("numBones", self.getNumBones())
        settings.setValue("maxInfs", self.getMaxInfs())
        settings.setValue("epsilon", float(self.getEpsilon()))
        settings.setValue("maxIters", self.getMaxIters())
        settings.endGroup()
    
    #----------------------------------------------------------------------
    def resetSettings(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        settings.beginGroup("Default")
        self.setNumBones(int(settings.value("numBones")))
        self.setMaxInfs(int(settings.value("maxInfs")))
        self.setEpsilon(float(settings.value("epsilon")))
        self.setMaxIters(int(settings.value("maxIters")))
        settings.endGroup()
        
        self.setTargetMesh("")
        self.setAlternativeUpdate(False)
    
    #----------------------------------------------------------------------
    @Slot()
    def on_loadTargetMesh_btn_clicked(self):
        mesh = learningFunc.getMeshFromSelection()
        self.setTargetMesh(mesh)
    
    #----------------------------------------------------------------------
    @Slot(bool)
    def on_startEnd_rbtn_toggled(self, isChecked):
        startTime_edit = self.findChild(QLineEdit, "startTime_edit")
        if startTime_edit != None:          
            startTime_edit.setEnabled(isChecked)        
        
        endTime_edit = self.findChild(QLineEdit, "endTime_edit")
        if endTime_edit != None:
            endTime_edit.setEnabled(isChecked)
    
    #----------------------------------------------------------------------
    @Slot()
    def on_solve_btn_clicked(self):
        settings = QSettings(cfgfile, QSettings.IniFormat)
        
        # Read global settings
        settings.beginGroup("Custom")
        pruneBelow = float(settings.value("pruneBeblow"))       
        isKeepOriginal = bool(int(settings.value("isKeepOriginal")))
        isDeleteDeltaMush = bool(int(settings.value("isDeleteDeltaMush")))
        settings.endGroup()
        
        # Read local settings
        numBones = self.getNumBones()
        maxInfs = self.getMaxInfs()
        start, end = self.getTimeRange()
        maxIters = self.getMaxIters()
        epilon = self.getEpsilon()
        targetMesh = self.getTargetMesh()
        isAlternativeUpdate = self.isAlternativeUpdate()
        learningFunc.solve(numBones, maxInfs, targetMesh, isAlternativeUpdate,
                           start, end, maxIters,isKeepOriginal, pruneBelow,
                           epilon, isDeleteDeltaMush)
    
    #----------------------------------------------------------------------
    @Slot()
    def on_measure_btn_clicked(self):
        start, end = self.getTimeRange()
        learningFunc.measure(start, end)
        
        
#----------------------------------------------------------------------
def getTab():
    """"""
    return LearningTab 
        
#----------------------------------------------------------------------
def main():
    import sys
    app = QApplication(sys.argv)
    window = LearningTab()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()