from os import listdir
import pandas as pd
import numpy as np
import pickle
from unitInfos import UnitInfos

class DataReader():
    """docstring for dataReader."""
    def __init__(self):
        self.dataDir = '../data/'
        self.experimentID = ['m4404ee', 'c6404ee']
        self.fileTypes = ['Tbhv', 'trTarget', 'ANDat', 'analogAx']

    def ex_int(self, s):
        try:
            int(s)
        except ValueError:
            return np.nan
        else:
            return int(s)

    def units(self, experimentID):
        targetDir = self.dataDir + experimentID
        files = listdir(targetDir)
        units = []
        for fileName in files:
            if fileName.startswith('unit') & fileName.endswith('.txt'):
                fh = open(targetDir + '/' + fileName)
                unit = UnitInfos()
                unit.Name = fileName.replace('.txt', '')
                for line in fh.readlines():
                    line = line.replace('\n', '')
                    if line.startswith('Spikes:'):
                        continue
                    elif line.startswith('IS:'):
                        elems = line.split(': ')
                        unit.IS = float(elems[1])
                    elif line.startswith('XYZ:'):
                        elems = line.split(': ')
                        unit.XYZ = [float(s) for s in elems[1].split(', ')]
                    elif line.startswith('Loc:'):
                        elems = line.split(': ')
                        unit.Loc = elems[1]
                    elif line.startswith('Stab:'):
                        elems = line.split(': ')
                        unit.Stab = [int(s) for s in elems[1].split(', ')]
                    else:
                        spikes = [self.ex_int(s) for s in line.split(', ')]
                        spikes = np.array(spikes)
                        unit.Spikes.append(spikes)
                units.append(unit)
        return units

    def makeUnitBinaryFiles(self, experimentID):
        targetDir = self.dataDir + experimentID
        units = self.units(experimentID)
        for unit in units:
            pickleFileName = targetDir + '/' + unit.Name + '.binaryfile'
            outFile = open(pickleFileName, 'wb')
            pickle.dump(unit, outFile)
