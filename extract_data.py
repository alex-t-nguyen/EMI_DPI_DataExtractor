from DataHandler import get_data
import FileHandler as fh
import pandas as pd
import os
import csv
import sys

#constants
FILE_NAME = 'Result Table.Result'

def main():
    info_type = get_user_input()
    #filename = 'Result Table.Result'
    file_path_list = fh.get_file(os.getcwd())
    if file_path_list:
        try:
            for path in file_path_list:
                os.chdir(path)
                df = get_data(FILE_NAME, info_type)
                df.to_csv('New_Results.csv', sep=',',index = False)
                #print(df)
        except OSError:
            print("Can't create Pandas dataframe.")
            print("Error: " + sys.exc_info()[0])
    else:
        print("\"file_path_list\" is empty")


def get_user_input():
    info_type = raw_input("Select information type: (emission, dpi): ")
    return info_type


if __name__ == "__main__":
    main()