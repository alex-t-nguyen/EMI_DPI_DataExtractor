import os
from extract_data import create_new_filename
import constants
import pandas as pd
import re
import codecs

def get_file(root_dir, info_type, overwrite=False):
    """
    Gets all directory paths in root folder for all .Result files that don't have a corresponding .csv file.\n

    :param root_dir: root directory to search for all .Result files in.\n
    :return: list of directory paths for .Result files without a corresponding .csv file.
    """
    file_path_list = []
    result_file_flag = False

    for (root, dirs, files) in os.walk(root_dir, topdown=True): # Walk through all folders in root_dir
        if constants.DATA_FILE_NAME in files: # if .Result file is in folder
            result_file_flag = True
            csv_file_name = create_new_filename(root, constants.CSV_FILE_NAME)   # new .csv file name
            if overwrite:   # if overwriting current .csv files               
                file_path_list.append(root) # Add folder path to list to create .csv later on    
            else:   # if ignoring current .csv files
                if csv_file_name not in files:  # if .csv file for corresponding .Result file is not in folder            
                    file_path_list.append(root) # Add folder path to list to create .csv later on 

    if not result_file_flag:
        print("No \"Result Table.Result\" files found in specified path ({}).".format(root_dir))          
    elif not file_path_list:
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
    result_file_flag = False

    for (root, dirs, files) in os.walk(root_dir, topdown=True): # Walk through all folders in root_dir 
        if constants.FILE_NAME in files: # if .Result file is in 
            result_file_flag = True
            del folder_properties[:]
            csv_file_name = create_new_filename(root, constants.CSV_FILE_NAME)   # new .csv file name
            if overwrite:
                folder_properties.append(root.split('\\')[-1]) # Add folder name to list
                folder_properties.append(root) # Add folder path to list to navigate with later on
                folder_list.append(folder_properties[:]) # Add list of folder properties (name and path) to folder list
            else:
                if csv_file_name not in files:
                    folder_properties.append(root.split('\\')[-1]) # Add folder name to list
                    folder_properties.append(root) # Add folder path to list to navigate with later on
                    folder_list.append(folder_properties[:]) # Add list of folder properties (name and path) to folder list

    if not result_file_flag:
        print("No \"Result Table.Result\" files found in specified path ({}).".format(root_dir)) 
        return folder_list
    elif not folder_list:
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
    sel_type = get_user_input_sel_type()
    while not correct_input:    # Check user input for valid input
        selected_dir_list = get_user_input_sel_dir(sel_type)
        if sel_type.lower() == 'i':
            for num in selected_dir_list:   # If select index mode for selection
                if num >= num_rows or num < 0:
                    print("An index must be a number between 0 and " + str(num_rows - 1) + ".")
                    correct_input = False
                    break
                correct_input = True
        elif sel_type.lower() == 'c':   # If select custom mode for selection
            unfound_key_list = []
            for key in selected_dir_list: # Check all desired keys in every folder in dataframe (folder names must contain all keys inputted by user --- NOT at least 1)
                correct_input = False
                for index, row in data_frame.iterrows():
                    keys_substring = get_key_substring(row['Folders'])
                    if key in keys_substring:
                        correct_input = True
                if key not in unfound_key_list and not correct_input:   # If key is found in folder name, don't add to unfound list
                        unfound_key_list.append(key)
            
            if unfound_key_list:    # If at least 1 key inputted by user was not found in folders
                print("Key(s) [" + ', '.join(unfound_key_list) + "] could not be found from available keys in folder names.")
                correct_input = False
            else:
                correct_input = True
        else:
            print("Invalid input.")
            sel_type = get_user_input_sel_type()
            correct_input = False

    selected_path_list = []
    if sel_type.lower() == 'i':
        for index in selected_dir_list:
            selected_path_list.append(data_frame.iloc[index, 1])
    elif sel_type.lower() == 'c':
        for index, row in data_frame.iterrows():
            #start_marker = row['Folders'].find('[') + len('[')
            #end_marker = row['Folders'].find(']')
            #keys_substring = row['Folders'][start_marker:end_marker]

            keys_substring = get_key_substring(row['Folders'])

            # Change 'all' to 'any' to check for at least 1 key existing in folder name
            if all(key in keys_substring for key in selected_dir_list): # If ALL keys entered in custom selection are present in folder name
                selected_path_list.append(data_frame.iloc[index, 1])

    return selected_path_list


def get_user_input_sel_dir(sel_type):
    parsed = False
    selected_dir_list = []
    while not parsed:
        try:
            if sel_type.lower() == 'i':
                dir_user_input = raw_input("Select indices of folders to create \".csv\" files for (Enter as comma or space separated list): ")
                dir_user_input = dir_user_input.strip() # Remove leading and trailing spaces
                selected_dir_list = list(map(int, re.split(',| ', dir_user_input))) # Remove comma and spaces from user input for indices
                parsed = True
            elif sel_type.lower() == 'c':
                dir_user_input = raw_input("Enter keyword(s) for custom selection (Enter as comma or space separated list): ")
                dir_user_input = dir_user_input.strip() # Remove leading and trailing spaces
                selected_dir_list = list(re.split(',| ', dir_user_input)) # Remove comma and spaces from user input for indices
                parsed = True

                # Copy user input keys into constants variable for to append to filename when making aggregated .csv file
                constants.KEYS = selected_dir_list[:]
            else:
                break
        except ValueError:
            print("Invalid list. Check syntax.\ni.e.\nComma-separated: 1,2,3\nSpace-separated: 1 2 3")
    return selected_dir_list


def get_user_input_sel_type():
    sel_type = raw_input("Select data by index or custom (I/C)? ")
    return sel_type


def get_key_substring(line):
    #start_marker = line.find('[') + len('[')
    #end_marker = line.find(']')
    #keys_substring = line[start_marker:end_marker]
    keys_list = line.split(' ')
    return keys_list


if __name__ == "__main__":
    get_dir('C:\Users\a0491609\TI Drive\SpotFire_DataStacking')