from DataHandler import get_data
import FileHandler as fh
import pandas as pd
import os
import csv
import sys
import constants

def main():
    info_type = get_user_input_info()   # User input info type
    dir_path = get_user_input_dir() # User input directory path of root folder containing data files
    #filename = 'Result Table.Result'
    file_path_list = fh.get_file(dir_path)
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


def get_user_input_info():
    """
    Asks user for input for type of data

    :return: type of info as string
    """
    info_type = raw_input("Select information type (emission, dpi): ")
    return info_type


def get_user_input_dir():
    """
    Asks user for input for directory path of folder containing all data

    :return: directory path as string
    """
    dir_path = raw_input("Enter directory path: ")
    return dir_path


def create_new_filename(path):
    """
    Creates new file name for generated .csv file

    :param path: path to directory of .Result file
    :return: name of generated .csv file as string
    """
    file_base_name = path.split('\\')[-1]
    return file_base_name + constants.CSV_FILE_NAME


if __name__ == "__main__":
    main()