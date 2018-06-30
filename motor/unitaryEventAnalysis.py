import numpy as np
import quantities as pq
import matplotlib.pyplot as plt
import string
import neo
import elephant.unitary_event_analysis as ue
import elephant.neo_tools as nt
from NeoObject import NeoObject
from experimentData import ExperimentData
from saveFig import save_fig

# defo params
winsize = 100*pq.ms
binsize = 5*pq.ms
winstep = 5*pq.ms
pattern_hash = [3]
method = 'analytic_TrialAverage'
significance_level = 0.05
ms = 5


def plotUEAnalysisFigure(data, Js_dict, sig_level, binsize, winsize, winstep, pattern_hash, N):
    t_start = data[0][0].t_start
    t_stop = data[0][0].t_stop

    t_winpos = ue._winpos(t_start, t_stop, winsize, winstep)
    Js_sig = ue.jointJ(sig_level)
    num_tr = len(data)
    pat = ue.inverse_hash_from_pattern(pattern_hash, N)

    fig = plt.figure()
    ax = plt.subplot(1,1,1)
    # ax.set_title('Unitary Events')
    for n in range(N):
        for tr, data_tr in enumerate(spiketrains):
            ax.plot(data_tr[n].rescale('ms').magnitude,
                    np.ones_like(data_tr[n].magnitude) *
                    tr + n * (num_tr + 1) + 1, '.',
                    markersize=0.1, color='k')
            sig_idx_win = np.where(Js_dict['Js'] >= Js_sig)[0]
            if len(sig_idx_win) > 0:
                x = np.unique(Js_dict['indices']['trial' + str(tr)])
            if len(x) > 0:
                xx = []
                for j in sig_idx_win:
                    xx = np.append(xx, x[np.where(
                        (x * binsize >= t_winpos[j]) &
                        (x * binsize < t_winpos[j] + winsize))])
                ax.plot(
                    np.unique(
                        xx) * binsize,
                    np.ones_like(np.unique(xx)) *
                    tr + n * (num_tr + 1) + 1,
                    ms=ms, marker='s', ls='', mfc='none', mec='r')
        if n < N - 1:
            ax.axhline((tr + 2) * (n + 1), lw=1, color='k')
    ax.set_yticks([1, num_tr//2, num_tr])
    ax.set_yticklabels([1, num_tr//2, num_tr])
    ax.set_ylim(0, (tr + 2) * (n + 1) + 1)
    ax.set_ylabel('Trial')
    ax.set_xlabel('Time [ms]')
    ax.axvline(0*pq.ms, ls='-', color='b', lw=1, alpha=0.5)

if __name__ == '__main__':
    neoObject = NeoObject()
    blk_L = [neoObject.createDataBlock(eID) for eID in neoObject.experimentID]
    for blk in blk_L:
        all_spiketrains = np.array(nt.get_all_spiketrains(blk))
        trial_num = len(blk.segments)
        unit_num  = len(blk.list_units)
        spiketrains = all_spiketrains.reshape(trial_num, unit_num)

        N = len(spiketrains.T)
        UE = ue.jointJ_window_analysis(spiketrains, binsize, winsize, winstep, pattern_hash, method=method)
        plotUEAnalysisFigure(spiketrains, UE, significance_level, binsize, winsize, winstep, pattern_hash, N)
        plt.title('Unitary events of ' + blk.name)
        save_fig('UEanalysis', blk.name)
