from DataHandler import get_data
import FileHandler as fh
import pandas as pd
import os
import csv
import sys
import constants
from itertools import izip
import codecs
import math

def main():
    info_type = get_user_input_info()   # User input info type
    dir_path = get_user_input_dir() # User input directory path of root folder containing data files
    overwrite = get_user_input_overwrite()  # User input for overwriting .csv files

    file_path_list = []
    df_list = []
    master_df = pd.DataFrame()

    correct_mode = False
    while not correct_mode: # Get user input for mode
        mode = get_user_input_mode()
        if mode.lower() == constants.MODE_SELECTIVE or mode.lower() == 's':    # Mode is selective
            file_path_list = fh.get_dir(dir_path, overwrite)
            correct_mode = True
        elif mode.lower() == constants.MODE_GENERAL or mode.lower() == 'g':    # Mode is general
            file_path_list = fh.get_file(dir_path, overwrite)
            correct_mode = True
        else:
            print("Invalid mode type.")

    if file_path_list:
        try:
            for path in file_path_list:
                os.chdir(path)
                df = get_data(constants.FILE_NAME, info_type)
                mask_df_list = create_mask_df(df)   # Create list of mask dataframes
                
                num_masks = len(mask_df_list)
                for i in range(num_masks):

                    mask_df_list[i] = add_identifier_columns(mask_df_list[i], info_type, path.split('\\')[-1], num_masks, i).copy(deep=True)
        
                    new_filename = create_new_filename(path, constants.CSV_FILE_NAME, None, num_masks, i)
                    
                    mask_df_list[i].to_csv(new_filename, sep = ',', index = False)

                    if 'MT1' in mask_df_list[i].columns:    # If dataframe has MT column -> drop them
                        for j in range(num_masks):                     
                            mask_df_list[i].drop('MT{}'.format(j + 1), axis=1, inplace=True)
                   
                    mask_df_list[i]['Limit Line'] = ''  # Add limit line column and set values to empty
                    
                    df_list.append((mask_df_list[i], path.split('\\')[-1])) # Append individual dataframes to list
                    
            
            master_df = create_master_df(df_list)   # Combine all dataframes into a master dataframe

            master_df = add_limit_line(master_df, df_list, dir_path, info_type).copy(deep=True) # Add limit line values to limit line dataframe in master dataframe

            os.chdir(dir_path)
            aggregated_csv_filename = create_new_filename(dir_path, constants.AGGREGATED_CSV_FILE_NAME, constants.KEYS) 
            master_df.to_csv(aggregated_csv_filename, sep= ',', index = False)  # Create .csv file from master dataframe
            
            if mode.lower() == constants.MODE_SELECTIVE:    # Mode is selective
                print("\".csv\" files for all selected \".Result\" files successfullly created.")
            else:    # Mode is general
                print("\".csv\" files for all \".Result\" files successfullly created.")
            
        except OSError:
            print("Can't create Pandas dataframe.")
            print("Error: " + sys.exc_info()[0])
    raw_input("Press any key to exit...")


def get_user_input_info():
    """
    Asks user for input for type of data.\n

    :return: type of info as string.
    """
    info_type = raw_input("Select information type ({}): ".format(', '.join(constants.INFO_TYPES_LIST)))

    while info_type not in constants.INFO_TYPES_LIST:
        print("The selected information type is not an available option.")
        info_type = raw_input("Select information type ({}): ".format(', '.join(constants.INFO_TYPES_LIST)))
    return info_type


def get_user_input_dir():
    """
    Asks user for input for directory path of folder containing all data.\n

    :return: directory path as string.
    """
    dir_path = raw_input("Enter directory path: ")
    return dir_path


def get_user_input_mode():
    """
    Asks user for input for mode of extracting data\n

    :return: mode type
    """
    mode = raw_input("Select data extraction mode ({}) (G/S): ".format(', '.join(constants.MODE_TYPES_LIST)))
    if mode != 'g' and mode != 's':
        while mode not in constants.MODE_TYPES_LIST:
            print("The selected mode type is not an available option.")
            mode  = raw_input("Select data extraction mode ({}): ".format(', '.join(constants.MODE_TYPES_LIST)))
    return mode


def get_user_input_overwrite():
    """
    Asks user if they want to overwrite current .csv files or skip them when creating and aggregating data.\n

    :return: boolean
    """
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


def create_new_filename(path, appended_filename, keys=None, num_masks=1, mask_index=0):
    """
    Creates new file name for generated .csv file.\n

    :param path: path to directory of .Result file.\n
    :param appended_filename: name to append to folder name in the file name.\n
    :param keys: keys in custom search to add to file name.\n
    :return: name of generated .csv file as string.
    """
    file_base_name = path.split('\\')[-1]
    mask_name = ''
    if num_masks > 1:
        mask_name = '_M{}_'.format(mask_index + 1)
    if keys:
        keys_as_string = ' '.join(map(str, keys))
        string_keys = "_keys=[{}]".format(keys_as_string if keys else "")
        return file_base_name + string_keys + mask_name + appended_filename
    else:
        return file_base_name + mask_name + appended_filename


def create_master_df(df_list):
    """
    Creates a master dataframe that combines all of the data files and limit lines files in 1 dataframe.\n

    :param df_list: list of dataframes to combine into a master dataframe
    :return: dataframe containing all datafarmes in df_list
    """
    master_dict = {}
    master_df = pd.DataFrame()

    # Check length of dataframe (# of rows) to determine size for new dictionary (master_dict)
    # Arrays in master_dict need to be same size to put into pandas dataframe
    lf_index, largest_index_row = 0, len(df_list[0][0])
    for i in range(1, len(df_list)):
        index_row = len(df_list[i][0])
        if index_row > largest_index_row:
            lf_index, largest_index_row = i, index_row

    for df in df_list:
        master_df = master_df.append(df[0], ignore_index=True, sort=False).copy(deep=True)
    master_df['Frequency'] = pd.to_numeric(master_df['Frequency'], errors='coerce').copy(deep=True)

    return master_df


def add_identifier_columns(data_frame, info_type, folder_name, num_masks, mask_index = 0):
    keys = folder_name.split(' ')
    if num_masks > 1:
        data_frame['Data Set'] = folder_name + "_M{}".format(mask_index + 1)
    else:
        data_frame['Data Set'] = folder_name
    if info_type.lower() == constants.TYPE_EMISSION:    # Add identifier columns for emission data
        for i in range(len(constants.EMISSION_IDENTIFIERS)):
            if constants.EMISSION_IDENTIFIERS[i] == '-':    # If column header is '-' -> don't add as column
                continue
            data_frame[constants.EMISSION_IDENTIFIERS[i]] = keys[i] if i < len(keys) and keys[i] != '-' else ''
    elif info_type.lower() == constants.TYPE_DPI:   # Add identifier columns for dpi data
        for i in range(len(constants.DPI_IDENTIFIERS)):
            if constants.DPI_IDENTIFIERS[i] == '-': # If column header is '-' -> don't add as column
                continue
            data_frame[constants.DPI_IDENTIFIERS[i]] = keys[i] if i < len(keys) and keys[i] != '-' else ''

    return data_frame


def add_limit_line(master_df, df_list, path, info_type):
    limit_line_file_flag = False
    limit_line_file_list = []
    temp_ll_file_list = []
    for (root, dirs, files) in os.walk(path, topdown=True): # Walk through all folders in root_dir
        for filename in files:
            if filename.endswith(constants.LIMIT_LINE_FILE_SUFFIX): # if .LimitLine file is in folder
                if filename == constants.IGNORE_LL_HEADER:  # Ignore TargetLevel.LimitLine file
                    continue
                limit_line_file_flag = True               
                if filename not in temp_ll_file_list:
                    limit_line_file_list.append(os.path.join(root, filename))
                    temp_ll_file_list.append(filename)
    if not limit_line_file_flag:
        print("No \".LimitLine\" files found in specified path ({}).".format(path))

    df_only_list = []
    for df in df_list:  # Get just the dataframes and put them into a list (for easier access)
        df_only_list.append(df[0])

    constants.LL_FREQUENCY_LIST = create_ll_frequency([])   # Create frequency values for limit line
    for limit_line_path in limit_line_file_list: # Create limit line df for each file in limit line list
        df = df_only_list[0].copy(deep=True)    # temp df for limit line df
        for col in df.columns:
            if col not in constants.IMPORTANT_COL_NAMES:    # Empty data in columns not necessary for limit line df
                df[col] = ''
        
        df['Data Set'] = 'LL ' + os.path.splitext(limit_line_path.split('\\')[-1])[0] # Create name for data set (LL + filename w/o extension)
       
        with codecs.open(limit_line_path, encoding='utf-16-le') as limit_line_file:   
            for line in limit_line_file:  # Skips lines until reading 'TableValues' line
                if constants.DATA_HEADER.encode(encoding='utf-16-le') not in line.encode(encoding='utf-16-le'): # Check for 'TableValues' string in line 
                    continue
                else:
                    break
            
            limit_lines = limit_line_file.readlines() # Get all remaining lines in file

            curr_line = limit_lines[0]
            temp_df_list = []
            for i in range(1, len(limit_lines)):
                prev_line = curr_line
                curr_line = limit_lines[i]

                slope = get_limit_line_slope(prev_line, curr_line)
                coord0 = get_coord(prev_line)
                coord1 = get_coord(curr_line)

                if math.isnan(slope):
                    continue
                
                
                
                ll_df = create_ll_df(df, constants.LL_FREQUENCY_LIST, limit_line_path)
                
                ll_df.sort_values(by='Frequency', ascending=True)
                temp_df = ll_df.loc[(ll_df.loc[:, 'Frequency'].apply(lambda x: float(x)) >= coord0[0]) & (ll_df.loc[:, 'Frequency'].apply(lambda x: float(x)) <= coord1[0]), :].copy(deep=True) # ------------ REMEMBER TO CONVERT NUMBERS IN DF FROM STRING TO FLOAT ------------------------------------
           
                temp_df.loc[:, 'Limit Line'] = temp_df.loc[:, 'Frequency'].apply(lambda x: calc_limit(slope, float(x), coord0, coord1)).copy(deep=True)

                temp_df_list.append(temp_df)
                
            new_df = pd.concat(temp_df_list, ignore_index=True)
        
            master_df = master_df.append(new_df, ignore_index=True, sort=False).copy(deep=True)
       
    return master_df

def get_limit_line_slope(signal0, signal1):
    """
    Calculates slope of limit line based on 2 coordinates\n

    :param signal0: first signal to use for slope calculation\n
    :param signal1: second signal to use for slope calculation\n

    :return: slope of limit line
    """
    signal_list0 = signal0.strip('\n').strip().split('\t')
    signal_list1 = signal1.strip('\n').strip().split('\t')
    
    x0 = float(signal_list0[0])    # frequency
    y0 = float(signal_list0[1])    # limit line value

    x1 = float(signal_list1[0])   # frequency
    y1 = float(signal_list1[1])    # limit line value

    try:
        slope = (y1-y0)/(math.log10(x1/x0))
        return slope
    except ZeroDivisionError:
        return float('NaN')


def get_coord(signal):
    """
    Gets coordinates from limit line file\n
    :param signal: line from limit line file\n

    :return: tuple containing the x and y coordinates of the line read from limit line file\n
    """
    signal_list = signal.strip('\n').strip().split('\t')
    signal_list[0] = float(signal_list[0])
    signal_list[1] = float(signal_list[1])
    return tuple(signal_list)


def calc_limit(slope, frequency, coord0, coord1):
    """
    Calculates limit of limit line based on 2 coordinates\n

    :param slope: slope of limit line\n
    :param frequency: frequency to calculate limit value of\n
    :param coord0: first coordinate of limit line\n
    :param coord1: second coordinate of limit line\n
    """
    if slope == 0:
        return coord0[1]
    elif math.isnan(slope):
        return coord1[1]
    else:
        return slope * math.log10(frequency/coord0[0]) + coord0[1]


def create_ll_frequency(LL_FREQUENCY_LIST):
    """
    Creates list of individual frequencies for limit line\n

    :param LL_FREQUENCY_LIST: list to add frequencies to\n

    :return: list of frequencies for limit line
    """
    frequency = .15
    while frequency <= 1e3: # Max frequency is 1 GHz
        while frequency < 10:  # 0.15 - 10 MHz
            LL_FREQUENCY_LIST.append(frequency)
            frequency = frequency + 0.01   # Increment in 250 kHz steps
        while frequency >= 10 and frequency < 100:  # 10 - 100 MHz
            LL_FREQUENCY_LIST.append(frequency)
            frequency = frequency + .01   # Increment in 1 MHz steps
        while frequency >= 100 and frequency < 200: # 100 - 200 MHz
            LL_FREQUENCY_LIST.append(frequency)
            frequency = frequency + .01   # Increment in 2 MHz steps
        while frequency >= 200 and frequency < 400:  # 200 - 400 MHz
            LL_FREQUENCY_LIST.append(frequency)
            frequency = frequency + .01   # Increment in 4 MHz steps
        while frequency >= 400 and frequency <= 1e3: # 400 MHz - 1 GHz
            LL_FREQUENCY_LIST.append(frequency)
            frequency = frequency + .01   # Increment in 10 MHz steps
    return LL_FREQUENCY_LIST


def create_ll_df(df, ll_list, path):
    """
    Creates limit line data frame with corresponding 'Data Set' value and frequency values\n

    :param df: dataframe to copy for columns\n
    :param ll_list: list of frequencies for limit line\n
    :param path: path of limit line file\n

    :return: dataframe for limit line
    """
    orig_num_rows = df.shape[0]
    new_num_rows = len(ll_list)
    temp_list = []
    col_names = list(df.columns)
    ll_df = pd.DataFrame(columns=col_names)
    ll_df['Frequency'] = ll_list
    ll_df['Data Set'] = 'LL ' + os.path.splitext(path.split('\\')[-1])[0] # Create name for data set (LL + filename w/o extension)
    return ll_df


def create_mask_df(df):
    # 1) Turn DataFrame into dictionary
    # 2) Read Frequency, Power, and MT columns
    # 3) Create n dictionaries based on how many MT columns there are
    # 4) If all MT are 0 -> follow power levels
            # If MT1 = 1 and MT2 = 0 -> MT1 follows power level, MT2 stays at the previous value before changing
            # If MT1 = 0 and MT2 = 1
    # 5) Turn all dictionaries into DataFrames
    # 6) Return list of DataFrames
    main_dict = df.to_dict()

    level_key = list(df.columns)[1]
    level_list = main_dict[level_key]
    df_list = []
    if 'MT3' in main_dict.keys():   # If file has 3 masks
        common_level = level_list[0]
        m1_dict = df.copy(deep=True).to_dict()
        m2_dict = df.copy(deep=True).to_dict()
        m3_dict = df.copy(deep=True).to_dict()
        for i in range (len(main_dict['Frequency'])):
            if not main_dict['MT1'][i] or not main_dict['MT2'][i] or not main_dict['MT3'][i]: # Check if MT column has an empty value, and skip it if so
                continue
            m1 = float(main_dict['MT1'][i])
            m2 = float(main_dict['MT2'][i])
            m3 = float(main_dict['MT3'][i])
            if m1 == 0 and m2 == 0:
                common_level = level_list[i]
            elif m1 == 1 and m2 == 0 and m3 == 0:
                m2_dict[level_key][i] = common_level
                m3_dict[level_key][i] = common_level
            elif m2 == 1 and m1 == 0 and m3 == 0:
                m1_dict[level_key][i] = common_level
                m3_dict[level_key][i] = common_level
            elif m3 == 1 and m1 == 0 and m2 == 0:
                m2_dict[level_key][i] = common_level
                m1_dict[level_key][i] = common_level
        
        m1_df = pd.DataFrame(m1_dict)
        m2_df = pd.DataFrame(m2_dict)
        m3_df = pd.DataFrame(m3_dict)
        df_list.append(m1_df)
        df_list.append(m2_df)
        df_list.append(m3_df)
    elif 'MT2' in main_dict.keys(): # If file has 2 masks
        common_level = level_list[0]
        m1_dict = df.copy(deep=True).to_dict()
        m2_dict = df.copy(deep=True).to_dict()
        
        for i in range (len(main_dict['Frequency'])):
            if not main_dict['MT1'][i] or not main_dict['MT2'][i]:  # Check if MT column has an empty value, and skip it if so
                continue
            try:
                m1 = float(main_dict['MT1'][i])
                m2 = float(main_dict['MT2'][i])
            except ValueError as e:
                print("Mask convert to float error: " + str(e) + "on line " + str(i))
            
            if m1 == 0 and m2 == 0:
                common_level = level_list[i]
            elif m1 == 1 and m2 == 0:
                m2_dict[level_key][i] = common_level
            elif m2 == 1 and m1 == 0:
                m1_dict[level_key][i] = common_level
        m1_df = pd.DataFrame(m1_dict)
        m2_df = pd.DataFrame(m2_dict)
        df_list.append(m1_df)
        df_list.append(m2_df)
    else:   # If file has no masks -> return the original dataframe
        df_list.append(df)
    return df_list
    

if __name__ == "__main__":
    main()