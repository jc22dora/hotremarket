import pandas as pd
import numpy as np
import math
import pyfiles
from operator import itemgetter
rawWithHeading = np.genfromtxt('./pyfiles/ZillowZIPData.csv', delimiter=',',dtype=None)
raw = np.genfromtxt('./pyfiles/ZillowZIPData.csv', delimiter=',', skip_header=1)
stringdf = raw[:,:9]
df = raw[:,9:]
num_rows, num_cols = df.shape
validCols = np.empty(num_rows)
meanVector = np.empty(num_rows)
RIV = np.empty(num_rows)
pcVector = np.empty(num_rows)
pcTopTen = []
RIVTopTen = []
dateVector = rawWithHeading[0,9:rawWithHeading.shape[1]]

def testFunc():
    findDataPoints()
    #calculateMean()
    #calculateRIV()
    #calculatePC()

    
""" 
Status: Done
Fill in column vector, validCols, with the number of datapoints for row r.
rtype: none
"""
def findDataPoints():
    for i, row in enumerate(df):
        numMissing = 0
        for j, col in enumerate(row):
            if np.isnan(row[j]) == True:
                numMissing += 1

        validCols[i] = num_cols-numMissing


""" 
Status: Not Done
[description]
rtype: 
"""
def calculateMean():
    for i, row in enumerate(df):
        isum = np.nansum(row)
        imean = isum/validCols[i]
        meanVector[i] = imean

""" 
Status: Not Done
[description]
rtype: 
"""
def calculateRIV():
    for i, row in enumerate(df):
        min = np.nanmin(row)
        max = np.nanmax(row)
        delta = max-min
        RIV[i] = delta/meanVector[i]

""" 
Status: Not Done
[description]
rtype: 
"""
def calculatePC():
    for i, row in enumerate(df):
        ind = int(num_cols-validCols[i])
        first = row[ind]
        last = row[num_cols-1]
        pcVector[i] = (last-first)/first

def findDateIndex(someDate):
    ln, i = len(dateVector), 0
    while i < ln:
        if dateVector[i].decode() == someDate:
            return i
        i += 1



def calculateGenericPC(rowIndex, firstDateIndex, lastDateIndex):
    first = df[rowIndex, firstDateIndex]
    last = df[rowIndex, lastDateIndex]
    pc = (last - first)/first
    return pc

""" 
Status: Not Done
[description]
rtype: 
"""
def findTop(arr):
    return np.argmax(arr)

""" 
Status: Not Done
[description]
rtype: 
"""
def findBottom(arr):
    return np.argmin(arr)


def findBottomTenZIP(arr):
    sorted = np.argsort(arr)
    sorted = sorted[:10]
    for i in range(10):
        sorted[i] = getZIP(sorted[i])
    return sorted

def findTopTenZIP(arr):
    sorted = np.argsort(arr)
    sorted = sorted[num_rows-11:]
    for i in range(10):
        sorted[i] = getZIP(sorted[i])
    return sorted

""" 
Status: Done
Accepts zip string and returns its index
rtype: int
"""
def findZipIndex(zip):
    i, zip = 0, float(zip)
    zipVector = stringdf[:,2]
    while i < num_rows:
        if int(zipVector[i]) == int(zip):
            return i
        i += 1

def findPCDateRange(zip, firstDate, lastDate):
    ln = len(dateVector)
    zipIndex = findZipIndex(zip)
    i, lastDateIndex, firstDateIndex = 0, findDateIndex(lastDate), findDateIndex(firstDate)
    return calculateGenericPC(zipIndex, firstDateIndex, lastDateIndex)

def findTopTenRIVDateRange(firstDate, lastDate):
    pass

def findYTD(zip):
    zipIndex, firstDateIndex, lastDateIndex = findZipIndex(zip), 288, 296
    return calculateGenericPC(zipIndex, firstDateIndex, lastDateIndex )


def createLosersObj(listOfLosers):
    loserList = []
    for i in range(len(listOfLosers)):
        loserList.append(Losers(findZipIndex(listOfLosers[i])))

    return loserList

def getCity(rowIndex):
    return rawWithHeading[rowIndex+1,6].decode()

def getState(rowIndex):
    return rawWithHeading[rowIndex+1, 5].decode()

def getValue(rowIndex):
    return pcVector[rowIndex]

def createListForDB():
    losers, gainers = [], []
    losersZip, gainersZip = findBottomTenZIP(getPC()), findTopTenZIP(getPC())
    for i in range(10):
        currLoserIndex = findZipIndex(losersZip[i])
        currGainIndex = findZipIndex(gainersZip[i])
        losers.append([losersZip[i], getCity(currLoserIndex), getState(currLoserIndex), getValue(currLoserIndex)])
        gainers.append([gainersZip[i], getCity(currGainIndex), getState(currGainIndex), getValue(currGainIndex)])

    package = [losers, gainers]
    return package

def createPCVectorForDB():
    newVector, ln = [], len(pcVector)
    sorted = np.argsort(pcVector)
    for i in range(ln):
        j = sorted[i]
        newVector.append([getZIP(j),pcVector[j]])
    return newVector

def writeDB():
    pack = createListForDB()
    dbmod.fillLoserDB(pack[0])
    dbmod.fillGainerDB(pack[1])

class Losers:
    def __init__(self, rowIndex):
        self.zip = getZIP(rowIndex)
        self.city = getCity(rowIndex)
        self.state = getState(rowIndex)
        self.value = getValue(rowIndex)


def velocityAlgo():
    inclusiveVector = []
    
    maxPoints = validCols[0]

    ln = len(validCols)
    for i in range(ln):
        if validCols[i] == maxPoints:
            currList = [] #"[index, zip]"
            currList.append(i)
            currList.append(getZIP(i))
            currList.append(calculateGenericPC(i,0,228))
            currList.append(calculateGenericPC(i,228,296))
            inclusiveVector.append(currList)
    
    #initialRank = inclusiveVector[inclusiveVector[:,2].argsort()]
    initialRank = sorted(inclusiveVector, key=itemgetter(2))
    #postRank = inclusiveVector[inclusiveVector[:,3].argsort()]
    postRank = sorted(inclusiveVector, key=itemgetter(3))

    ln = len(initialRank)
    for i in range(ln):
        initIndex, postIndex = findRankIndexes(initialRank, postRank, i)
        currList = inclusiveVector[i]
        currList.append(postIndex-initIndex)

    sortedVelocity = sorted(inclusiveVector, key=itemgetter(4))

    #return [initialRank, postRank]
    return sortedVelocity
    
def findRankIndexes(initRank, postRank, i):
    initIndex, postIndex = 0, 0
    for j in range(len(initRank)):
        currInit = initRank[j]
        currPost = postRank[j]
        if int(currInit[0]) == i:
            initIndex = j
        if int(currPost[0]) == i:
            postIndex = j
    return initIndex, postIndex
    

"""""""""
"""""""""   
"""""""""
GETTERS
"""""""""
"""""""""
"""""""""            


"""
Status: Done
Returns dataframe to user.
This was created for use during testing, might be deleted in future. 
rtype: dataframe
"""
def getData():
    return df

def getRawData():
    return rawWithHeading

def getCols():
    return num_cols

"""
Status: Done
Returns validCols to user
rtype: np.array 
"""        
def getValidCols():
    return validCols

def getSum(arr):
    return np.sum(arr)

def getMeanVector():
    return meanVector

def getRIV():
    return RIV

def getPC():
    return pcVector

def getTopRIV():
    return findTop(RIV)

def getBottomRIV():
    return findBottom(RIV)

def getTopPC():
    return findTop(pcVector)

def getBottomPC():
    return findBottom(pcVector)

def getZIP(index):
    return stringdf[index][2]

def getTopPCZip():
    return getZIP(getTopPC())
def getTopRIVZip():
    return getZIP(getTopRIV())
def getBottomPCZip():
    return getZIP(getBottomPC())
def getBottomRIVZip():
    return getZIP(getBottomRIV())

def getpcTopTen():
    return findTopTenZIP(pcVector)
def getRIVTopTen():
    return findTopTenZIP(RIV)