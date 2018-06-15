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

    def _getAnalogData(self, experimentID, name_data, flatten=False):
        files, targetDir = self._experimentfiles_L(experimentID)
        for fileName in files:
            if fileName.startswith(name_data):
                df = pd.read_csv(targetDir + '/' + fileName, header=None)
                data = df.values
                if flatten:
                    data = data.ravel()
        return data

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

    def getTrTarget_A(self, experimentID):
        trTarget = self._getAnalogData(experimentID, name_data='trTarget', flatten=True)
        return trTarget

    def getTbhv_A(self, experimentID):
        Tbhv = self._getAnalogData(experimentID, name_data='Tbhv')
        return Tbhv

    def getANdat_A(self, experimentID):
        ANdat = self._getAnalogData(experimentID, name_data='ANdat')
        return ANdat

    def getAnalogAx_A(self, experimentID):
        analogAx = self._getAnalogData(experimentID, name_data='analogAx', flatten=True)
        return analogAx
