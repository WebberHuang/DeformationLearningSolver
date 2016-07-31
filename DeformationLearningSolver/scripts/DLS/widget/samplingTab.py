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

import maya.OpenMaya as om

from DLS.widget import utils

from DLS.core import samplingFunc
from DLS.widget import baseTab
from DLS.widget import axisOptionWindow
from DLS.widget import customAttributeEditor


#reload(baseTab)
#reload(utils)
reload(samplingFunc)
#reload(axisOptionWindow)
reload(customAttributeEditor)

TAB = ''
uifile = os.path.join(utils.SCRIPT_DIRECTORY, "ui/samplingTab.ui")
cfgfile = os.path.join(utils.SCRIPT_DIRECTORY, "config.ini")
ENABLE = True
INDEX = 2


########################################################################
class SamplingTab(baseTab.BaseTab):
    """
    self.attrData = {node1: [[attr1, min, max], [attr2, min, max], ...],
                     node2: [[attr1, min, max], [attr2, min, max], ...],
                     ...}
    """
    _TITLE = 'Sampling'
    
    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(SamplingTab, self).__init__(parent)
        utils.loadUi(uifile, self)
        self.attrData = {}
        self.initWidgets()
    
    #----------------------------------------------------------------------
    def initWidgets(self):
        """"""
        self.readSettings()
        
        doubleVal = QDoubleValidator(decimals=3, parent=self)
        
        # Set transformation widgets        
        rotateMin_edit = self.findChild(QLineEdit, "rotateMin_edit")
        if rotateMin_edit != None:
            rotateMin_edit.setValidator(doubleVal)
            
        rotateMax_edit = self.findChild(QLineEdit, "rotateMax_edit")
        if rotateMax_edit != None:
            rotateMax_edit.setValidator(doubleVal)        
        
        translateMin_edit = self.findChild(QLineEdit, "translateMin_edit")
        if translateMin_edit != None:        
            translateMin_edit.setValidator(doubleVal)
        
        translateMax_edit = self.findChild(QLineEdit, "translateMax_edit")
        if translateMax_edit != None:           
            translateMax_edit.setValidator(doubleVal)
            
        scaleMin_edit = self.findChild(QLineEdit, "scaleMin_edit")
        if scaleMin_edit != None:
            scaleMin_edit.setValidator(doubleVal)
        
        scaleMax_edit = self.findChild(QLineEdit, "scaleMax_edit")
        if scaleMax_edit != None:        
            scaleMax_edit.setValidator(doubleVal)

        # Set blendshape widgets
        rx = QRegExp("^[a-zA-Z][a-zA-Z0-9_]+")
        val = QRegExpValidator(rx, self)        
        blendshape_edit = self.findChild(QLineEdit, "blendshape_edit")
        if blendshape_edit != None:           
            blendshape_edit.setValidator(val)            
                
    #----------------------------------------------------------------------
    def getTranslateMin(self):
        """"""
        translateMin_edit = self.findChild(QLineEdit, "translateMin_edit")
        if translateMin_edit != None:           
            return float(translateMin_edit.text())
        return -1.0
    
    #----------------------------------------------------------------------
    def setTranslateMin(self, val):
        """"""
        translateMin_edit = self.findChild(QLineEdit, "translateMin_edit")
        if translateMin_edit != None:           
            translateMin_edit.setText(str(val))  

    #----------------------------------------------------------------------
    def getTranslateMax(self):
        """"""
        translateMax_edit = self.findChild(QLineEdit, "translateMax_edit")
        if translateMax_edit != None:         
            return float(translateMax_edit.text())
        return 1.0

    #----------------------------------------------------------------------
    def setTranslateMax(self, val):
        """"""
        translateMax_edit = self.findChild(QLineEdit, "translateMax_edit")
        if translateMax_edit != None:         
            translateMax_edit.setText(str(val))
    
    #----------------------------------------------------------------------
    def getRotateMin(self):
        """"""
        rotateMin_edit = self.findChild(QLineEdit, "rotateMin_edit")
        if rotateMin_edit != None:        
            return float(rotateMin_edit.text())
        return -90.0

    #----------------------------------------------------------------------
    def setRotateMin(self, val):
        """"""
        rotateMin_edit = self.findChild(QLineEdit, "rotateMin_edit")
        if rotateMin_edit != None:        
            rotateMin_edit.setText(str(val))

    #----------------------------------------------------------------------
    def getRotateMax(self):
        """"""
        rotateMax_edit = self.findChild(QLineEdit, "rotateMax_edit")
        if rotateMax_edit != None:        
            return float(rotateMax_edit.text())
        return 90.0

    #----------------------------------------------------------------------
    def setRotateMax(self, val):
        """"""
        rotateMax_edit = self.findChild(QLineEdit, "rotateMax_edit")
        if rotateMax_edit != None:        
            rotateMax_edit.setText(str(val))
    
    #----------------------------------------------------------------------
    def getScaleMin(self):
        """"""
        scaleMin_edit = self.findChild(QLineEdit, "scaleMin_edit")
        if scaleMin_edit != None:        
            return float(scaleMin_edit.text())
        return -1.0

    #----------------------------------------------------------------------
    def setScaleMin(self, val):
        """"""
        scaleMin_edit = self.findChild(QLineEdit, "scaleMin_edit")
        if scaleMin_edit != None:        
            scaleMin_edit.setText(str(val))

    #----------------------------------------------------------------------
    def getScaleMax(self):
        """"""
        scaleMax_edit = self.findChild(QLineEdit, "scaleMax_edit")
        if scaleMax_edit != None:         
            return float(scaleMax_edit.text())
        return 1.0

    #----------------------------------------------------------------------
    def setScaleMax(self, val):
        """"""
        scaleMax_edit = self.findChild(QLineEdit, "scaleMax_edit")
        if scaleMax_edit != None:         
            scaleMax_edit.setText(str(val))
    
    #----------------------------------------------------------------------
    def getBlendshapeName(self):
        """"""
        blendshape_edit = self.findChild(QLineEdit, "blendshape_edit")
        if blendshape_edit != None:         
            return str(blendshape_edit.text())
    
    #----------------------------------------------------------------------
    def setBlendshapeName(self, val):
        """"""
        blendshape_edit = self.findChild(QLineEdit, "blendshape_edit")
        if blendshape_edit != None:         
            blendshape_edit.setText(str(val))  

    #----------------------------------------------------------------------
    def isTranslate(self):
        """"""
        translate_chk = self.findChild(QCheckBox, "translate_chk")
        if translate_chk != None:
            return translate_chk.isChecked()
        return False

    #----------------------------------------------------------------------
    def setTranslate(self, val):
        """"""
        translate_chk = self.findChild(QCheckBox, "translate_chk")
        if translate_chk != None:
            translate_chk.setChecked(val)
            translate_chk.click()
            translate_chk.click()              
    
    #----------------------------------------------------------------------
    def isRotate(self):
        """"""
        rotate_chk = self.findChild(QCheckBox, "rotate_chk")
        if rotate_chk != None:        
            return rotate_chk.isChecked()
        return True

    #----------------------------------------------------------------------
    def setRotate(self, val):
        """"""
        rotate_chk = self.findChild(QCheckBox, "rotate_chk")
        if rotate_chk != None:        
            rotate_chk.setChecked(val)
            rotate_chk.click()
            rotate_chk.click()            
    
    #----------------------------------------------------------------------
    def isScale(self):
        """"""
        scale_chk = self.findChild(QCheckBox, "scale_chk")
        if scale_chk != None:         
            return scale_chk.isChecked()
        return False

    #----------------------------------------------------------------------
    def setScale(self, val):
        """"""
        scale_chk = self.findChild(QCheckBox, "scale_chk")
        if scale_chk != None:         
            scale_chk.setChecked(val)
            scale_chk.click()
            scale_chk.click()
    
    #----------------------------------------------------------------------
    def isTransform(self):
        """"""
        transformOptions_frame = self.findChild(QFrame, "transformOptions_frame")
        if transformOptions_frame != None:
            return transformOptions_frame.isEnabled()
        return False
    
    #----------------------------------------------------------------------
    def isBlendshape(self):
        """"""
        blendshape_chk = self.findChild(QCheckBox, "blendshape_chk")
        if blendshape_chk != None:         
            return blendshape_chk.isChecked()
        return False
    
    #----------------------------------------------------------------------
    def setBlendshape(self, val):
        """"""
        blendshape_chk = self.findChild(QCheckBox, "blendshape_chk")
        if blendshape_chk != None:         
            blendshape_chk.setChecked(val)
            blendshape_chk.click()
            blendshape_chk.click()
    
    #----------------------------------------------------------------------
    def isCustomAttrs(self):
        """"""
        customAttrs_chk = self.findChild(QCheckBox, "customAttrs_chk")
        if customAttrs_chk != None:         
            return customAttrs_chk.isChecked()
        return False
    
    #----------------------------------------------------------------------
    def setCustomAttrs(self, val):
        """"""
        customAttrs_chk = self.findChild(QCheckBox, "customAttrs_chk")
        if customAttrs_chk != None:         
            customAttrs_chk.setChecked(val)
            customAttrs_chk.click()
            customAttrs_chk.click()
            
    #----------------------------------------------------------------------
    def resetSettings(self):
        """"""
        settings = QSettings(cfgfile, QSettings.IniFormat)

        settings.beginGroup("Default")
        self.setBlendshape(bool(int(settings.value("isBlendshape"))))
        self.setBlendshapeName(settings.value("blendshapeName"))
        
        self.setTranslate(bool(int(settings.value("isTranslate"))))
        self.setTranslateMin(float(settings.value("translateMin")))
        self.setTranslateMax(float(settings.value("translateMax")))
        
        self.setRotate(bool(int(settings.value("isRotate"))))
        self.setRotateMin(float(settings.value("rotateMin")))
        self.setRotateMax(float(settings.value("rotateMax")))
        
        self.setScale(bool(int(settings.value("isScale"))))
        self.setScaleMin(float(settings.value("scaleMin")))
        self.setScaleMax(float(settings.value("scaleMax")))
        
        self.setCustomAttrs(bool(int(settings.value("isCustomAttrs"))))
        
        settings.endGroup()

    #----------------------------------------------------------------------
    def readSettings(self):
        """"""
        settings = QSettings(cfgfile, QSettings.IniFormat)

        settings.beginGroup("Custom")
        self.setBlendshape(bool(int(settings.value("isBlendshape"))))
        
        self.setTranslate(bool(int(settings.value("isTranslate"))))
        self.setTranslateMin(float(settings.value("translateMin")))
        self.setTranslateMax(float(settings.value("translateMax")))
        
        self.setRotate(bool(int(settings.value("isRotate"))))
        self.setRotateMin(float(settings.value("rotateMin")))
        self.setRotateMax(float(settings.value("rotateMax")))
        
        self.setScale(bool(int(settings.value("isScale"))))
        self.setScaleMin(float(settings.value("scaleMin")))
        self.setScaleMax(float(settings.value("scaleMax")))
        
        self.setCustomAttrs(bool(int(settings.value("isCustomAttrs"))))
        
        settings.endGroup()

    #----------------------------------------------------------------------
    def writeSettings(self):
        """"""
        settings = QSettings(cfgfile, QSettings.IniFormat)

        settings.beginGroup("Custom")
        settings.setValue("isTranslate", int(self.isTranslate()))
        settings.setValue("translateMin", self.getTranslateMin())
        settings.setValue("translateMax", self.getTranslateMax())
        
        settings.setValue("isRotate", int(self.isRotate()))
        settings.setValue("rotateMin", self.getRotateMin())
        settings.setValue("rotateMax", self.getRotateMax())
        
        settings.setValue("isScale", int(self.isScale()))
        settings.setValue("scaleMin", self.getScaleMin())
        settings.setValue("scaleMax", self.getScaleMax())
        
        settings.setValue("isBlendshape", int(self.isBlendshape()))
        
        settings.setValue("isCustomAttrs", int(self.isCustomAttrs()))
        
        settings.endGroup()
    
    #----------------------------------------------------------------------
    @Slot(bool)
    def on_translate_chk_clicked(self, isChecked):
        translateMin_edit = self.findChild(QLineEdit, "translateMin_edit")
        if translateMin_edit != None:         
            translateMin_edit.setEnabled(isChecked)
            
        translateMax_edit = self.findChild(QLineEdit, "translateMax_edit")
        if translateMax_edit != None:         
            translateMax_edit.setEnabled(isChecked)
    
    #----------------------------------------------------------------------
    @Slot()
    def on_translateOpt_btn_clicked(self):
        axisOptionWindow.TranslateAxisOptionWindow(self).show()
    
    #----------------------------------------------------------------------
    @Slot(bool)
    def on_rotate_chk_clicked(self, isChecked):
        rotateMin_edit = self.findChild(QLineEdit, "rotateMin_edit")
        if rotateMin_edit != None:          
            rotateMin_edit.setEnabled(isChecked)
        
        rotateMax_edit = self.findChild(QLineEdit, "rotateMax_edit")
        if rotateMax_edit != None:          
            rotateMax_edit.setEnabled(isChecked)

    #----------------------------------------------------------------------
    @Slot()
    def on_rotateOpt_btn_clicked(self):
        axisOptionWindow.RotateAxisOptionWindow(self).show()

    #----------------------------------------------------------------------
    @Slot(bool)
    def on_scale_chk_clicked(self, isChecked):
        scaleMin_edit = self.findChild(QLineEdit, "scaleMin_edit")
        if scaleMin_edit != None:         
            scaleMin_edit.setEnabled(isChecked)
        
        scaleMax_edit = self.findChild(QLineEdit, "scaleMax_edit")
        if scaleMax_edit != None:             
            scaleMax_edit.setEnabled(isChecked)

    #----------------------------------------------------------------------
    @Slot()
    def on_scaleOpt_btn_clicked(self):
        axisOptionWindow.ScaleAxisOptionWindow(self).show()
    
    #----------------------------------------------------------------------
    @Slot(bool)
    def on_blendshape_chk_clicked(self, isChecked):
        transformOptions_frame = self.findChild(QFrame, "transformOptions_frame")
        if transformOptions_frame != None:
            transformOptions_frame.setEnabled(not isChecked)
        
        blendshape_edit = self.findChild(QLineEdit, "blendshape_edit")
        if blendshape_edit != None:           
            blendshape_edit.setEnabled(isChecked)
        
        loadBlendshape_btn = self.findChild(QPushButton, "loadBlendshape_btn")
        if loadBlendshape_btn != None:        
            loadBlendshape_btn.setEnabled(isChecked)
        
        customAttrsOptions_frame = self.findChild(QFrame, "customAttrsOptions_frame")
        if customAttrsOptions_frame != None:         
            customAttrsOptions_frame.setEnabled(not isChecked)         
    
    #----------------------------------------------------------------------
    @Slot()
    def on_loadBlendshape_btn_clicked(self):
        blendshape = samplingFunc.getBlendshapeFromSelection()
        
        blendshape_edit = self.findChild(QLineEdit, "blendshape_edit")
        if blendshape_edit != None:        
            blendshape_edit.setText(blendshape)

    #----------------------------------------------------------------------
    @Slot(bool)
    def on_customAttrs_chk_clicked(self, isChecked):
        transformOptions_frame = self.findChild(QFrame, "transformOptions_frame")
        if transformOptions_frame != None:
            transformOptions_frame.setEnabled(not isChecked)
        
        blendshapeOptions_frame = self.findChild(QFrame, "blendshapeOptions_frame")
        if blendshapeOptions_frame != None:           
            blendshapeOptions_frame.setEnabled(not isChecked)    
        
        openCustomAttrsEditor_btn = self.findChild(QPushButton, "openCustomAttrsEditor_btn")
        if openCustomAttrsEditor_btn != None:         
            openCustomAttrsEditor_btn.setEnabled(isChecked)

    #----------------------------------------------------------------------
    @Slot()
    def on_openCustomAttrsEditor_btn_clicked(self):
        editor = customAttributeEditor.CustomAttributeEditor(self.attrData, self)
        editor.showUI()
        
    #----------------------------------------------------------------------
    @Slot()
    def on_run_btn_clicked(self):
        # Sample transform attributes
        if self.isTransform():            
            translateMin = self.getTranslateMin()
            translateMax = self.getTranslateMax()
            rotateMin = self.getRotateMin()
            rotateMax = self.getRotateMax()
            scaleMin = self.getScaleMin()
            scaleMax = self.getScaleMax()
            isTranslate = self.isTranslate()
            isRotate = self.isRotate()
            isScale = self.isScale()
            
            translateAttrs = []
            rotateAttrs = []
            scaleAttrs = []
            
            # Parse axis settings
            settings = QSettings(cfgfile, QSettings.IniFormat)
            settings.beginGroup("Custom")
            if bool(int(settings.value("translateX"))): translateAttrs.append("tx")
            if bool(int(settings.value("translateY"))): translateAttrs.append("ty")
            if bool(int(settings.value("translateZ"))): translateAttrs.append("tz")
            
            if bool(int(settings.value("rotateX"))): rotateAttrs.append("rx")
            if bool(int(settings.value("rotateY"))): rotateAttrs.append("ry")
            if bool(int(settings.value("rotateZ"))): rotateAttrs.append("rz")
            
            if bool(int(settings.value("scaleX"))): scaleAttrs.append("sx")
            if bool(int(settings.value("scaleY"))): scaleAttrs.append("sy")
            if bool(int(settings.value("scaleZ"))): scaleAttrs.append("sz")             
            settings.endGroup()            
            
            
            samplingFunc.transformSampling(translateMin,
                                           translateMax,
                                           rotateMin,
                                           rotateMax,
                                           scaleMin,
                                           scaleMax,
                                           isTranslate,
                                           isRotate,
                                           isScale,
                                           translateAttrs,
                                           rotateAttrs,
                                           scaleAttrs)
        
        # Sample blendshape attributes
        if self.isBlendshape():
            blendshape = self.getBlendshapeName()
            if blendshape:
                samplingFunc.blendShapeSampling(blendshape)
            else:
                om.MGlobal.displayError("Please load blendshape first.")
                return
        
        # Sample custom attributes    
        if self.isCustomAttrs():
            if self.attrData:
                samplingFunc.customAttrsSampling(self.attrData)
            else:
                om.MGlobal.displayError("Please append attributes for sampling first.")
                return


#----------------------------------------------------------------------
def getTab():
    """"""
    return SamplingTab
            
#----------------------------------------------------------------------
def main():
    import sys
    app = QApplication(sys.argv)
    window = SamplingTab()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()