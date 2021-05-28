import os

#constants
DATA_FILE_NAME = 'Result Table.Result'
CSV_FILE_NAME = 'New_Results.csv'

def get_file(root_dir):
    file_path_list = []

    for (root, dirs, files) in os.walk(root_dir, topdown=True):
        if DATA_FILE_NAME in files and CSV_FILE_NAME not in files:
            path = os.path.join(root, DATA_FILE_NAME)
            file_path_list.append(root)
            #print(file_path_list)
    
    if not file_path_list:
        print("\"Result Table.Result\" files already have corresponding \"New_Results.csv\" files")
    return file_path_list


if __name__ == "__main__":
    get_file('temp')