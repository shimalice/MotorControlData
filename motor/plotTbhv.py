import matplotlib.pyplot as plt
from neo.core import Block, Segment, ChannelIndex, Unit, SpikeTrain, AnalogSignal, Event
from NeoObject import NeoObject
from saveFig import save_fig

neoObject = NeoObject()
blk_L = [neoObject.createDataBlock(eID) for eID in neoObject.experimentID]

for blk in blk_L:
    segments = blk.segments
    for segment in segments:
        Tbhv = [ e for e in segment.events if e.name == 'Tbhv'][0]
        plt.title('Tbhv of ' + blk.name)
        plt.xticks(range(len(Tbhv)), Tbhv.labels, rotation=10)
        plt.plot(Tbhv, '--o')
    # plt.show()
    save_fig('Tbhv', blk.name)
