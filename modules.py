import matplotlib.pyplot as plt
import numpy as np

__all__ = ["LoadData", "MakeParaDic", "SepParaDic", "MatrixFourierSeries", "ChiSquare", "PlotLightCurve", "PlotChiSquare"]

def LoadData():
    """
    Custom light curve load data.

    Returns
    -------
    x : 1-D Array as float
        Demension of 0 contents.
    y : 1-D Array as float
        Demension of 1 contents.

    """
    _data27 = np.loadtxt("data/data_27.txt", delimiter="\t", dtype=str)[1:].astype(float)
    _data28 = np.loadtxt("data/data_28.txt", delimiter="\t", dtype=str)[1:].astype(float)
    x = np.hstack([_data27[:,0], _data28[:,0]+24])
    y = np.hstack([_data27[:,1], _data28[:,1]])
    return x, y

def MakeParaDic(a, P, t0):
    """
    Convert a, P, t0 parameters as dictionary.

    Parameters
    ----------
    a : 1-D Array of Float
        a coefficient of fourier series.
    P : Float
        Period parameter.
    t0 : Float
        Initial time parameter.

    Returns
    -------
    paraDic : Dictionary
        Contained by 'an' series, 'P' and 't0'.

    Examples
    --------
    >>> MakeParaDic(np.array([1.1,0.2,0]), 2.1, 0.2)
    {'a0': 1.1, 'a1': 0.2, 'a2': 0.0, 'P': 2.1, 't0': 0.2}
    """
    paraDic = {}
    for _idx, _a in enumerate(a):
        paraDic["a"+str(_idx)] = a[_idx]
    paraDic["P"] = P
    paraDic["t0"] = t0
    return paraDic

def SepParaDic(paraDic):
    """
    Seperate paraDic value.

    Parameters
    ----------
    paraDic : Dictionary
        Contained by 'an' series, 'P' and 't0'.

    Returns
    -------
    a : 1-D Array as Float
        a coefficient of fourier series.
    P : Float
        Period parameter.
    t0 : Float
        Initial time parameter.

    Examples
    --------
    >>> SepParaDic({'a0': 1.1, 'a1': 0.2, 'a2': 0.0, 'P': 2.1, 't0': 0.2})
    (array([1.1, 0.2, 0. ]), 2.1, 0.2)
    """
    a = []
    for key in paraDic.keys():
        if "a" in key:
            a.append(paraDic[key])
    a = np.array(a)
    P = paraDic["P"]
    t0 = paraDic["t0"]
    return a, P, t0

def CalCosPart(_n, _P, _t0, _theta):
    triIn = 2*_n*np.pi/_P
    return np.cos(triIn*(_theta-_t0))

def MatrixFourierSeries(_a, _P, _t0, theta):
    """
    Calculate Fourier series as multi-dimension.

    Parameters
    ----------
    _a : 1-D Array
        a coefficient of fourier series.
    _P : float or 4-D Array
        Shape muse be (N, 1, 1, 1).
    _t0 : float or 3-D Array
        Shape muse be (N, 1, 1).
    theta : TYPE
        theta parameter of fourier series.

    Returns
    -------
    _results : N-D Array
        Fourier series as multi-dimension matrix array.
    """
    _results = np.vstack(_a) * CalCosPart(np.vstack(np.arange(len(_a))), _P, _t0, theta)
    return _results

def ChiSquare(expect, measure):
    """
    Calculate chi Square values.

    Parameters
    ----------
    expect : N-D Array

    measure : N-D Array
        Must same size about expect value.

    Returns
    -------
    N-D Array

    Examples
    --------
    >>> ChiSquare(np.arange(5), np.arange(5)+2)
    array([4, 4, 4, 4, 4])
    """
    return (expect - measure)**2

def PlotLightCurve(expectXY, measureXY, pathName=None):
    """
    Plot and show or save light curve.

    Parameters
    ----------
    expectXY : 2-D Array
        x, y axis parameters of Line2D.
    measureXY : 2-D Array
        x, y axis parameters of Scatter2D.
    pathName : String, optional
        Graph saving path. The default is None.

    Returns
    -------
    None.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(expectXY[0], expectXY[1], c="gray", label="model")
    plt.scatter(measureXY[0], measureXY[1], c="red", s=1, label="measure")
    plt.xlabel("Hours")
    plt.ylabel("Magnitude")
    plt.xlim(min(expectXY[0]), max(expectXY[0]))
    plt.legend()
    if pathName == None:
        plt.show()
    else:
        plt.savefig(pathName)
        plt.close()
    return None

def PlotChiSquare(chiSquareXY, pathName=None):
    """
    Plot chi square value as bat and show or save.

    Parameters
    ----------
    chiSquareXY : 2-D Array
        x, y axis parameters.
    pathName : String, optional
        Graph saving path. The default is None.

    Returns
    -------
    None.
    """
    plt.figure(figsize=(8, 5))
    xRange = [chiSquareXY[0], chiSquareXY[0]]
    yRange = [np.zeros(len(chiSquareXY[0])), chiSquareXY[1]]
    plt.plot(xRange, yRange, c='b', linewidth=0.5)
    plt.ylim(0, max(yRange[1]*1.1))
    plt.xlim(min(xRange[0])-2, max(xRange[0])+2)
    plt.xlabel("Hours")
    plt.ylabel("Chi Square")
    if pathName == None:
        plt.show()
    else:
        plt.savefig(pathName)
        plt.close()
    return None