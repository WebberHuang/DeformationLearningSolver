__author__ = "Webber Huang"
__contact__ = "xracz.fx@gmail.com"
__website__ = "http://riggingtd.com"


import maya.cmds as cmds
import maya.OpenMaya as om

from DLS.core import utils


#----------------------------------------------------------------------
def attrSampling(node, attr, minVal, maxVal, interval=1):
    """
    Args:
      node (str)
      attrs (list)
      minVal (float)
      maxVal (float)
      interval (int)
    
    Returns:
      int
    """    
    currTime = cmds.currentTime(q=1)
    currVal = cmds.getAttr('%s.%s' % (node, attr))
    vals = [currVal, currVal+minVal, currVal+maxVal, currVal]

    for i, v in enumerate(vals):
        if i not in [0, len(vals)-1] and (currVal - v) == 0:
            continue
        
        cmds.setKeyframe(node, at=attr, v=v, t=currTime)
        currTime += interval
    return currTime

#----------------------------------------------------------------------
def attrsSampling(attrData, interval=1):
    """
    Args:
      attrData (dict): {node1: [[attr1, min, max], [attr2, min, max], ...],
                        node2: [[attr1, min, max], [attr2, min, max], ...],
                        ...}
      interval (int)
    
    Returns:
      int
    """
    currTime = cmds.currentTime(q=1)
    for node, attrVals in attrData.iteritems():        
        for vals in attrVals:
            attr, minVal, maxVal = vals
            if not cmds.objExists('.'.join([node, attr])):
                continue
            currTime = attrSampling(node, attr, minVal, maxVal, interval)
            currTime -= 2 * interval
            cmds.currentTime(currTime)
    return currTime+1 * interval

#----------------------------------------------------------------------
def customAttrsSampling(attrData, interval=1):
    """
    Args:
      attrData (dict): {node1: [[attr1, min, max], [attr2, min, max], ...],
                        node2: [[attr1, min, max], [attr2, min, max], ...],
                        ...}
      interval (int)
    
    Returns:
      int
    """
    start = cmds.currentTime(q=1)
    currTime = attrsSampling(attrData, interval)
    end = currTime-1
    utils.trimTimeRange(start, end)
    cmds.currentTime(start) 

#----------------------------------------------------------------------
def blendShapeSampling(node, interval=1):
    """
    Args:
      node (str)
      interval (int)
    
    Returns:
      int
    """
    assert cmds.nodeType(node) == 'blendShape', \
        "node must be a blendShape type"
    start = cmds.currentTime(q=1)
    
    attrs = cmds.listAttr('%s.weight' % node, m=1)
    attrData = {node: [[attr, 0.0, 1.0] for attr in attrs]}
    
    currTime = attrsSampling(attrData, interval)

    end = currTime-1
    utils.trimTimeRange(start, end)
    cmds.currentTime(start)

#----------------------------------------------------------------------
def transformSampling(translateMin, translateMax,
                      rotateMin, rotateMax,
                      scaleMin, scaleMax,
                      isTranslate, isRotate, isScale,
                      translateAttrs = ('tx', 'ty', 'tz'),
                      rotateAttrs = ('rx', 'ry', 'rz'),
                      scaleAttrs = ('sx', 'sy', 'sz'),
                      interval=1):
    """
    Args:
      translateMin (float)
      translateMax (float)
      rotateMin (float)
      rotateMax (float)
      scaleMin (float)
      scaleMax (float)
      isTranslate (bool)
      isRotate (bool)
      isScale (bool)
      interval (int)
    """
    start = cmds.currentTime(q=1)
    sel = cmds.ls(sl=1, ap=1)
    if not sel:
        om.MGlobal.displayError("Please select some tranform nodes.")
        return
    
    attrData = {}    
    for node in sel:
        if not attrData.has_key(node):
            attrData[node] = []
            
        if isRotate:
            [attrData[node].append([attr, rotateMin, rotateMax]) for attr in rotateAttrs]
            
        if isTranslate:
            [attrData[node].append([attr, translateMin, translateMax]) for attr in translateAttrs]
        
        if isScale:
            [attrData[node].append([attr, scaleMin, scaleMax]) for attr in scaleAttrs]
    
    currTime = attrsSampling(attrData, interval)
            
    end = currTime-1
    utils.trimTimeRange(start, end)
    cmds.currentTime(start)    

#----------------------------------------------------------------------
def getBlendshapeFromSelection():
    """
    Returns:
      str
    """
    try:
        return cmds.ls(sl=1, type='blendShape')[0]
    except:
        om.MGlobal.displayError("No blendshape found in your selection.")
        return

#----------------------------------------------------------------------
def deleteAnimations():
    """"""
    animCurveTypes = ['animCurveTU', 'animCurveTA', 'animCurveTL', 'animCurveTT']
    
    sel = cmds.ls(sl=1, ap=1)
    if not sel:
        om.MGlobal.displayError("Please select something first.")
        return        
    
    for node in sel:
        connects = cmds.listConnections(node, s=1, d=0, scn=1)
        animCurves = cmds.ls(connects, type=animCurveTypes)
        cmds.delete(animCurves)


if __name__ == '__main__':
    node = 'locator1'
    bsNode = 'headGEO_IMBS'
    attr = 'tx'
    maxVal = 1
    minVal = -1
    interval = 1
    sel = cmds.ls(sl=1, ap=1)
    for s in sel:
        rotateSampling(s, -90, 90, interval)
        currTime = translateSampling(s, minVal, maxVal, interval)
    cmds.currentTime(currTime+1)
    # currTime = blendShapeSampling(bsNode, interval)
    # cmds.currentTime(currTime)