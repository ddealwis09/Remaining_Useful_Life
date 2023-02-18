from pathlib import Path

# get training data
path = Path(__file__).parent.parent.parent.resolve()

folder = 'models/current/'
par_path = path.joinpath(folder)
filename = "saved_step2.pkl"
fullpath = par_path.joinpath(filename)

print(fullpath)







