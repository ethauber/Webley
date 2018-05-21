# Webley
Solution to Puzzle Question from Webley

### Setup
``` bash
# clone or download

# unzip

# open command prompt

# navigate to unzipped folder

# example run with
python3 webleyPuzzle.py CSVWebley.csv

#usage: python3 webleyPuzzle.py input-file.csv
```

My implementation uses depth first search to find the combinations the sum up to the target number through recursively subtracting from the target number until it reaches zero and adds the qualifying candidates to the solution output.

I do not assume order is maintained and use the sorted() library function.
I allow repeated prices of items so long as they have different names.
I have included input test files that I ran with my program.

Output is written to the terminal and to a statically named file called solutions.csv.
