from multiprocessing import Pool
import matplotlib.pyplot as plt
import numpy as np
import pickle

def FourierSeries(_paraDic, theta):
    _a = []
    for key in _paraDic.keys():
        if "a" in key:
            _a.append(_paraDic[key])
    _P = _paraDic["P"]
    _t0 = _paraDic["t0"]
    _results = np.zeros(len(theta), dtype=float)
    for _n in range(len(_a)):
        triIn = _n*np.pi/_P
        _b_n = np.cos(triIn*_t0)
        _b_ns = np.sin(triIn*_t0)
        _results += _a[_n]*(_b_n*np.cos(triIn*theta)+_b_ns*np.sin(triIn*theta))
        #_results += _a[_n]*np.cos(triIn*(theta-_t0))
    return _results

def ChiSquare(expect, measure):
    return np.sum(((expect - measure)/len(expect))**2)

def MakeParaDic(a, P, t0):
    paraDic = {}
    for _idx, _a in enumerate(a):
        paraDic["a"+str(_idx)] = a[_idx]
    paraDic["P"] = P
    paraDic["t0"] = t0
    return paraDic

def MultiCalFuc(_variableDic):
    _num = _variableDic["num"]
    _vSepList = _variableDic["vSepList"]
    _idxMatList = []
    _chiMatList = []
    for _idxList in indexComb[indexCombSlice[_num]:indexCombSlice[_num+1]]:
        _idxMat = tuple(_idxList)
        for _idx, _key in enumerate(paraList):
            paraDicNew[_key] = _vSepList[_key][_idxMat[_idx]]
        _chiMatList.append(ChiSquare(FourierSeries(paraDicNew, time), magnitude))
        _idxMatList.append(_idxMat)
    return _idxMatList, _chiMatList

time = []
magnitude = []
_tmp = np.loadtxt("../data/data_27.txt", delimiter="\t", dtype="str")
time.append(_tmp[1:,0].astype(float))
magnitude.append(_tmp[1:,1].astype(float))
_tmp = np.loadtxt("../data/data_28.txt", delimiter="\t", dtype="str")
time.append(24+_tmp[1:,0].astype(float))
magnitude.append(_tmp[1:,1].astype(float)-0.15)
time = np.hstack(time)
magnitude = np.hstack(magnitude)

aList = []
PList = []
t0List = []
chiSList = []

#a = np.array([10.9, -0.28, 0.52, 0.59, 0.51, -0.07, -0.35, -0.32, 0.01, 0.21, 0.21, 0.04, -0.05])
a = np.array([11, -0.28, 0.52, 0.59, 0.51, -0.07, -0.35])
P = 2.66
t0 = 0.49
paraDic = MakeParaDic(a, P, t0)
paraDicNew = paraDic.copy()
deltaDic = paraDic.copy()
for key in deltaDic.keys():
    deltaDic[key] = 0.1
deltaDic["P"] = 0.01
deltaDic["t0"] = 0.01

sepNum = 5
processNum = 16
paraList = list(paraDic.keys())
scoreMat = np.zeros(np.ones(len(paraList),dtype=int)*sepNum)

vSepList = {}
inputCom = []
for key in paraList:
    vSepList[key] = np.linspace(paraDic[key]-deltaDic[key], paraDic[key]+deltaDic[key], sepNum)
    inputCom.append(range(sepNum))
indexComb = np.array(np.meshgrid(*inputCom)).T.reshape(-1, len(paraList))
indexCombSlice = np.linspace(0, len(indexComb)+processNum, processNum+1).astype(int)

if __name__ == '__main__':
    for num in range(10):
        print(num)
        
        numList = np.arange(processNum)
        variableDic = []
        for i in range(len(numList)):
            variableDic.append({"num" : numList[i], "vSepList" : vSepList})
        
        with Pool(processNum) as p:
            mpResultList = p.map(MultiCalFuc, variableDic)
            
        for _idxMatList, _chiMatList in mpResultList:
            for _idx, _chi in zip(_idxMatList, _chiMatList):
                scoreMat[_idx] = _chi
        _idxMin = np.array(np.where(scoreMat == scoreMat.min()))[:,0]
        for _idx, key in enumerate(paraList):
            if _idxMin[_idx] == sepNum-1:
                paraDic[key] += deltaDic[key]
            elif _idxMin[_idx] == 0:
                paraDic[key] -= deltaDic[key]
            else:
                deltaDic[key] /= 2
        for key in paraList:
            vSepList[key] = np.linspace(paraDic[key]-deltaDic[key], paraDic[key]+deltaDic[key], sepNum)

    x = np.linspace(20, 50, 1000)
    plt.figure(figsize=(8, 5))
    plt.plot(x, FourierSeries(paraDic, x), c="gray", label="model")
    plt.scatter(time, magnitude, s=2, c="red", label="measure")
    plt.xlabel("time (hour)")
    plt.ylabel("magnitude")
    plt.legend()
    plt.ylim(11.8, 10.6)
    plt.show()
    
    pickle.dump(scoreMat, open("LC_fitting_gradi_matrix.dump", "wb"))
    pickle.dump(paraDic, open("LC_fitting_parameter.dump", "wb"))

    gradiMat = np.zeros([101, 101])
    for idx1, v1 in enumerate(np.linspace(paraDic["P"]-0.1, paraDic["P"]+0.1, 101)):
        for idx2, v2 in enumerate(np.linspace(paraDic["t0"]-0.1, paraDic["t0"]+0.1, 101)):
            paraDicNew["P"] = v1
            paraDicNew["t0"] = v2
            gradiMat[idx1, idx2] = ChiSquare(FourierSeries(paraDicNew, time), magnitude)
    plt.imshow(gradiMat)
    plt.show()

    print(paraDic)