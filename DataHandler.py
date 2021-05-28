import pandas
import codecs

# constants
DATA_HEADER = '[TableValues]'
TYPE_EMISSION = 'emission'
TYPE_DPI = 'dpi'

def get_data(filename, info_type):
    """ 
    Read data (frequency and level) from file. 

    :param filename: name of file to read
    :return: pandas data frame containing frequency and data point
    """

    #data_dict = {'Frequency': [], 'Level': []}
    data_dict = create_dict(info_type)
    #with open(filename) as fp:
        # skip_lines(fp, 7)   # skip lines 1-7 in file
    for line in skip_lines(filename):
        signal_list = line.strip('\n').strip().split('\t')   # remove \n char at end of line and separate data into list
        
        if len(signal_list) <= 3:
            continue

        append_data(TYPE_EMISSION, data_dict, signal_list)

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
    Skip lines in file up until reading a specific string (DATA_HEADER)

    :param opened_file: file to read
    """
    with codecs.open (opened_file, encoding='utf-16-le') as data_file:
        for line in data_file:
            if DATA_HEADER not in line:
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


def create_dict(info_type):
    """ 
    Skip lines in file up until reading a specific string (DATA_HEADER)

    :param info_type: type of data in file (i.e. emission, DPI, etc.)
    """
    switcher = {
        TYPE_EMISSION: {'Frequency': [], 'Level': []},
        TYPE_DPI: {'Col1': [], 'Col2': [], 'Col3': [], 'Col4': []},
    }
    return switcher.get(info_type, {})


def append_data(info_type, data_dict, signal_list):
    """ 
    Appends signal data to dictionary.
    Number of keys in dictionary (data_dict) depends on file (info_type) read

    :param info_type: type of data in file (i.e. emission, DPI, etc.)
    :param data_dict: dictionary containing signal data
    :param signal_list: list of individual signal data values
    :return: data_dict
    """
    if info_type == TYPE_EMISSION:
        data_dict['Frequency'].append(signal_list[0])    # add frequency component to data_dict
        data_dict['Level'].append(signal_list[1])
    elif info_type == TYPE_DPI:
        data_dict['Col1'].append(signal_list[0])
        data_dict['Col2'].append(signal_list[1])
        data_dict['Col3'].append(signal_list[2])
        data_dict['Col4'].append(signal_list[3])
    else:
        print('Not a valid info_type')
    
    return data_dict


if __name__ == '__main__':
    get_data('Result Table.Result')