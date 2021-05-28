from DataHandler import getData
import pandas as pd
from Signal import Signal
import os
import shutil
import csv

def main():
    filename = 'Result Table.Result'
    
    csv_columns = ["Frequency","Level"]
    try:
        df = getData(filename)
        df.to_csv('New_Results.csv', sep=',',index = False)
        print(df)
    except OSError:
        print("Can't create Pandas dataframe")


if __name__ == "__main__":
    main()