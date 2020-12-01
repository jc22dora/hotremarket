import numpy as np

def func():

    raw = np.genfromtxt('pyfiles/staticdb.csv', delimiter=',', skip_header=1, dtype=None)
    objList = []
    for i in range(len(raw)):
        objList.append(rowData(raw[i]))
    return tableData(objList)
    
def collectTableData():
    losersRaw = np.genfromtxt('pyfiles/loserdb.csv', delimiter=',', skip_header=1, dtype=None)
    gainersRaw = np.genfromtxt('pyfiles/gainerdb.csv', delimiter=',', skip_header=1, dtype=None)
    losersList, gainersList = [], []
    ln = len(losersRaw)
    for i in range(ln):
        losersList.append(rowData(losersRaw[i]))
        gainersList.append(rowData(gainersRaw[i]))
    return package(tableData(losersList), tableData(gainersList))

class package:
    def __init__(self, losersTableData, gainersTableData):
        self.losers = losersTableData
        self.gainers = gainersTableData

class rowData:
    def __init__(self,row):
        self.zip = row[0]
        self.city = row[1].decode()
        self.state = row[2].decode()
        self.pc = int(100*row[3])

class tableData:
    def __init__(self, objectList):
        self.rowOne = objectList[0]
        self.rowTwo = objectList[1]
        self.rowThree = objectList[2]
        self.rowFour = objectList[3]
        self.rowFive = objectList[4]
        self.rowSix = objectList[5]
        self.rowSeven = objectList[6]
        self.rowEight = objectList[7]
        self.rowNine = objectList[8]
        self.rowTen = objectList[9]