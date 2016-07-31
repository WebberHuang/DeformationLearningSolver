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
import maya.OpenMaya as om


from DLS.widget import baseOptionWindow
from DLS.widget import utils
from DLS.startup import setup


uifile = os.path.join(utils.SCRIPT_DIRECTORY, "ui/customAttributeEditor.ui")
cfgfile = os.path.join(utils.SCRIPT_DIRECTORY, "config.ini")


########################################################################
class CustomAttributeEditor(baseOptionWindow.BaseOptionWindow):
    """
    self.data = {node1: [[attr1, min, max], [attr2, min, max], ...],
                 node2: [[attr1, min, max], [attr2, min, max], ...],
                 ...}
    """
    
    _TITLE = 'Custom Attributes Editor'
    _HEAD_LABLE = ['Attribute','Min','Max']
    
    #----------------------------------------------------------------------
    def __init__(self, data, parent=None):
        """Constructor"""
        super(CustomAttributeEditor, self).__init__(parent)
        utils.loadUi(uifile, self)
        self.parent = parent
        self.table = None
        self.attrs = []
        self.minVals = []
        self.maxVals = []
        self.data = data
        
        self.initWidgets() 
    
    #----------------------------------------------------------------------
    def initWidgets(self):
        """"""        
        self.setWindowTitle(self._TITLE)
        cp = QDesktopWidget().screenGeometry().center()
        self.move(cp)
        
        # Set table        
        self.table = self.findChild(QTableWidget, "data_table")
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(self._HEAD_LABLE)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(1, 56)
        self.table.setColumnWidth(2, 56)
        
        if setup.PYSIDE_VERSION < 2.0:
            self.table.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)
        else:
            self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        # Fill table
        i = 0
        for node, attrVals in self.data.iteritems():
            for vals in attrVals:
                attr, minVal, maxVal = vals
                name = "%s.%s" %  (node, attr)
                self.appendRow()
                self.setRow(i, [name, minVal, maxVal])
                i += 1
            
        # Set delete row action
        delAction = QAction(self)
        delAction.setObjectName("del_action")
        delAction.triggered.connect(self.removeRow)
        delAction.setShortcut(QKeySequence.Delete)
        delAction.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.addAction(delAction)
        
        # Set signal functions
        self.table.itemChanged.connect(self.setItems)
    
    #----------------------------------------------------------------------
    def numRow(self):
        return self.table.rowCount()
    
    #----------------------------------------------------------------------
    def numColumn(self):
        return self.table.columnCount()    
    
    #----------------------------------------------------------------------
    def appendRow(self):
        self.table.insertRow(self.numRow())
        for i in xrange(self.numColumn()):
            self.table.setItem(self.numRow()-1, i, QTableWidgetItem('0'))
    
    #----------------------------------------------------------------------
    def setRow(self, row, data):
        """
        Args:
          row (int)
          data (list)
        """
        for i in xrange(len(data)):
            self.table.item(row, i).setText(str(data[i]))
    
    #----------------------------------------------------------------------
    def getDataOnRow(self, row):
        """
        Args:
          row (int)
        """
        data = []
        for i in xrange(self.numColumn()):
            val = self.table.item(row, i).text()
            if i > 0: val = float(val)
            data.append(val)
        return data
    
    #----------------------------------------------------------------------
    def setItems(self, item):
        """
        Args:
          item (QTableWidgetItem)
        """
        self.table.blockSignals(True)
        
        value = item.text()
        dataType = item.type()
        for cellIdx in self.table.selectedIndexes():
            currCell = self.table.item(cellIdx.row(), cellIdx.column())
            if currCell.type() == dataType:
                currCell.setText(value)
        
        self.table.blockSignals(False)
    
    #----------------------------------------------------------------------
    def removeRow(self):
        """"""
        selRanges = self.table.selectedRanges()
        for sel in reversed(selRanges):            
            if sel.columnCount() == 3:
                for i in xrange(sel.bottomRow(), sel.topRow()-1, -1):
                    self.table.removeRow(i)
            else:
                # Set each cell's value to 0
                for i in xrange(sel.topRow(), sel.bottomRow()+1):
                    for j in xrange(sel.leftColumn(), sel.rightColumn()+1):
                        item = QTableWidgetItem('0')
                        self.table.setItem(i, j, item)
    
    #----------------------------------------------------------------------
    def saveData(self):
        """"""
        self.data.clear()
        for i in xrange(self.numRow()):
            nodeAttr, minVal, maxVal = self.getDataOnRow(i)
            node, attr = nodeAttr.split('.')
            if not self.data.has_key(node):
                self.data[node] = []
            self.data[node].append([attr, minVal, maxVal])                
    
    #----------------------------------------------------------------------
    @Slot()
    def on_add_btn_clicked(self):
        
        selNodes = cmds.ls(sl=1, ap=1)
        if not selNodes:
            om.MGlobal.displayError("Please select some nodes and attributes.")
            return
        
        selAttrs = (cmds.channelBox("mainChannelBox", q=1, sma=1) or []) \
            + (cmds.channelBox("mainChannelBox", q=1, sha=1) or []) \
            + (cmds.channelBox("mainChannelBox", q=1, ssa=1) or []) \
            + (cmds.channelBox("mainChannelBox", q=1, soa=1) or [])
        
        if not selAttrs:
            selAttrs = cmds.listAttr(selNodes, v=1, k=1, sn=1)
            selAttrs = list(set(selAttrs))
            try:
                selAttrs.remove('v')
            except:
                pass
        
        self.table.clearSelection()
        
        for node in selNodes:
            for attr in selAttrs:
                name = "%s.%s" % (node, attr)
                minVal, maxVal = 0.0, 1.0
                hasMinVal, hasMaxVal = False, False
                
                if not cmds.objExists(name):
                    continue
                
                # Set minVal
                if cmds.attributeQuery(attr, node=node, minExists=1):
                    minVal = cmds.attributeQuery(attr, node=node, min=1)[0]
                    hasMinVal = True
                
                if cmds.attributeQuery(attr, node=node, softMinExists=1):
                    minVal = cmds.attributeQuery(attr, node=node, smn=1)[0]
                    hasMinVal = True
                
                # Set maxVal    
                if cmds.attributeQuery(attr, node=node, maxExists=1):
                    maxVal = cmds.attributeQuery(attr, node=node, max=1)[0]
                    hasMaxVal = True
                
                if cmds.attributeQuery(attr, node=node, softMaxExists=1):
                    maxVal = cmds.attributeQuery(attr, node=node, smx=1)[0]
                    hasMaxVal = True
                
                currVal = cmds.getAttr(name)
                if hasMinVal: minVal = minVal - currVal
                if hasMaxVal: maxVal = maxVal - currVal
                    
                self.appendRow()
                self.setRow(self.numRow()-1, [name, minVal, maxVal])
    
    #----------------------------------------------------------------------
    @Slot()
    def on_clear_btn_clicked(self):
        for i in xrange(self.numRow()-1, -1, -1):
            self.table.removeRow(i)
    
    #----------------------------------------------------------------------
    @Slot()
    def on_save_btn_clicked(self):
        self.saveData()        
        self.close()    
            


#----------------------------------------------------------------------
def main():
    import sys
    app = QApplication(sys.argv)
    window = CustomAttributeEditor([])
    window.show()
    app.exec_()


if __name__ == "__main__":
    main() 