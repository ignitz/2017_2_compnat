def get_values_csv(file_name):
    values_list = []
    y_list = []

    dimensions = 0

    with open(file_name, 'r') as f:
        for each_line in f:
            line = each_line[:-1] if each_line[-1] == '\n' else each_line

            values = list(map(float, line.split(',')))

            values_list.append(values[:-1])
            y_list.append(values[-1])

            if dimensions != 0 and len(values) - 1 != dimensions:
                print('Something wrong with dimensions')
                print('last dimension: ', dimensions)
                print('this line dimension: ', len(values) - 1)
            else:
                dimensions = len(values) - 1

    return values_list, y_list, dimensions

if __name__ == '__main__':
    print(get_values_csv('datasets/keijzer-7-test.csv'))
