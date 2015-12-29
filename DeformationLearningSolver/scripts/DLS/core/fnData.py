__author__ = "Webber Huang"
__contact__ = "xracz.fx@gmail.com"
__website__ = "http://riggingtd.com"


import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
from DLS.core import utils


class FnSkinCluster(object):

    def __init__(self, skinCluster=None):
        """
        Args:
          skinCluster (str, Optional): Defaults to None
        """
        self.skinCluster = skinCluster
        if skinCluster:
            self.fn = oma.MFnSkinCluster(utils.getDependNode(skinCluster))

    def setSkinCluster(self, skinCluster):
        """
        Args:
          skinCluster (str, Optional): Defaults to None

        Returns:
          SkinClusterFn
        """
        self.skinCluster = skinCluster
        self.fn = oma.MFnSkinCluster(utils.getDependNode(skinCluster))
        return self

    def getLogicalInfluenceIndex(self,influence):
        """
        Args:
          influence (str)

        Returns:
          int
        """
        try:
            dagPath = utils.getDagPath(influence)
        except:
            raise utils.UserInputError("Could not find influence '%s' in %s" %
                                        (influence, self.skinCluster))

        return self.fn.indexForInfluenceObject(dagPath)

    #----------------------------------------------------------------------
    def getPhysicalInfluenceIndex(self, influence):
        """
        Args:
          influence (str)

        Returns:
          int
        """
        matrices = cmds.listConnections("%s.matrix" % self.skinCluster, s=1, d=0)
        return matrices.index(influence)

    #----------------------------------------------------------------------
    def getInfluenceData(self, influence):
        """
        Args:
          influence (str)

        Returns:
          WeightData
        """
        try:
            dagPath = utils.getDagPath(influence)
        except:
            raise utils.UserInputError("Could not find influence '%s' in %s" %
                                        (influence, self.skinCluster))
        selList = om.MSelectionList()
        weights = om.MDoubleArray()

        self.fn.getPointsAffectedByInfluence(dagPath, selList, weights)

        componentStr = []
        selList.getSelectionStrings(componentStr)
        componentStr = cmds.ls(componentStr, ap=1, fl=1)
        weights = [w for w in weights]

        return WeightData(componentStr, weights)

    #----------------------------------------------------------------------
    def listInfluences(self, asDagPath=True):
        """
        Returns:
          list
        """
        dagPaths = om.MDagPathArray()
        self.fn.influenceObjects(dagPaths)
        if asDagPath: return dagPaths
        else: return [dagPaths[i].partialPathName() for i in xrange(dagPaths.length())]

    #----------------------------------------------------------------------
    def getWeightData(self, elements):
        """
        Args:
          elements (list)

        Returns:
          SkinWeightData
        """
        dagPath, components = utils.getDagPathComponents(elements)

        # Get all influences
        infs = self.listInfluences(asDagPath=False)
        influenceIndices = om.MIntArray()
        [influenceIndices.append(self.getPhysicalInfluenceIndex(inf)) for inf in infs]

        # Get all weights
        weights = om.MDoubleArray()
        self.fn.getWeights(dagPath, components, influenceIndices, weights)
        weights = [w for w in weights]

        return SkinWeightData(elements, infs, weights)

    #----------------------------------------------------------------------
    def setWeightData(self, data, normalize=True):
        """
        Args:
          data (SkinWeightData)
          normalize (bool, Optional): Defaults to True
        """
        # Construct dagPath and components
        compList = data.getComponents()
        dagPath, components = utils.getDagPathComponents(compList)

        # Construct influence indices
        influenceIndices = om.MIntArray()
        [influenceIndices.append(self.getPhysicalInfluenceIndex(inf)) for inf in data.getInfluences()]

        # Construct weights
        weights = om.MDoubleArray()
        [weights.append(w) for w in data.getWeights()]
        oldValues = om.MDoubleArray()
        self.fn.getWeights(dagPath, components, influenceIndices, oldValues)

        self.fn.setWeights(dagPath, components, influenceIndices, weights, normalize, oldValues)

    #----------------------------------------------------------------------
    def flushWeights(self, influence):
        """
        Args:
          influence (str)
        """
        weightData = self.getInfluenceData(influence)
        skinData = SkinWeightData(weightData.getElements(), [influence], weightData.getWeights())
        [skinData.addInfluence(comp, influence, 0.0) for comp in skinData.getComponents()]
        self.setWeightData(skinData)

    #----------------------------------------------------------------------
    def getInfluenceTransforms(self, space=om.MSpace.kObject):
        infs = self.listInfluences()

        if space == om.MSpace.kWorld:
            return [infs[i].inclusiveMatrix() for i in xrange(infs.length())]

        return [om.MFnTransform(infs[i]).transformation().asMatrix()
                for i in xrange(infs.length())]