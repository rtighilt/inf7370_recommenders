import ntpath
import os
import pandas as pd
import pickle

class FileReader:
    path = ""
    shape = []
    head_only = False
    num_rows = 10
    data = None

    def __init__(self, filepath, shape, head_only=False, num_rows=0):
        self.path = filepath
        self.shape = shape
        self.head_only = head_only
        self.num_rows = num_rows
        print("Reading file " + self.path)
        if os.path.exists(r'dataframes/' + ntpath.basename(filepath[:-3])):
            self.load_data_from_binary(ntpath.basename(filepath[:-3]))
        else:
            self.read().save_data_to_binary(ntpath.basename(filepath[:-3]))

    def read(self):
        """ Reading the file from csv, and returning a dataframe with only a few data if specified"""
        df = pd.read_csv(self.path)
        df = df[self.shape]
        if self.head_only:
            self.data = df.applymap(str).head(self.num_rows).replace(r'^\s*$', "Unknown", regex=True)
        else:
            self.data = df.applymap(str).replace(r'^\s*$', "Unknown", regex=True)
        return self

    def get_data(self):
        return self.data

    def load_data_from_binary(self, path):
        file = open(r'dataframes/' + path, 'rb')
        self.data = pickle.load(file)
        file.close()

    def save_data_to_binary(self, path):
        file = open(r'dataframes/' + path, 'wb+')
        pickle.dump(self.data, file)
        file.close()