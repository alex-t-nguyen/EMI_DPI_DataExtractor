from DataHandler import get_data
import FileHandler as fh
import pandas as pd
import os
import csv
import sys
import constants

#constants
#FILE_NAME = 'Result Table.Result'
#CSV_FILE_NAME = '_New_Results.csv'

def main():
    info_type = get_user_input()
    #filename = 'Result Table.Result'
    file_path_list = fh.get_file(os.getcwd())
    if file_path_list:
        try:
            for path in file_path_list:
                os.chdir(path)
                df = get_data(constants.FILE_NAME, info_type)
                new_filename = create_new_filename(path)
                df.to_csv(new_filename, sep=',',index = False)
                #print(df)
        except OSError:
            print("Can't create Pandas dataframe.")
            print("Error: " + sys.exc_info()[0])
    else:
        print("\"file_path_list\" is empty")


def get_user_input():
    info_type = raw_input("Select information type: (emission, dpi): ")
    return info_type


def create_new_filename(path):
    file_base_name = path.split('\\')[-1]
    return file_base_name + constants.CSV_FILE_NAME


if __name__ == "__main__":
    main()