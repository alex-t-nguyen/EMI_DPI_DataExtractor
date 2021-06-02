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
    overwrite = get_user_input_overwrite()

    file_path_list = []
    
    correct_mode = False
    while not correct_mode: # Get user input for mode
        mode = get_user_input_mode()
        if mode.lower() == constants.MODE_SELECTIVE:    # Mode is selective
            file_path_list = fh.get_dir(dir_path, overwrite)
            correct_mode = True
        elif mode.lower() == constants.MODE_GENERAL:    # Mode is general
            file_path_list = fh.get_file(dir_path, overwrite)
            correct_mode = True
        else:
            print("Invalid mode type.")

    if file_path_list:
        try:
            for path in file_path_list:
                os.chdir(path)
                df = get_data(constants.FILE_NAME, info_type)
                new_filename = create_new_filename(path)
                df.to_csv(new_filename, sep=',',index = False)
                #print(df)
            if mode.lower() == constants.MODE_SELECTIVE:    # Mode is selective
                print("\".csv\" files for all selected \".Result\" files successfullly created.")
            else:    # Mode is general
                print("\".csv\" files for all \".Result\" files successfullly created.")
        except OSError:
            print("Can't create Pandas dataframe.")
            print("Error: " + sys.exc_info()[0])


def get_user_input_info():
    """
    Asks user for input for type of data.\n

    :return: type of info as string.
    """
    info_type = raw_input("Select information type (emission, dpi): ")
    return info_type


def get_user_input_dir():
    """
    Asks user for input for directory path of folder containing all data.\n

    :return: directory path as string.
    """
    dir_path = raw_input("Enter directory path: ")
    return dir_path


def get_user_input_mode():
    mode = raw_input("Enter data extraction mode (General, Selective): ")
    return mode


def get_user_input_overwrite():
    overwrite_flag = False
    overwrite = False
    while not overwrite_flag:
        input_overwrite = raw_input("Overwrite current \".csv\" files (Y/N)? ")
        if input_overwrite.lower() == "y" or input_overwrite.lower() == "yes":
             overwrite = True
             overwrite_flag = True
        elif input_overwrite.lower() == "n" or input_overwrite.lower() == "no":
            overwrite = False
            overwrite_flag = True

    return overwrite


def create_new_filename(path):
    """
    Creates new file name for generated .csv file.\n

    :param path: path to directory of .Result file.\n
    :return: name of generated .csv file as string.
    """
    file_base_name = path.split('\\')[-1]
    return file_base_name + constants.CSV_FILE_NAME


if __name__ == "__main__":
    main()