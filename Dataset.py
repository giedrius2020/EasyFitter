import pandas as pd
import numpy as np


class Dataset:
    def __init__(self, data, tab_name):
        self.df = pd.DataFrame(data, columns=['x', 'y'])
        self.tab_name = tab_name
        self.convert_to_float()
        # self.log10()

    def convert_to_float(self):
        # Convert all values to float
        self.df = self.df.apply(pd.to_numeric, errors='coerce')

    def log10(self):
        # Apply log10 to the column
        self.df['y'] = self.df['y'].apply(np.log10)








