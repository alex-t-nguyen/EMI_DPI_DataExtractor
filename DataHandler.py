import pandas
import codecs
import constants

def get_data(filename, info_type):
    """ 
    Read data (frequency and level) from file. 

    :param filename: name of file to read
    :return: pandas data frame containing frequency and data point
    """

    #data_dict = {'Frequency': [], 'Level': []}
    col_names = get_col_names(filename, info_type)
    data_dict = create_dict(info_type, col_names)
    #with open(filename) as fp:
        # skip_lines(fp, 7)   # skip lines 1-7 in file
    for line in skip_lines(filename):
        signal_list = line.strip('\n').strip().split('\t')   # remove \n char at end of line and separate data into list
        
        if len(signal_list) <= 3:
            continue

        append_data(col_names, data_dict, signal_list)

        # Assign frequency and level values of signal from signal_list
        # Not really necessary, but improves readability
        """
        frequency = signal_list[0]
        level = signal_list[1]

        data_dict['Frequency'].append(frequency)    # add frequency component to data_dict
        data_dict['Level'].append(level)  # add data component to data_dict
        """
    data_frame = pandas.DataFrame(data_dict)    # turn dictionary into Pandas DataFrame

    return data_frame


def skip_lines(opened_file):
    """ 
    Skip lines in file up until reading a specific string (constants.DATA_HEADER)

    :param opened_file: file to read
    """
    with codecs.open (opened_file, encoding='utf-16-le') as data_file:
        for line in data_file:
            if constants.DATA_HEADER not in line:
                data_file.next()
            else:
                break
        #for i in range(28):
        #    data_file.readline()
        for line in data_file:
            if not line:
                continue
            else:
                yield line


def create_dict(info_type, col_names):
    """ 
    Creates a dictionary with all of the column names as keys and empty lists as values for each key

    :param info_type: type of data in file (i.e. emission, DPI, etc.)
    :col_names: names of columns to be used as keys in dictionary
    """
    data_dict = {}
    for name in col_names:
        data_dict[name] = []
    return data_dict
    """
    switcher = {
        constants.TYPE_EMISSION:    
            {'Frequency': [], 'Level': []},
        constants.TYPE_DPI: {'Col1': []}#, 'Col2': [], 'Col3': [], 'Col4': []},
    }
    return switcher.get(info_type, {})
    """


def append_data(col_names, data_dict, signal_list):
    """ 
    Appends signal data to dictionary.
    Number of keys in dictionary (data_dict) depends on file (info_type) read

    :param info_type: type of data in file (i.e. emission, DPI, etc.)
    :param data_dict: dictionary containing signal data
    :param signal_list: list of individual signal data values
    :return: data_dict
    """
    for i in range(len(col_names)):
        data_dict[col_names[i]].append(signal_list[constants.EMISSION_COL_INDEXES[i]])
    """
    if info_type == constants.TYPE_EMISSION:
        data_dict['Frequency'].append(signal_list[0])    # add frequency component to data_dict
        data_dict['Level'].append(signal_list[1])   # add level component to data_dict
    elif info_type == constants.TYPE_DPI:
        data_dict['Col1'].append(signal_list[0])    # add Col1 component to data_dict
        #data_dict['Col2'].append(signal_list[1])
        #data_dict['Col3'].append(signal_list[2])
        #data_dict['Col4'].append(signal_list[3])
    else:
        print('Not a valid info_type')
    """
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
                column_names = line.strip('\n').split('\t') # get all column names in file
                del column_names[0]
                break
    for i in range(len(column_names)):
        if info_type.lower() == constants.TYPE_EMISSION:
            if i in constants.EMISSION_COL_INDEXES:
                desired_col_names.append(column_names[i]) # add all desired column names to list
        if info_type.lower() == constants.TYPE_DPI:
            if i in constants.DPI_COL_INDEXES:
                desired_col_names.append(column_names[i])
    return desired_col_names

if __name__ == '__main__':
    get_data('Result Table.Result')