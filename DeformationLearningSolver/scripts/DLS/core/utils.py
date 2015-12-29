__author__ = "Webber Huang"
__contact__ = "xracz.fx@gmail.com"
__website__ = "http://riggingtd.com"

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma



# Create exception class
class UserInputError(Exception): pass

#----------------------------------------------------------------------
def mayaVersion():
    """
    need to manage this better and use the API version,
    eg: 2013.5 returns 2013
    """
    return mel.eval('getApplicationVersionAsFloat')

#----------------------------------------------------------------------    
def getDependNode(name):
    """
    Args:
      name (str)

    Returns:
      MOBject
    """
    selList = om.MSelectionList()
    selList.add (name)
    node = om.MObject()
    selList.getDependNode(0, node)
    return node

#----------------------------------------------------------------------    
def getDagPath(name):
    """
    Args:
      name (str)

    Returns:
      MDagPath
    """
    selList = om.MSelectionList()
    selList.add (name)
    dagPath = om.MDagPath()
    selList.getDagPath(0, dagPath)
    return dagPath

#----------------------------------------------------------------------    
def getComponent(name):
    """
    Args:
      name (str)

    Returns:
      MOBject
    """
    selList = om.MSelectionList()
    selList.add (name)
    dagPath = om.MDagPath()
    component = om.MObject()
    selList.getDagPath(0, dagPath, component)
    return component

#----------------------------------------------------------------------
def getDagPathComponents(compList):
    """
    Args:
      compList (list)

    Returns:
      MObject
    """

    currSel = cmds.ls(sl=1, l=1)
    cmds.select(compList, r=1)
    selList = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selList)
    dagPath = om.MDagPath()
    components = om.MObject()
    selList.getDagPath(0, dagPath, components)
    cmds.select(cl=1)
    try:
        cmds.select(currSel, r=1)
    except:
        pass
    return dagPath, components

#----------------------------------------------------------------------
def findRelatedSkinCluster(geometry):
    '''
    Return the skinCluster attached to the specified geometry
    
    Args:
      geometry (str): Geometry object/transform to query
    
    Returns:
      str
    '''
    # Check geometry
    if not cmds.objExists(geometry):
        om.MGlobal.displayError('Object '+geometry+' does not exist!')
        return
    
    # Check transform
    if cmds.objectType(geometry) == 'transform':
        try: geometry = cmds.listRelatives(geometry,s=True,ni=True,pa=True)[0]
        except:
            om.MGlobal.displayError('Object %s has no deformable geometry!' % geometry)
            return

    # Determine skinCluster
    skin = mel.eval('findRelatedSkinCluster \"%s\"' % geometry)
    if not skin: 
        skin = cmds.ls(cmds.listHistory(geometry, pdo=1, gl=1), type='skinCluster')
        if skin: skin = skin[0]
    if not skin: skin = None

    # Return result
    return skin

#----------------------------------------------------------------------
def findRelatedDeltaMush(geometry):
    """
    Return the delta mush deformer attached to the specified geometry
    
    Args:
      geometry (str): Geometry object/transform to query
    
    Returns:
      str
    """
    # Check geometry
    if not cmds.objExists(geometry):
        raise Exception('Object '+geometry+' does not exist!')
    
    hist = cmds.listHistory(geometry, pdo=1, gl=1)
    try:
        if mayaVersion() >= 2016:
            return cmds.ls(hist, type=["deltaMush", "wbDeltaMush"])[0]
        else:
            return cmds.ls(hist, type="wbDeltaMush")[0]
    except:        
        return None

#----------------------------------------------------------------------
def trimTimeRange(start, end):
    """
    Args:
      start (float)
      end (float)
    """
    animCtrl = oma.MAnimControl()
    startTime = om.MTime(start)
    endTime = om.MTime(end)
    animCtrl.setAnimationStartEndTime (startTime, endTime)
    animCtrl.setMinMaxTime(startTime, endTime)    
