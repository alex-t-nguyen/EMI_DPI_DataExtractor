import pandas
import codecs

# constants
DATA_HEADER = '[TableValues]'


def getData(filename):
    """ 
    Read data (frequency and level) from file. 

    :param filename: name of file to read
    :return: pandas data frame containing frequency and data point
    """

    data_dict = {'Frequency': [], 'Level': []}
    #with open(filename) as fp:
        # skip_lines(fp, 7)   # skip lines 1-7 in file
    for line in skip_lines(filename):
        signal_list = line.strip('\n').strip().split('\t')   # remove \n char at end of line and separate data into list
        
        if len(signal_list) <= 3:
            continue

        # Assign frequency and level values of signal from signal_list
        # Not really necessary, but improves readability
        frequency = signal_list[0]
        level = signal_list[1]

        data_dict['Frequency'].append(frequency)    # add frequency component to data_dict
        data_dict['Level'].append(level)  # add data component to data_dict
        
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


if __name__ == '__main__':
    getData('Result Table.Result')