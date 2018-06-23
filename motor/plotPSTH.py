import math
import numpy as np
import matplotlib.pyplot as plt
from quantities import ms
from neo.core import Block, Segment, ChannelIndex, Unit, SpikeTrain, AnalogSignal, Event
from NeoObject import NeoObject
from elephant.statistics import time_histogram
from saveFig import save_fig

neoObject = NeoObject()
blk_L = [neoObject.createDataBlock(eID) for eID in neoObject.experimentID]

for blk in blk_L:
    list_units = blk.list_units
    colNum = 2
    rowNum = math.ceil(len(list_units) / colNum)

    fig = plt.figure(figsize=(10,10))
    fig.suptitle('PSTH for each unit of ' + blk.name)
    fig.subplots_adjust(hspace=0.4)

    for unit_i, unit in enumerate(list_units):
        plotID = unit_i + 1

        spiketrains = unit.spiketrains
        t_start = spiketrains[0].t_start
        t_stop = spiketrains[0].t_stop
        binsize = 50*ms
        time = np.arange(t_start, t_stop-1*ms, binsize)
        PSTH = time_histogram(spiketrains, binsize, output='rate', t_start=t_start, t_stop=t_stop)

        if plotID <= rowNum * colNum:
            ax = fig.add_subplot(rowNum, colNum, plotID)
            ax.plot(time, PSTH)
            plot_title = unit.name + ' [' + str(t_start) + str(t_stop) + ']'
            ax.set_title(plot_title, fontsize=9)

            if plotID % colNum != 1:
                labels = [item.get_text() for item in ax.get_yticklabels()]
                empty_string_labels = ['']*len(labels)
                ax.set_yticklabels(empty_string_labels)
            else:
                ax.set_ylabel('rate', fontsize=10)

            if plotID / colNum < rowNum - 1:
                labels = [item.get_text() for item in ax.get_xticklabels()]
                empty_string_labels = ['']*len(labels)
                ax.set_xticklabels(empty_string_labels)
            else:
                ax.set_xlabel('time', fontsize=10)
        ax.set_ylim([0.0, 0.1])
    # plt.show()
    save_fig('PSTH', blk.name)
