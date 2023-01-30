import pandas as pd
from pathlib import Path
import sys

path = Path(__file__).parent.parent.parent.resolve()
filename = 'data/raw/train_FD001.txt'

fullpath = path.joinpath(filename)

print(fullpath)

data = pd.read_csv(fullpath)

print(data.head(2))


"""
import sys
sys.path.insert(0, '/Users/dinushdealwis/Documents/ML_Projects/RUL/notebooks')

from test import donny

d = donny(3,4)
print(d)

"""


