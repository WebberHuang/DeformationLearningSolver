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

from DLS.widget import baseTab
from DLS.widget import utils
from DLS.core import miscFunc

#reload(baseTab)
#reload(utils)
reload(miscFunc)


TAB = ''
uifile = os.path.join(utils.SCRIPT_DIRECTORY, "ui/miscTab.ui")
ENABLE = False
INDEX = 3


########################################################################
class MiscTab(baseTab.BaseTab):
    """"""
    _TITLE = 'Misc'    
    
    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(MiscTab, self).__init__(parent)
        utils.loadUi(uifile, self)
        self.initWidgets()
    
    #----------------------------------------------------------------------
    def initWidgets(self):
        """"""
        pass
    
    #----------------------------------------------------------------------
    @Slot()
    def on_applyRigidSkinWeights_btn_clicked(self):
        miscFunc.applyRigidSkin() 
    
    #----------------------------------------------------------------------
    @Slot()
    def on_applyDeltaMushDeformer_btn_clicked(self):
        miscFunc.applyDeltaMushDeformer()
    
    #----------------------------------------------------------------------
    @Slot()
    def on_transSkinWeights_btn_clicked(self):
        msg = b"This's transfer skin weights function"       
        QMessageBox.information(self, self.trUtf8(b'Informations'),
                                self.trUtf8(msg))
    
    #----------------------------------------------------------------------
    @Slot()
    def on_transBlendshapAttrs_btn_clicked(self):
        msg = b"This's transfer blendshape function"  
        QMessageBox.information(self, self.trUtf8(b'Informations'),
                                self.trUtf8(msg))
        
        
#----------------------------------------------------------------------
def getTab():
    """"""
    return MiscTab
        
#----------------------------------------------------------------------
def main():
    import sys
    app = QApplication(sys.argv)
    window = MiscTab()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()