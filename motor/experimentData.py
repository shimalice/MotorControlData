from os import listdir
import pandas as pd
import numpy as np
import pickle
from unitInfos import UnitInfos

class ExperimentData(object):
    """docstring for experimentData."""
    def __init__(self):
        self.dataDir = '../data/'
        self.experimentID = ['m4404ee', 'c6404ee']

    def _experimentfiles_L(self, experimentID):
        targetDir = self.dataDir + experimentID
        files = listdir(targetDir)
        return files, targetDir

    def createSpikes_DF(self, experimentID):
        files, targetDir = self._experimentfiles_L(experimentID)
        unitDict = {}
        for fileName in files:
            if fileName.startswith('unit') & fileName.endswith('.binaryfile'):
                fh = open(targetDir + '/' + fileName, 'rb')
                unit = pickle.load(fh)
                unitDict[unit.Name] = unit.Spikes
        return pd.DataFrame(unitDict)

    def getUnitNames_L(self, experimentID):
        SpikesDataFrame = self.createSpikes_DF(experimentID)
        unitNames = SpikesDataFrame.columns
        unitNames = np.array(unitNames)
        return unitNames

    def getTrTargets_A(self, experimentID):
        files, targetDir = self._experimentfiles_L(experimentID)
        for fileName in files:
            if fileName.startswith('trTarget'):
                trTargetsDataFrame = pd.read_csv(targetDir + '/' + fileName, header=None)
                trTargets = trTargetsDataFrame.values
                trTargets = trTargets.ravel()
        return trTargets

    def getTbhv(self, experimentID):
        files, targetDir = self._experimentfiles_L(experimentID)
        for fileName in files:
            if fileName.startswith('Tbhv'):
                Tbhv = self.read_csv(targetDir + '/' + fileName, header=None)
        return Tbhv.values

    def getANdat(self, experimentID):
        files, targetDir = self._experimentfiles_L(experimentID)
        for fileName in files:
            if fileName.startswith('ANdat'):
                ANdat = self.read_csv(targetDir + '/' + fileName, header=None)
        return ANdat.values
