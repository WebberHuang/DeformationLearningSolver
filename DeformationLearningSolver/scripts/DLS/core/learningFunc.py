__author__ = "Webber Huang"
__contact__ = "xracz.fx@gmail.com"
__website__ = "http://riggingtd.com"


import maya.cmds as cmds
import maya.OpenMaya as om

from DLS.core import utils
from DLS.core import fnData
reload(utils)


#----------------------------------------------------------------------
def solve(numBones, maxInfs, targetMesh, isAlternativeUpdate, start, end, maxIters=10, isKeepOriginal=True,
          pruneBelow=0.0, epsilon=1.0, isDeleteDeltaMush=False):
    """
    Args:
      numBones (int)
      maxInfs (int)
      start (int)
      end (int)
      maxIters (int)
      epsilon (float)
    """
    try:
        mesh = cmds.ls(sl=1)[0];
    except:
        om.MGlobal.displayError("Select mesh first.")
        return
    
    mode = 0
        
    skinCluster = utils.findRelatedSkinCluster(mesh)
    if skinCluster:
        fnSkin = fnData.FnSkinCluster(skinCluster)
        bones = fnSkin.listInfluences(False)
        
        if targetMesh: # Solve transformations from existing weights
            if not isAlternativeUpdate: # Alternative update transformations and weights with new mesh sequences
                mode = 2
        else: # Solve weights from existing transformations
            targetMesh = mesh
            mode = 1
        cmds.ssdSolver(mesh,
                       tm=targetMesh,
                       m=mode,
                       mit=maxIters,
                       mi=maxInfs,                           
                       ib=bones,
                       isc=skinCluster,
                       st=start,
                       et=end,
                       pb=pruneBelow, 
                       e=epsilon)            
    else:
        if isKeepOriginal:
            # Duplicate a new mesh, then transfer deformation with blendshape
            cmds.currentTime(start)
            new_mesh = cmds.duplicate(mesh, name="%s_solved" % mesh, rc=1, rr=1)[0]
            blendshape = cmds.blendShape(mesh, new_mesh, o="world")[0]
            attrs = cmds.listAttr('%s.weight' % blendshape, m=1)
            cmds.setAttr("%s.%s" % (blendshape, attrs[0]), 1)
            mesh = new_mesh
        
        targetMesh = mesh
        cmds.ssdSolver(mesh,
                       tm=targetMesh,
                       m=mode, 
                       mi=maxInfs,
                       nb=numBones,
                       st=start,
                       et=end,
                       mit=maxIters,                       
                       pb=pruneBelow, 
                       e=epsilon)
        
        if isKeepOriginal:
            cmds.delete(blendshape)
    
    # postprocessing
    if isDeleteDeltaMush:
        deltaMushNode = utils.findRelatedDeltaMush(mesh)
        if deltaMushNode:
            cmds.delete(deltaMushNode)

#----------------------------------------------------------------------
def measure(start, end):
    """"""
    src, tgt = '', ''
    try:
        src, tgt = cmds.ls(sl=1, ap=1)
    except:
        om.MGlobal.displayError("Please select two meshes.")
        return
    
    cmds.ssdSolver(src, st=start, et=end, cw=tgt)

#----------------------------------------------------------------------
def getMeshFromSelection():
    """"""
    try:
        node = cmds.ls(sl=1, ap=1)[0]
        dagPath = utils.getDagPath(node)
        if dagPath.hasFn(om.MFn.kMesh):
            return node
        else:
            om.MGlobal.displayError("\"%s\" isn't mesh type." % node)
    except:
        return ""