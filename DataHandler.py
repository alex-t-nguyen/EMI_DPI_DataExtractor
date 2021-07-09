import pandas
import codecs
import constants

def get_data(filename, info_type):
    """ 
    Read data (frequency and level) from file. 

    :param filename: name of file to read
    :return: pandas data frame containing frequency and data point
    """
    col_names = get_col_names(filename, info_type)
    data_dict = create_dict(info_type, col_names)
    
    if not check_emi_or_dpi(filename, info_type):
        return pandas.DataFrame(data_dict)

    for line in skip_lines(filename, info_type):
        signal_list = line.strip('\n').strip().strip('\r').split('\t')   # remove \n char at end of line and separate data into list
        
        if len(signal_list) <= 1:   # If line is empty -> prevents error when trying to read the empty last line in .Results file
            continue

        for i in range(len(signal_list)):
            if signal_list[i] == '---':
                signal_list[i] = '' # make dashes equal to blank instead of NaN since spotfire does it anyway

        append_data(col_names, data_dict, signal_list, info_type)   # Add data from each row into corresponding key/column in data dictionary

    data_frame = pandas.DataFrame(data_dict)    # turn dictionary into Pandas DataFrame

    return data_frame


def skip_lines(opened_file, info_type):
    """ 
    Skip lines in file up until reading a specific string (constants.DATA_HEADER) (skip first 28 lines)

    :param opened_file: file to read
    """
    try:
        with codecs.open (opened_file, encoding='utf-16-le') as data_file:
            
            for line in data_file:  # Skips lines until reading 'TableValues' line
                if constants.DATA_HEADER.encode(encoding='utf-16-le') not in line.encode(encoding='utf-16-le'): # Check for 'TableValues' string in line 
                    continue
                else:
                    break
            
            for line in data_file:
                if not line:
                    continue
                else:
                    yield line
    except IOError:
        print("Can't open file")


def create_dict(info_type, col_names):
    """ 
    Creates a dictionary with all of the column names as keys and empty lists as values for each key

    :param info_type: type of data in file (i.e. emission, DPI, etc.)
    :col_names: names of columns to be used as keys in dictionary
    """
    data_dict = {}
    for name in col_names:
        data_dict[name] = []
    # data_dict['Limit Line'] = []    # Add Limit Line column to data dictionary ----- DO this in extract_data.py because we don't want the empty limit line column in individual .csv file --------------------------
    return data_dict


def append_data(col_names, data_dict, signal_list, info_type):
    """ 
    Appends signal data to dictionary.
    Number of keys in dictionary (data_dict) depends on file (info_type) read

    :param info_type: type of data in file (i.e. emission, DPI, etc.)
    :param data_dict: dictionary containing signal data
    :param signal_list: list of individual signal data values
    :return: data_dict
    """
    index_list = []
    if info_type.lower() == constants.TYPE_EMISSION:
        index_list = constants.EMISSION_COL_INDEXES[:]
    elif info_type.lower() == constants.TYPE_DPI:
        index_list = constants.DPI_COL_INDEXES[:]

    for i in range(len(col_names)):
        data_dict[col_names[i]].append(signal_list[index_list[i]])
    
    return data_dict


def get_col_names(filename, info_type):
    """
    Gets the desired data column names depending on the info_type

    :param filename: data file
    :param info_type: data information type
    :return: list of desired column names
    """
    column_names = []
    desired_col_names = []
    with codecs.open (filename, encoding='utf-16-le') as data_file:
        for line in data_file:
            if constants.COLUMN_NAME_HEADER in line:
                column_names = line.strip('\n').strip('\r').strip().split('\t') # get all column names in file
                del column_names[0]
                break
    
    if info_type.lower() == constants.TYPE_EMISSION:
        desired_col_names.append('Frequency')
        desired_col_names.append('PK+_CLRWR')
    if info_type.lower() == constants.TYPE_DPI:
        desired_col_names.append('Frequency')
        desired_col_names.append('Imm Level-Pk')
        if 'MT1' in column_names:
            desired_col_names.append('MT1')
            constants.DPI_COL_INDEXES.append(4) # MT1 index
        if 'MT2' in column_names:
            desired_col_names.append('MT2')
            constants.DPI_COL_INDEXES.append(5) # MT2 index
        if 'MT3' in column_names:
            desired_col_names.append('MT3')
            constants.DPI_COL_INDEXES.append(6) # MT3 index
    return desired_col_names


def check_emi_or_dpi(filename, info_type):
    """
    Skips files if data is not matching the info_type
    i.e. If info_type is DPI -> skip emission files, If info_type is EMI -> skip dpi files
    :param filename: filename
    :param info_type: type of data in file to search for
    :return: boolean
    """
    column_names = []
    with codecs.open (filename, encoding='utf-16-le') as data_file:
        for line in data_file:
            if constants.COLUMN_NAME_HEADER in line:
                column_names = line.strip('\n').strip('\r').strip().split('\t') # get all column names in file
                del column_names[0]
                break

    if 'PK+_CLRWR' in column_names and info_type.lower() == 'emission':
        return True
    elif 'Imm Level-Pk' in column_names and info_type.lower() == 'dpi':
        return True
    else:
        return False


if __name__ == '__main__':
    get_data('Result Table.Result')