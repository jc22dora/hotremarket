
import csv



#let rows be a list of lists
# ex:

#rows = [['12549', 'Montgomery','NY','.10'],
# ['02145', 'Somerville','MA','.125'],
# ['01801', 'Woburn','MA','.321']]
def fillLoserDB(rows):
    fields = ('Zip','City','State','PC')
    with open("loserdb.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

def fillGainerDB(rows):
    fields = ('Zip','City','State','PC')
    with open("gainerdb.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

def fillRankVector(pcVector):
    fields = ('Zip','PC')
    with open("pcvectordb.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(pcVector)

def getZIPRank(zip):
    with open("./pyfiles/pcvectordb.csv", 'r') as csvfile: 
        csvreader = csv.reader(csvfile)
        next(csvreader)
        i = 1
        for row in csvreader:
            j = int(float(row[0]))
            if j == zip:
                return calculateRank(i,30367)
            i += 1
        return 'invalid'

def getZIPData(zip):
    with open("./pyfiles/ZillowZIPData.csv", 'r') as csvfile: 
        csvreader = csv.reader(csvfile)
        dates = next(csvreader)
        i = 1
        for row in csvreader:
            currZip = int(float(row[2]))
            if currZip == zip:
                rowData = row[9:]
                empty = ['']*len(rowData)
                empty = dates[9:]
                return [empty, rowData]

def getPCVectorFromDB():
     with open("./pyfiles/pcvectordb.csv", 'r') as csvfile: 
        csvreader = csv.reader(csvfile)
        next(csvreader)
        vec = []
        empty = []
        for lines in csvreader:
            vec.append(lines[1])
            empty.append('')
        return [empty, vec]



def calculateRank(rank, ln):
    return [rank, rank/ln]






