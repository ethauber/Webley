import sys
import csv
import math
import os
import operator

class Puzzle:

    def __init__(self):
        self.outputList = []
        self.targetPrice = -1
        self.csvPriceList = []
        self.index = 0
        self.currentSum = 0
        self.workingList = []

    def findSumForTarget(self, candidates, target, start, valuelist):
        length = len(candidates)
        if math.isclose(target, 0, rel_tol=1e-09):
            if valuelist not in self.outputList:
                self.outputList.append(valuelist)
            return
        for i in range(start, length):
            #
            j = i + 1
            while (j in range(start, length) and candidates[i] == candidates[j]):
                self.findSumForTarget(candidates, target - float(candidates[j]), j, valuelist + [self.csvPriceList[j]])
                j += 1
            #
            if math.isclose(target, float(candidates[i]), rel_tol=1e-09):
                if (valuelist + [self.csvPriceList[i]]) not in self.outputList:
                    self.outputList.append(valuelist + [self.csvPriceList[i]])
                return
            if target < float(candidates[i]):
                return
            #print('target-candidates:', target-float(candidates[i]), i)
            if (valuelist + [self.csvPriceList[i]]) in self.outputList:
                continue
            self.findSumForTarget(candidates, target - float(candidates[i]), i, valuelist + [self.csvPriceList[i]])

    def parseCSVFile(self):
        try:
            with open(sys.argv[1], 'r') as csvFile:
                csvReaderWithPrices = csv.reader( (row.replace('$', '')) for row in csvFile)
                if os.path.getsize(sys.argv[1]) <= 0:
                    print('ERROR: File is empty.')
                    raise IOError()
                self.targetPrice = float(csvReaderWithPrices.__next__()[1])
                print('targetPrice:', self.targetPrice)
                self.csvPriceList = list( [row[0],row[1]] for row in csvReaderWithPrices)
                self.csvPriceList = sorted(self.csvPriceList, key=operator.itemgetter(1))
                print('csvPriceList: ', self.csvPriceList)
                candidates = list( row[1] for row in self.csvPriceList)
                self.findSumForTarget(candidates, self.targetPrice, 0, self.workingList)
            if len(self.outputList) == 0:
                print('No solutions possible with given prices.')
            else:
                print('Solution(s): ')
                for solutions in self.outputList:
                    print(solutions)

        except IOError:
            print("File:{0} had an input error with csv reader.".format(sys.argv[1]))
        except ValueError:
            print("CSV file is illformated| Values must follow format: item_name, $XX.XX")
        except IndexError:
            print("CSV file is illformated| Parsing file ran into an error in indexing.")

        try:
            with open('./solutions.csv', 'w', newline='') as outputFile:
                fileWriter = csv.writer(outputFile)
                for solutions in self.outputList:
                    fileWriter.writerow(solutions)
        except IOError:
            print("File:solutions.csv had an output error with csv writer.")

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        puzzleObj = Puzzle()
        puzzleObj.parseCSVFile() 
    else:
        print("ERROR: wrong number of arguments")
        print("USAGE: python3 webleyPuzzle.py csv-file")