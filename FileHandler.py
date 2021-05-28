import os
from extract_data import create_new_filename
import constants

def get_file(root_dir):
    """
    Gets all directory paths in root folder for all .Result files that don't have a corresponding .csv file

    :param root_dir: root directory to search for all .Result files in
    :return: list of directory paths for .Result files without a corresponding .csv file
    """
    file_path_list = []

    for (root, dirs, files) in os.walk(root_dir, topdown=True):
        if constants.DATA_FILE_NAME in files: # if .Result file is in folder
            csv_file_name = create_new_filename(root)   # new .csv file name
            if csv_file_name not in files:  # if .csv file for corresponding .Result file is not in folder
                file_path_list.append(root) # Add folder path to list to create .csv later on
                
    if not file_path_list:
        print("\"Result Table.Result\" files already have corresponding \"New_Results.csv\" files")
    return file_path_list


if __name__ == "__main__":
    get_file('temp')