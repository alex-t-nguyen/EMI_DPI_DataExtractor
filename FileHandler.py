import os
from extract_data import create_new_filename
import constants
import pandas as pd
import re

def get_file(root_dir, overwrite=False):
    """
    Gets all directory paths in root folder for all .Result files that don't have a corresponding .csv file.\n

    :param root_dir: root directory to search for all .Result files in.\n
    :return: list of directory paths for .Result files without a corresponding .csv file.
    """
    file_path_list = []

    for (root, dirs, files) in os.walk(root_dir, topdown=True): # Walk through all folders in root_dir
        if constants.DATA_FILE_NAME in files: # if .Result file is in folder
            csv_file_name = create_new_filename(root)   # new .csv file name
            if overwrite:
                file_path_list.append(root)
            else:
                if csv_file_name not in files:  # if .csv file for corresponding .Result file is not in folder
                    file_path_list.append(root) # Add folder path to list to create .csv later on
                
    if not file_path_list:
        print("All \"Result Table.Result\" files already have corresponding \"New_Results.csv\" files.")
    return file_path_list


def get_dir(root_dir, overwrite=False):
    """
    Gets all directory paths in root folder for all SELECTED .Result files.\n
    Overwrites previous ".csv" file if one already exists

    :param root_dir: root directory to search for all SELECTED .Result files in.\n
    :return: list of directory paths for .Result files.
    """
    folder_properties = []
    folder_list = []

    for (root, dirs, files) in os.walk(root_dir, topdown=True): # Walk through all folders in root_dir 
        if constants.DATA_FILE_NAME in files: # if .Result file is in 
            del folder_properties[:]
            csv_file_name = create_new_filename(root)   # new .csv file name
            if overwrite:
                folder_properties.append(root.split('\\')[-1]) # Add folder name to list
                folder_properties.append(root) # Add folder path to list to navigate with later on
                folder_list.append(folder_properties[:]) # Add list of folder properties (name and path) to folder list
            else:
                if csv_file_name not in files:
                    folder_properties.append(root.split('\\')[-1]) # Add folder name to list
                    folder_properties.append(root) # Add folder path to list to navigate with later on
                    folder_list.append(folder_properties[:]) # Add list of folder properties (name and path) to folder list
            #print(folder_properties)
            #print(folder_list)
    if not folder_list:
        print("The selected \"Result Table.Result\" files already have corresponding \"New_Results.csv\" files.")
        return folder_list

    data_frame = pd.DataFrame(folder_list, columns=['Folders','Path'])
    pd.set_option("display.max_colwidth", 200)
    print('')
    print(data_frame.iloc[:,:])
    print('')

    correct_input = False
    num_rows = int(data_frame.shape[0])
    selected_dir_list = []
    while not correct_input:
        selected_dir_list = get_user_input_sel_dir()
        for num in selected_dir_list:
            if num >= num_rows or num < 0:
                print("An index must be a number between 0 and " + str(num_rows - 1) + ".")
                correct_input = False
                break
            correct_input = True
    
    selected_path_list = []
    for index in selected_dir_list:
        selected_path_list.append(data_frame.iloc[index, 1])
        
    return selected_path_list


def get_user_input_sel_dir():
    parsed = False
    while not parsed:
        try:
            dir_user_input = raw_input("Select indices of folders to create \".csv\" files for (Enter as comma or space separated list): ")
            dir_user_input = dir_user_input.strip() # Remove leading and trialing spaces
            selected_dir_list = list(map(int, re.split(',| ', dir_user_input))) # Remove comma and spaces from user input for indices
            parsed = True
        except ValueError:
            print("Invalid list. Check syntax.\ni.e.\nComma-separated: 1,2,3\nSpace-separated: 1 2 3")
    return selected_dir_list


if __name__ == "__main__":
    get_dir('C:\Users\a0491609\TI Drive\SpotFire_DataStacking')