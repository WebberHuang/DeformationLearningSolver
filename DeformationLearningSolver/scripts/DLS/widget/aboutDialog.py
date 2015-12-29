__author__ = "Webber Huang"
__contact__ = "xracz.fx@gmail.com"
__website__ = "http://riggingtd.com"

import os

from PySide.QtCore import *
from PySide.QtGui import *

from DLS.widget import utils


uifile = os.path.join(utils.SCRIPT_DIRECTORY, "ui/aboutDialog.ui")


########################################################################
class AboutDialog(QDialog):
    """"""
    _TITLE = 'Utility'    
    
    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(AboutDialog, self).__init__(parent)
        utils.loadUi(uifile, self)
        self.initWidgets()
    
    #----------------------------------------------------------------------
    def initWidgets(self):
        """"""
        cp = QDesktopWidget().screenGeometry().center()
        self.move(cp)  
        
        
#----------------------------------------------------------------------
def main():
    import sys
    app = QApplication(sys.argv)
    window = AboutDialog()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()