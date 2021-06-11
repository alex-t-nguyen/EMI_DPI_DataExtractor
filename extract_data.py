from DataHandler import get_data
import FileHandler as fh
import pandas as pd
import os
import csv
import sys
import constants
from itertools import izip

def main():
    info_type = get_user_input_info()   # User input info type
    dir_path = get_user_input_dir() # User input directory path of root folder containing data files
    #filename = 'Result Table.Result'
    overwrite = get_user_input_overwrite()

    file_path_list = []
    df_list = []
    master_df = pd.DataFrame()

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
                #print(df)
                new_filename = create_new_filename(path, constants.CSV_FILE_NAME)
                df.to_csv(new_filename, sep = ',', index = False)

                df_list.append((df, path.split('\\')[-1]))
                #print(df_list)
            
            master_df = create_master_df(df_list)

            os.chdir(dir_path)
            aggregated_csv_filename = create_new_filename(dir_path, constants.AGGREGATED_CSV_FILE_NAME, constants.KEYS)
            master_df.to_csv(aggregated_csv_filename, sep= ',', index = False)
            
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


def create_new_filename(path, appended_filename, keys=None):
    """
    Creates new file name for generated .csv file.\n

    :param path: path to directory of .Result file.\n
    :param appended_filename: name to append to folder name in the file name.\n
    :return: name of generated .csv file as string.
    """
    file_base_name = path.split('\\')[-1]
    if keys:
        keys_as_string = ' '.join(map(str, keys))
        string_keys = "_keys=[{}]".format(keys_as_string if keys else "")
        return file_base_name + string_keys + appended_filename
    else:
        return file_base_name + appended_filename


def create_master_df(df_list):
    master_dict = {}
    master_df = df_list[0][0].copy(deep=True)
    # Check length of dataframe (# of rows) to determine size for new dictionary (master_dict)
    # Arrays in master_dict need to be same size to put into pandas dataframe
    lf_index, largest_index_row = 0, len(df_list[0][0])#float(df_list[0][0]['Frequency'].iloc[-1])
    for i in range(1, len(df_list)):
        index_row = len(df_list[i][0])#float(df_list[i][0]['Frequency'].iloc[-1])
        if index_row > largest_index_row:
            lf_index, largest_index_row = i, index_row

    master_dict['Frequency'] = df_list[lf_index][0]['Frequency'].to_list()
    for col in df_list[0][0].columns:
        if col != 'Frequency':
            master_df.drop(col, axis=1, inplace=True)   # Drop the data columns in master_df to prevent duplicates when comparing with the same data in loop below
   # master_df['Frequency'] = pd.to_numeric(master_df['Frequency'], errors='coerce')
    for df in df_list:
        temp_names = []
        col_names = list(df[0].columns)
        col_names.remove('Frequency')
        for i in range(0, len(col_names)):
            temp_names.append(df[1] + "_" + col_names[i])
        temp_names.insert(0, 'Frequency')
        print(temp_names)
        df[0].columns = temp_names
        
        #df[0]['Frequency'] = pd.to_numeric(df[0]['Frequency'], errors='coerce')
        master_df = pd.merge(master_df, df[0], how='outer', on='Frequency')
    master_df['Frequency'] = pd.to_numeric(master_df['Frequency'], errors='coerce')
    master_df = master_df.sort_values('Frequency', ascending=True)
    #print(master_df)
    """
    for df in df_list:
        temp_dict = df[0].to_dict('list')
        del temp_dict["Frequency"]
        old_key = temp_dict.keys()[0]
        new_key = df[1] + "_" + old_key
        temp_dict[new_key] = temp_dict[old_key]
        del temp_dict[old_key]

        #print(len(master_dict['Frequency']))
        #print(len(temp_dict[new_key]))

        for i in range(0, len(master_dict['Frequency']) - len(temp_dict[new_key])):
            temp_dict[new_key].append("NaN")

        master_dict.update(temp_dict)

    master_df = pd.DataFrame(master_dict)
    """
    return master_df


if __name__ == "__main__":
    main()