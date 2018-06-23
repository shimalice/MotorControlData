import math
import numpy as np
import matplotlib.pyplot as plt
from quantities import ms
from neo.core import Block, Segment, ChannelIndex, Unit, SpikeTrain, AnalogSignal, Event
from NeoObject import NeoObject
from saveFig import save_fig

neoObject = NeoObject()
blk_L = [neoObject.createDataBlock(eID) for eID in neoObject.experimentID]

for blk in blk_L:

    list_units = blk.list_units

    colNum = 2
    rowNum = math.ceil(len(list_units) / colNum)

    fig = plt.figure(figsize=(10,10))
    fig.suptitle('Raster plot for each unit of ' + blk.name)
    fig.subplots_adjust(hspace=0.4)

    for unit_i, unit in enumerate(list_units):
        plotID = unit_i + 1

        spiketrains = unit.spiketrains

        ax = fig.add_subplot(len(blk.list_units)//2+1, 2, unit_i+1)
        for i, spiketrain in enumerate(spiketrains):
            ax.plot(spiketrain, i*np.ones_like(spiketrain), 'k.', markersize=2)
        ax.set_title('%s' % unit.name)

        if plotID % colNum != 1:
            labels = [item.get_text() for item in ax.get_yticklabels()]
            empty_string_labels = ['']*len(labels)
            ax.set_yticklabels(empty_string_labels)
        else:
            ax.set_ylabel('trial', fontsize=10)

        if plotID / colNum < rowNum - 1:
            labels = [item.get_text() for item in ax.get_xticklabels()]
            empty_string_labels = ['']*len(labels)
            ax.set_xticklabels(empty_string_labels)
        else:
            ax.set_xlabel('time', fontsize=10)
        ax.set_ylim([0.0,len(spiketrains)])
    # plt.show()
    save_fig('Raster', blk.name)
