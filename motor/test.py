import pandas as pd
import numpy as np
from quantities import s, ms
from neo.core import Block, Segment, ChannelIndex, Unit, SpikeTrain, AnalogSignal
from dataReader import DataReader
from experimentData import ExperimentData
from NeoObject import NeoObject


# dReder = DataReader()
# for eID in dReder.experimentID:
#     dReder.makeUnitBinaryFiles(eID)

eData = ExperimentData()
for eID in eData.experimentID:
    UnitNames = eData.getTrTargets_A(eID)
    print(UnitNames)

# neoObject = NeoObject()
# for eID in neoObject.experimentID:
#     print(eID)
#     blk = neoObject.createDataBlock(eID)
#     print(blk.segments)
