import numpy as np
import matplotlib.pyplot as plt
from quantities import ms
from neo.core import Block, Segment, ChannelIndex, Unit, SpikeTrain, AnalogSignal, Event
from NeoObject import NeoObject
import elephant.conversion as econv
from experimentData import ExperimentData
from sklearn.grid_search import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.base import clone
from saveFig import save_fig

rbf_kernel_svm_clf = Pipeline([
    ("imputer", Imputer(missing_values='NaN', strategy='mean', axis=0)),
    ("scaler", StandardScaler()),
    ("svm_clf", SVC(kernel="rbf", gamma=5, C=0.001))
])

neoObject = NeoObject()
blk_L = [neoObject.createDataBlock(eID) for eID in neoObject.experimentID]

for blk in blk_L:
    segments = blk.segments
    list_units = blk.list_units

    y = []
    for seg in segments:
        trTarget = seg.annotations['trTarget']
        y.append(trTarget)
    y = np.array(y)

    for unit in list_units:
        print(unit.name)
        spiketrains = unit.spiketrains
        st_matrix = np.array([econv.BinnedSpikeTrain(st, binsize=50*ms).to_array() for st in spiketrains])
        st_matrix = st_matrix.reshape(len(spiketrains), -1)

        clf = clone(rbf_kernel_svm_clf)

        X_train, X_test, y_train, y_test = train_test_split(st_matrix, y, test_size=0.2)

        clf.fit(X_train, y_train)
        print(cross_val_score(clf, X_train, y_train, cv=3, scoring="accuracy"))
