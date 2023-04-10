import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

time = []
magnitude = []
_tmp = np.loadtxt("../data/data_27.txt", delimiter="\t", dtype="str")
time.append(_tmp[1:,0].astype(float))
magnitude.append(_tmp[1:,1].astype(float))
_tmp = np.loadtxt("../data/data_28.txt", delimiter="\t", dtype="str")
time.append(24+_tmp[1:,0].astype(float))
magnitude.append(_tmp[1:,1].astype(float))
time = np.hstack(time)
magnitude = np.hstack(magnitude)

def FourierSeries(num, _a, _P, _t0, theta):
    _results = np.zeros(len(theta), dtype=float)
    for _n in range(num):
        triIn = _n*np.pi/_P
        _b_nc = np.cos(triIn*_t0)
        _b_ns = np.sin(triIn*_t0)
        _results += _a[_n]*(_b_nc*np.cos(triIn*theta)+_b_ns*np.sin(triIn*theta))
    return _results

def ChiSquare(expect, measure):
    return np.sum(((expect - measure)/len(expect))**2)

def CornerPlot(paraDic, chiSList):
    idxMin = np.argmin(chiSList)
    
    paraList = list(paraDic.keys())
    for _idx in range(len(paraList)):
        xLabel = paraList[_idx]
        for _idx2 in range(_idx):
            yLabel = paraList[_idx2]
            mat, x, _, _ = plt.hist2d(paraDic[paraList[_idx]], paraDic[paraList[_idx2]], norm=mpl.colors.LogNorm(), bins=200, cmap="seismic")
            plt.xlabel(xLabel)
            plt.ylabel(yLabel)
            plt.show()
            #plt.plot(x[:-1], mat.sum(1))
            #plt.show()

    return None

aList = []
PList = []
t0List = []
chiSList = []
#a = np.array([10.9, -0.28, 0.52, 0.59, 0.51, -0.07, -0.35, -0.32, 0.01, 0.21, 0.21, 0.04, -0.05])
#a = np.array([10.9, 0, 0, 0, 0, 0, 0, 0, 0])
a = np.array([10.9, 0, 0, 0, 0])
P = 5.64
t0 = 0.472
chiS = -1

i = 0
iRe = 0
num = 350000
while (i < num):
    aN = np.random.normal(a, 0.01)
    PN = np.random.normal(P, 0.01)
    t0N = np.random.normal(t0, 0.01)
    resultsN = FourierSeries(len(aN), aN, PN, t0N, time)
    chiSN = ChiSquare(resultsN, magnitude)
    iRe += 1
    if np.random.rand() > (chiSN / chiS):
        a = aN
        P = PN
        t0 = t0N
        chiS = chiSN
        aList.append(a)
        PList.append(P)
        t0List.append(t0)
        chiSList.append(chiS)
        i += 1
        if i % 100 == 0:
            print("%d/%d"%(i, num))
    if (chiS < 0.0001 or iRe > 1e4):
        iRe = 0
        a = np.random.normal(a, 0.1)
        P = np.random.normal(P, 0.1)
        t0 = np.random.normal(t0, 0.1)
        chiS = -1

idxB = np.argmin(chiSList)
aB = aList[idxB]
PB = PList[idxB]
t0B = t0List[idxB]

x = np.linspace(20, 50, 1000)
plt.plot(x, FourierSeries(len(aB), aB, PB, t0B, x), c="black")
plt.scatter(time, magnitude, s=0.5, c="red")
plt.show()

paraDic = {}
aArray = np.array(aList)
for _idx, _a in enumerate(a):
    paraDic["a"+str(_idx)] = aArray[:,_idx]
paraDic["P"] = PList
paraDic["t0"] = t0List

CornerPlot(paraDic, chiSList)