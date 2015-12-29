__author__ = "Webber Huang"
__contact__ = "xracz.fx@gmail.com"
__website__ = "http://riggingtd.com"


import maya.cmds as cmds
import maya.OpenMaya as om

from DLS.core import utils


#----------------------------------------------------------------------
def applyRigidSkin():
    """"""
    sel = cmds.ls(sl=1, ap=1)
    if len(sel) < 2:
        om.MGlobal.displayError("Please select joints first, then mesh.")
        return
    mesh = sel.pop()
    cmds.skinCluster(sel, mesh, tsb=1, mi=0, nw=1, bm=1)

#----------------------------------------------------------------------
def applyDeltaMush(smooth=1.0, iterations=20, useBuildIn=False):
    """
    Args:
      smooth (float)
      iterations (int)
    """
    sel = cmds.ls(sl=1, ap=1)

    if not sel:
        om.MGlobal.displayError("Please select a few meshes.")
        return

    if useBuildIn:
        cmds.deltaMush(sel, si=iterations, ss=smooth, pbv=0)
    else:
        cmds.wbDeltaMush(sel, si=iterations, ss=smooth, pbv=0)

#----------------------------------------------------------------------
def selectAllBelow(skipTips=False):
    try:
        sel = cmds.ls(sl=1, ap=1)
        allDescs = sel + cmds.listRelatives(sel, f=1, ad=1, s=0, ni=1)
        if skipTips:
            allDescs = [s for s in allDescs if cmds.listRelatives(s, c=1)]
        cmds.select(allDescs)
    except:
        om.MGlobal.displayError("Please select something.")
        return

#----------------------------------------------------------------------
def selectInfluenceJoints():
    try:
        sel = cmds.ls(sl=1, ap=1)[0]
        try:
            skinNode = utils.findRelatedSkinCluster(sel)
            infs = cmds.skinCluster(skinNode, q=1, inf=1)
        except:
            om.MGlobal.displayError("No skinCluster found in history of %s." % sel)
            return             
        cmds.select(infs)
    except:
        om.MGlobal.displayError("Please select something.")
        return        
    