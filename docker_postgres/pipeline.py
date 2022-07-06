import pandas as pd
import sys

print(sys.argv)
day = sys.argv[1]
print('hello world from ' + pd.__version__)
print(f'Today is {day}')