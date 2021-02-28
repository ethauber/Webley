''' Solution for KnapSack Problem on prices '''
import sys
import csv
import math
import os
import operator

class Puzzle:
    ''' Puzzle Object for finding the sum.
        Attributes:
        output_list (list): The list to output
        target_price (int): The price we want the sum for
        csv_price_list (list): List of prices from the csv file
        index (int): where we are currently at in the list
        current_sum (int): The current summation
        working_list (list): The list we are working with currently
    '''
    def __init__(self):
        self.output_list = []
        self.target_price = -1
        self.csv_price_list = []
        self.index = 0
        self.current_sum = 0
        self.working_list = []

    @staticmethod
    def is_zero(val):
        '''Check if float is aproximately zero.
        Can also be done by multiplying by 100 since we only care
        about two decimal places.
        '''
        return math.isclose(float(val), 0, rel_tol=1e-09)

    def is_all_zero(self, candidates):
        '''Checks if candidate list is all zero'''
        print('list ', [val for val in candidates if self.is_zero(val)])
        return bool([
            val for val in candidates if self.is_zero(val)
        ])

    def find_sum_for_target(self, candidates, target, start, value_list):
        '''
        This function finds the sum we are targeting with the
        given items.
        Args:
            candidates (list): Possible answers.
            target (int): The target price sum.
            start (int): Where we should start now in the graph.
            value_list (list): The list of values
        Returns:
            None: Works on this object to create solutions
        '''

        if start == 0 and self.is_all_zero(candidates) and self.is_zero(target):
            self.output_list.append(self.csv_price_list)
            return

        length = len(candidates)
        if self.is_zero(target):
            if value_list not in self.output_list:
                self.output_list.append(value_list)
            return

        for i in range(start, length):
            j = i + 1
            while (j in range(start, length) and candidates[i] == candidates[j]):
                self.find_sum_for_target(
                    candidates, target - float(candidates[j]),
                    j, value_list + [self.csv_price_list[j]]
                )
                j += 1

            if math.isclose(target, float(candidates[i]), rel_tol=1e-09):
                if (value_list + [self.csv_price_list[i]]) not in self.output_list:
                    self.output_list.append(value_list + [self.csv_price_list[i]])
                return
            if target < float(candidates[i]):
                return

            #print('target-candidates:', target-float(candidates[i]), i)
            if value_list + [self.csv_price_list[i]] in self.output_list:
                continue
            self.find_sum_for_target(
                candidates, target - float(candidates[i]), i, value_list + [self.csv_price_list[i]]
            )

    def parse_csv_file(self):
        '''Parses the csv file and also outputs a solution as a file'''
        try:
            with open(sys.argv[1], 'r') as csv_file:
                csv_reader_with_prices = csv.reader( (row.replace('$', '')) for row in csv_file)
                if os.path.getsize(sys.argv[1]) <= 0:
                    print('ERROR: File is empty.')
                    raise IOError()
                self.target_price = float(csv_reader_with_prices.__next__()[1])
                print('target_price:', self.target_price)

                self.csv_price_list = list([row[0],row[1]] for row in csv_reader_with_prices)
                self.csv_price_list = sorted(self.csv_price_list, key=operator.itemgetter(1))
                print('csv_price_list: ', self.csv_price_list)

                candidates = list(row[1] for row in self.csv_price_list)
                self.find_sum_for_target(candidates, self.target_price, 0, self.working_list)

            if len(self.output_list) == 0:
                print('No solutions possible with given prices.')
            else:
                print('Solution(s): ')
                for solutions in self.output_list:
                    print(solutions)

        except IOError:
            print("File:{0} had an input error with csv reader.".format(sys.argv[1]))
        except ValueError:
            print("CSV file is illformated| Values must follow format: item_name, $XX.XX")
        except IndexError:
            print("CSV file is illformated| Parsing file ran into an error in indexing.")

        try:
            with open('./solutions.csv', 'w', newline='') as output_file:
                file_writer = csv.writer(output_file)
                for solutions in self.output_list:
                    file_writer.writerow(solutions)
        except IOError:
            print("File:solutions.csv had an output error with csv writer.")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        puzzleObj = Puzzle()
        puzzleObj.parse_csv_file()
    else:
        print("ERROR: wrong number of arguments")
        print("USAGE: python3 webleyPuzzle.py csv-file")
