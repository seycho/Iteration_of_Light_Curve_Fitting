from modules import *

import matplotlib.pyplot as plt
import numpy as np
import argparse, pickle, os

def RetakeRange(vList, idx, vDelta, matScore, dim):
    retake = True
    condiNot0 = np.mean(np.diff(matScore, axis=dim)**2) > 0
    condiDelta = vDelta > 0.01
    if condiNot0 * condiDelta:
        v = vList[idx[dim]]
        if idx[dim] - len(vList) // 2 != len(vList) // 2:
            vDelta /= 2
        vList = np.linspace(v-vDelta, v+vDelta, len(vList))
    else:
        retake = False
    return vList, vDelta, retake

def MakeChiSquareMultiDim(a, hList, vList, data, measure):
    hListMultiDim = np.expand_dims(np.expand_dims(np.expand_dims(hList, 1), 1), 1)
    vListMultiDim = np.expand_dims(np.expand_dims(vList, 1), 1)
    matFourier = MatrixFourierSeries(a, hListMultiDim, vListMultiDim, data)
    matChisqua = ChiSquare(matFourier.sum(2), measure).sum(2)
    return np.nan_to_num(matChisqua, nan=np.inf)

def main():
    parser = argparse.ArgumentParser(description="Find best P, t0 parameters.")
    parser.add_argument("--loadpath", type=str, default="paraDic_least_square.dump", help="Parameter dictionary saved path")
    parser.add_argument("--savepath", type=str, default="paraDic_gradi.dump",  help="Parameter dictionary export path")
    parser.add_argument("--num", type=int, default=103, help="Space num of width")
    parser.add_argument("--Pinit", type=float, default=None, help="Initial parameter of P")
    parser.add_argument("--t0init", type=float, default=None, help="Initial parameter of t0")
    parser.add_argument("--Pwidth", type=float, default=3, help="Search range of P parameter")
    parser.add_argument("--t0width", type=float, default=2, help="Search range of t0 parameter")
    parser.add_argument("--plotpath", type=str, default="None", help="Plot graph export folder path")
    args = parser.parse_args()

    # Load Data
    dataHours, dataMagni = LoadData()
    paraDic = pickle.load(open(args.loadpath, "rb"))
    a, P, t0 = SepParaDic(paraDic)

    # Initialization
    numSep = args.num
    if args.Pinit != None:
        P = args.Pinit
    if args.t0init != None:
        t0 = args.t0init
    PDelta = args.Pwidth
    t0Delta = args.t0width
    if PDelta == 0:
        PDelta = 3
    if t0Delta == 0:
        t0Delta = 2
    PList = np.linspace(P-PDelta, P+PDelta, numSep)
    t0List = np.linspace(t0-t0Delta, t0+t0Delta, numSep)
    PRetake, t0Retake = True, True

    # Find Minima
    record = {}
    record["P"] = []
    record["t0"] = []
    while PRetake + t0Retake:
        matChisqua = MakeChiSquareMultiDim(a, PList, t0List, dataHours, dataMagni)
        idxMin = np.array(np.where(matChisqua == matChisqua.min())).T
        if len(idxMin) > 0:
            idxMin = idxMin[len(idxMin) // 2]
        else:
            idxMin = idxMin[0]

        if args.plotpath == "None":
            plt.imshow(matChisqua)
            plt.title("P=%.2f, t0=%.2f"%(PList[idxMin[0]], t0List[idxMin[1]]))
            plt.xlabel("P(%.2f~%.2f)"%(min(PList), max(PList)))
            plt.ylabel("t0(%.2f~%.2f)"%(min(t0List), max(t0List)))
            plt.scatter(idxMin[0], numSep-1-idxMin[1], c="red")
            plt.xticks([])
            plt.yticks([])
            plt.show()

        record["P"].append(PList[idxMin[0]])
        record["t0"].append(t0List[idxMin[1]])
        PList, PDelta, PRetake = RetakeRange(PList, idxMin, PDelta, matChisqua, 0)
        t0List, t0Delta, t0Retake = RetakeRange(t0List, idxMin, t0Delta, matChisqua, 1)
    PLast, t0Last = record["P"][-1], record["t0"][-1]

    # Show
    if args.plotpath == "None":
        PLast, t0Last = record["P"][-1], record["t0"][-1]
        PWidth = max(np.abs([PLast - min(record["P"]), PLast - max(record["P"])]))+0.1
        t0Width = max(np.abs([t0Last - min(record["t0"]), t0Last - max(record["t0"])]))+0.1
        PList = np.linspace(PLast-PWidth, PLast+PWidth, numSep)
        t0List = np.linspace(t0Last-t0Width, t0Last+t0Width, numSep)
        matChisqua = matChisqua = MakeChiSquareMultiDim(a, PList, t0List, dataHours, dataMagni)
        PPath = (np.array(record["P"]) - PLast + PWidth) / 2 / PWidth * numSep
        t0Path = (np.array(record["t0"]) - t0Last + t0Width) / 2 / t0Width * numSep
    
        plt.figure(figsize=(8, 8))
        plt.imshow(matChisqua, cmap="gray")
        plt.plot(PPath, numSep-1-t0Path, c="red")
        plt.title("P=%.2f, t0=%.2f"%(PLast, t0Last))
        plt.xlabel("P(%.2f~%.2f)"%(min(PList), max(PList)))
        plt.ylabel("t0(%.2f~%.2f)"%(min(t0List), max(t0List)))
        plt.xticks([])
        plt.yticks([])
        plt.show()

    P = PLast
    t0 = t0Last
    hours = np.linspace(min(dataHours)-2, max(dataHours)+2, 1000)
    if args.plotpath == "None":
        PlotLightCurve([hours, MatrixFourierSeries(a, P, t0, hours).sum(0)], [dataHours, dataMagni])
        PlotChiSquare([dataHours, ChiSquare(MatrixFourierSeries(a, P, t0, dataHours).sum(0), dataMagni)])
    else:
        plotPath = os.path.join(args.plotpath, "gradi_descent_light_curve.png")
        PlotLightCurve([hours, MatrixFourierSeries(a, P, t0, hours).sum(0)], [dataHours, dataMagni], pathName=plotPath)
        plotPath = os.path.join(args.plotpath, "gradi_descent_chi_square.png")
        PlotChiSquare([dataHours, ChiSquare(MatrixFourierSeries(a, P, t0, dataHours).sum(0), dataMagni)], pathName=plotPath)

    # Export
    pickle.dump(MakeParaDic(a, P, t0), open(args.savepath, "wb"))
    return None


if __name__ == "__main__":
    main()