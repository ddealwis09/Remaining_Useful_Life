import sys
from pathlib import Path
import pandas as pd

path = Path(__file__).parent.parent.parent.resolve()
filename = 'data/raw/train_FD001.txt'
fullpath = path.joinpath(filename)
data = pd.read_csv(fullpath)

print(data)


