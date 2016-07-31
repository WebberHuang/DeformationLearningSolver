__author__ = "Webber Huang"
__contact__ = "xracz.fx@gmail.com"
__website__ = "http://riggingtd.com"
__buildVersionID__      = '1.5.4'
__ENVIRONMENT_NAME__ = "DEFORMATION_LEARNING_SOLVER"


import sys
import os
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui

PYSIDE_VERSION = '-1'
try:
    import PySide
    PYSIDE_VERSION = PySide.__version__
    from PySide import QtGui, QtCore
    from PySide.QtGui import *
    from PySide.QtCore import *
    from shiboken import wrapInstance
except ImportError:
    import PySide2
    PYSIDE_VERSION = PySide2.__version__
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# Static variables
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
SSD_SOLVER_PLUGIN_BASE_NAME = "SSDSolverCmd"
DELTA_MUSH_PLUGIN_BASE_NAME = "wbDeltaMushDeformer"
MAIN_WINDOW = "DeformationLearningSolverWin"


#----------------------------------------------------------------------
def getMayaWindow():
    ptr = omui.MQtUtil.mainWindow()
    if ptr:
        return wrapInstance(long(ptr), QWidget)

#----------------------------------------------------------------------
def show():
    """"""
    from DLS.widget import mainWindow
    reload(mainWindow)

    if cmds.window(MAIN_WINDOW, ex=1):
        cmds.deleteUI(MAIN_WINDOW)

    parent = getMayaWindow()
    win = mainWindow.MainWindow(parent)

    win.setWindowFlags(Qt.Window) # Make this widget a standalone window
    # identify a Maya-managed floating window, 
    # which handles the z order properly and saves its positions
    win.setProperty("saveWindowPref", True )  

    win.setAttribute(Qt.WA_DeleteOnClose)
    win.show()

#----------------------------------------------------------------------
def getEnviron():
    """"""
    return __ENVIRONMENT_NAME__


#----------------------------------------------------------------------
def loadSSDSolverPlugin():
    """"""    
    os = cmds.about(os=1)

    if os == 'win64':
        pluginName = '%s.mll' % (SSD_SOLVER_PLUGIN_BASE_NAME)
    elif os == 'mac':
        pluginName = '%s.bundle' % (SSD_SOLVER_PLUGIN_BASE_NAME)
    elif os == 'linux64':
        pluginName = '%s.so' % (SSD_SOLVER_PLUGIN_BASE_NAME)

    if not cmds.pluginInfo(pluginName, q=True, l=True ):
        try:
            cmds.loadPlugin(pluginName)
            pluginVers = cmds.pluginInfo(pluginName, q=1, v=1)
            log.info('Plug-in: %s v%s loaded success!' % (pluginName, pluginVers))
        except: 
            log.info('Plug-in: %s, was not found on MAYA_PLUG_IN_PATH.' % (pluginName))
    else:
        pluginVers = cmds.pluginInfo(pluginName, q=1, v=1)
        log.info('Plug-in: %s v%s has been loaded!' % (pluginName, pluginVers))

#----------------------------------------------------------------------
def loadDeltaMushPlugin():
    """"""   
    os = cmds.about(os=1)

    if os == 'win64':
        pluginName = '%s.mll' % (DELTA_MUSH_PLUGIN_BASE_NAME)
    elif os == 'mac':
        pluginName = '%s.bundle' % (DELTA_MUSH_PLUGIN_BASE_NAME)
    elif os == 'linux64':
        pluginName = '%s.so' % (DELTA_MUSH_PLUGIN_BASE_NAME)

    if not cmds.pluginInfo(pluginName, q=True, l=True ):
        try:
            cmds.loadPlugin(pluginName)
            pluginVers = cmds.pluginInfo(pluginName, q=1, v=1)
            log.info('Plug-in: %s v%s loaded success!' % (pluginName, pluginVers))
        except:
            log.info('Plug-in: %s, was not found on MAYA_PLUG_IN_PATH.' % (pluginName))
    else:
        pluginVers = cmds.pluginInfo(pluginName, q=1, v=1)
        log.info('Plug-in: %s v%s has been loaded!' % (pluginName, pluginVers))

#----------------------------------------------------------------------
def loadPlugin():
    """"""
    loadSSDSolverPlugin()
    loadDeltaMushPlugin()

#----------------------------------------------------------------------
def mayaVersion():
    """
    need to manage this better and use the API version,
    eg: 2013.5 returns 2013
    """
    return mel.eval('getApplicationVersionAsFloat')

#----------------------------------------------------------------------
def getModulePath():
    '''
    Returns the Main path to the root module folder
    '''
    return os.path.join(os.path.dirname(SCRIPT_DIRECTORY),'').replace('\\', '/')

#----------------------------------------------------------------------
def getVersion():
    return __buildVersionID__

#----------------------------------------------------------------------
def getAuthor():
    return __author__

#----------------------------------------------------------------------
def getMainWindowName():
    return MAIN_WINDOW

# BOOT FUNCTS - Add and Build --------------------------------------------------------------

def addScriptsPath(path):
    '''
    Add additional folders to the ScriptPath
    '''
    scriptsPath = os.environ.get('MAYA_SCRIPT_PATH')

    if os.path.exists(path):
        if not path in scriptsPath:
            log.info('Adding To Script Paths : %s' % path)
            os.environ['MAYA_SCRIPT_PATH']+='%s%s' % (os.pathsep, path)
        else:
            log.info('Deformation Learning Script Path already setup : %s' % path)
    else:
        log.debug('Given Script Path is invalid : %s' % path)


#=========================================================================================
# BOOT CALL ------------------------------------------------------------------------------
#=========================================================================================

def launch():
    '''
    Main entry point
    '''
    log.info('Deformation Learning v%s : Author: %s' % (getVersion(), getAuthor()))
    log.info('Deformation Learning Setup Calls :: Booting from >> %s' % getModulePath())  

    # Add module to environment
    os.environ[__ENVIRONMENT_NAME__] = getModulePath()    
    # addScriptsPath(os.environ[__ENVIRONMENT_NAME__])

    # Load Plug-in
    loadPlugin()    

    # launch UI
    show()

    log.info('Deformation Learning initialize Complete!')

def interface():
    show()
