import os

def MakeDirTree(pathDir, pathRoot=""):
    pathSplit = pathDir.split('/', 1)
    pathFull = os.path.join(pathRoot, pathSplit[0])
    if not os.path.isdir(pathFull):
        os.mkdir(pathFull)
    if (len(pathSplit[1]) != 0):
        MakeDirTree(pathSplit[1], pathRoot=pathFull)
    return None

def main():
    numCycle = 5
    
    pathParaGDPrevious = "None"
    for _n in range(numCycle):
        pathRoot = "results/%d/"%_n
        pathParaLS = os.path.join(pathRoot, "paraDic_least_square.dump")
        pathParaGD = os.path.join(pathRoot, "paraDic_gradi_descent.dump")
        MakeDirTree(pathRoot)

        option = "--loadpath %s --savepath %s --anum %d --plotpath %s"%(pathParaGDPrevious, pathParaLS, 24, pathRoot)
        commend = "python least_square.py %s"%option
        print(commend)
        os.system(commend)

        option = "--loadpath %s --savepath %s --plotpath %s"%(pathParaLS, pathParaGD, pathRoot)
        commend = "python gradi_descent.py %s"%option
        print(commend)
        os.system(commend)

        pathParaGDPrevious = pathParaGD

    return None

if __name__ == "__main__":
    main()
