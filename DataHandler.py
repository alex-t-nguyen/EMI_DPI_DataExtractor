import pandas

def main():
    data_dict = {'Frequency': [], 'Data': []}
    with open('data.txt') as fp:
        for i in range(7):
            fp.readline()
        for line in fp:
            frequency, data = line.strip('\n').split(' ')
            data_dict['Frequency'].append(frequency)
            data_dict['Data'].append(data)

    # print data_dict

    # header_list = ['Frequency', 'Data']
    # data_frame = pandas.read_csv('data.txt', names=header_list, sep=' ')
    data_frame = pandas.DataFrame(data_dict)
    print data_frame

# print "DataHandler name: {}".format(__name__)

if __name__ == '__main__':
    main()