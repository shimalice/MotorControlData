from __future__ import print_function
from os import listdir
#import pickle

class unitStructure():
    def __init__(self):
        self.Spikes = []
    # def write():

dataDir = '../data/'
dirNames = ['m4404ee', 'c6404ee']
fileTypes = ['Tbhv', 'trTarget', 'ANDat', 'analogAx']

for dirName in dirNames:
    targetDir = dataDir + dirName
    files = listdir(targetDir)
    for fileName in files:
        unitL = []
        if fileName.startswith('unit'):
            fh = open(targetDir + '/' + fileName)
            unit = unitStructure()
            unitID = 0
            for line in fh.readline():
                if line.startswith('Spikes:'):
                    continue
                elif line.startswith('IS:'):
                    elems = line.split(':')
                    unit.IS = float(elems[1])
                elif line.startswith('XYZ:'):
                    elems = line.split(':')
                    unit.XYZ = elems[1]
                elif line.startswith('Loc:'):
                    elems = line.split(':')
                    unit.Loc = elems[1]
                elif line.startswith('Stab:'):
                    elems = line.split(':')
                    unit.Stab = elems[1]
                else:
                    # elems = line.split(',')
                    unit.Spikes.append(line)
                unitL.append(unit)

        pickleFileName = targetDir + '/' + fileName + '.pkl'
        outFile = open(pickleFileName, 'w')
        # pickle.dump(unitL, outFile)
