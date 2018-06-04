from os import listdir
import pandas as pd
import numpy as np
from quantities import s, ms
from neo.core import Block, Segment, ChannelIndex, Unit, SpikeTrain, AnalogSignal
from experimentData import ExperimentData

class NeoObject():
    """docstring for NeoObject."""
    def __init__(self):
        self.experimentID = ['m4404ee', 'c6404ee']

    def createDataBlock(self, experimentID):

        eData = ExperimentData()
        # prepare SpikesDataFrame
        SpikesDataFrame = eData.createSpikes_DF(experimentID)
        # prepate unitNames
        unitNames = eData.getUnitNames_L(experimentID)

        # create a Block of m4404ee
        blk = Block(name=experimentID)

        # create a segment for each trials
        trial_num = len(SpikesDataFrame)
        for trial_index in range(trial_num):
            seg = Segment(name='trial %i' % trial_index, index=trial_index)
            blk.segments.append(seg)

        # create a channel index
        chx = ChannelIndex(index=None, name='tetrode')
        blk.channel_indexes.append(chx)

        # create units
        for unitName in unitNames:
            unit = Unit(name=unitName)
            chx.units.append(unit)

        # starting time and stoppingtime of trial
        startTime = -1000
        stopTime = 4001

        # set spike trains into segment and unit
        for trial_index, seg in enumerate(blk.segments):
            for unitName in unitNames:
                spikeTrain_array = SpikesDataFrame[unitName].values[trial_index]
                spikeTimes_array = np.where(spikeTrain_array==1)[0] + startTime
                spikeTrain = SpikeTrain(spikeTimes_array*ms,t_start=startTime,t_stop=stopTime)
                seg.spiketrains.append(spikeTrain)

                unit = [unit for unit in chx.units if unit.name == unitName][0]
                unit.spiketrains.append(spikeTrain)

        return blk
