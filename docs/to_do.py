# subset aircraft table while preserving unit_number order in upload file
# https://stackoverflow.com/questions/56658723/how-to-maintain-order-when-selecting-rows-in-pandas-dataframe

# make prediction on input file
# return join file with predictions which depend on the threshold and yes/no filter selected by user
# store sensor names list and rename columns of inout file

import pandas as pd
import numpy as np

a = pd.DataFrame([[1,2,3],[3,3,1],[1,4,1]], columns=['a','b', 'c'])
print(a.c.unique())


#joined = a.join(b, on='unit_number', how='inner')
#print(joined.iloc[:,-2:])

