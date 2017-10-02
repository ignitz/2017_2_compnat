from individual import *
import sys
import operator
from itertools import groupby

# define default const

TAMANHO_INDIVIDUO = 7

TAMANHO_POPULACAO = 50
# TAMANHO_POPULACAO = 100
# TAMANHO_POPULACAO = 500

PROB_CROSSOVER = 0.9
PROB_MUTATION = 0.05

# PROB_CROSSOVER = 0.6
# PROB_MUTATION = 0.3

TAMANHO_TORNEIO = 5
# TAMANHO_TORNEIO = 5

# TAMANHO_TORNEIO = 3
# TAMANHO_TORNEIO = 7

TAMANHO_ELITISMO = 2

MAX_GEN = 50

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

def tournament(population, tour_size=TAMANHO_TORNEIO):
    chooses_index=[]

    i = 0
    while i < tour_size:
        random_index = randint(0, TAMANHO_POPULACAO-1)
        if random_index not in chooses_index:
            chooses_index.append(random_index)
            i += 1

    chooses_ind = []
    for index in chooses_index:
        chooses_ind.append(population[index])

    chooses_ind.sort(key=operator.attrgetter('fitness'))

    # gets the best
    return chooses_ind[0]

if __name__ == '__main__':

    # DESCRIPTION = 'TP1 - Genetic Programming - Yuri Niitsuma<ignitzhjfk@gmail.com>'
    #
    # parser = argparse.ArgumentParser(description=DESCRIPTION)
    #
    # parser.add_argument('csv_file', type=str, nargs='2',
    #                     help='CSV files for train and test')
    #
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')
    #
    # args = parser.parse_args()
    # print (args.accumulate(args.csv_files))

    params = sys.argv[1:]

    if len(params) <= 1:
        print('TP1 - Genetic Programming - Yuri Niitsuma<ignitzhjfk@gmail.com>')
        print('\tUsage: python3 gp.py train_data test_data')

    # TODO: insert params values
    # get train files
    train_x, train_y, train_dim = get_values_csv(params[0])
    # get_test_files
    test_x, test_y, test_dim = get_values_csv(params[1])

    if test_dim != train_dim:
        print_error('Train and test files have diff dimensions')
        print_error('train_dim: ' + str(train_dim))
        print_error('test_dim: ' + str(test_dim))
        sys.exit(1)

    population = []

    # generate initial population
    for i in range(TAMANHO_POPULACAO):
        population.append(Individual(train_dim))

    # fitness
    for ind in population:
        ind.set_fitness(train_x, train_y)

    population.sort(key=operator.attrgetter('fitness'))

    for count_gen in range(MAX_GEN):
        new_population = list()
        waiting_room = list()

        # Elitismo
        for i in range(TAMANHO_ELITISMO):
            new_population.append(copy.copy(population[i]))

        # Crossover
        while len(population) >= 2:
            ind1 = population.pop(randint(0, len(population)-1))
            ind2 = population.pop(randint(0, len(population)-1))
            ind1_children, ind2_children = ind1.do_crossover(ind2, PROB_CROSSOVER)
            if ind1_children is not None and ind2_children is not None:
                waiting_room.append(copy.deepcopy(ind1_children))
                waiting_room.append(copy.deepcopy(ind2_children))
            else:
                waiting_room.append(copy.deepcopy(ind1))
                waiting_room.append(copy.deepcopy(ind2))

        # Mutação
        while len(new_population) < TAMANHO_POPULACAO:
            # ind = waiting_room.pop(randint(0, len(waiting_room)-1))
            ind = tournament(waiting_room)
            ind.do_mutation(PROB_MUTATION)
            new_population.append(copy.deepcopy(ind))

        # Fitness
        for ind in new_population:
            ind.set_fitness(train_x, train_y)

        new_population.sort(key=operator.attrgetter('fitness'))
        population = new_population

        valores = []

        for ind in population:
            valores.append(ind.fitness)

        print_purple('Geração ' + str(count_gen))
        print_purple('Melhor Indivíduo: ' + str(population[0].fitness) + '\t' + str(population[0]))
        print_purple('Pior Indivíduo: ' + str(population[-1].fitness) + '\t' + str(population[-1]))
        print_purple('Média de erro: ' + str(media(valores)))

    for ind in population:
        print(ind)

    print_bold(population[0])
    print_bold(population[0].fitness)
    print_bold(population[-1])
    print_bold(population[-1].fitness)

    # Check if test is OK
    print_error(population[0].set_fitness(test_x, test_y))

    for x in [len(list(group)) for key, group in groupby(valores)]:
        if x > 1:
            print_error(str(x) + ' indivíduos repetidos!')
