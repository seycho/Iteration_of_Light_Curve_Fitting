from modules import *

import matplotlib.pyplot as plt
import numpy as np
import argparse, pickle, os

def CalLeastSquareMat(onesFourier, measure):
    matF = (np.expand_dims(onesFourier, 0) * np.expand_dims(onesFourier, 1)).sum(2)
    matM = np.vstack((onesFourier * measure).sum(1))
    matA = np.matmul(np.linalg.inv(matF), matM)
    return np.hstack(matA)

def main():
    parser = argparse.ArgumentParser(description="Calculate best a_n series parameters.")
    parser.add_argument("--loadpath", type=str, default="None", help="Parameter dictionary saved path")
    parser.add_argument("--savepath", type=str, default="paraDic_least_square.dump",  help="Parameter dictionary export path")
    parser.add_argument("--anum", type=int, default=7, help="Number of a_n term")
    parser.add_argument("--Pinit", type=float, default=None, help="Initial parameter of P")
    parser.add_argument("--t0init", type=float, default=None, help="Initial parameter of t0")
    parser.add_argument("--plotpath", type=str, default="None", help="Plot graph export folder path")
    args = parser.parse_args()

    # Load Data
    dataHours, dataMagni = LoadData()
    if os.path.isfile(args.loadpath):
        paraDic = pickle.load(open(args.loadpath, "rb"))
        a, P, t0 = SepParaDic(paraDic)
    else:
        if args.Pinit != None:
            P = args.Pinit
        else:
            P = 2
        if args.t0init != None:
            t0 = args.t0init
        else:
            t0=0.1

    # Calculate A Matrix
    a = np.ones(args.anum)
    matFourier = MatrixFourierSeries(a, P, t0, dataHours)
    a = CalLeastSquareMat(matFourier, dataMagni)

    # Show
    hours = np.linspace(min(dataHours)-2, max(dataHours)+2, 1000)
    if args.plotpath == "None":
        PlotLightCurve([hours, MatrixFourierSeries(a, P, t0, hours).sum(0)], [dataHours, dataMagni])
        PlotChiSquare([dataHours, ChiSquare(MatrixFourierSeries(a, P, t0, dataHours).sum(0), dataMagni)])
    else:
        plotPath = os.path.join(args.plotpath, "least_square_light_curve.png")
        PlotLightCurve([hours, MatrixFourierSeries(a, P, t0, hours).sum(0)], [dataHours, dataMagni], pathName=plotPath)
        plotPath = os.path.join(args.plotpath, "least_square_chi_square.png")
        PlotChiSquare([dataHours, ChiSquare(MatrixFourierSeries(a, P, t0, dataHours).sum(0), dataMagni)], pathName=plotPath)

    # Export
    pickle.dump(MakeParaDic(a, P, t0), open(args.savepath, "wb"))
    return None

if __name__ == "__main__":
    main()