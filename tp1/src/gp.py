from individual import *
import sys
import operator
from itertools import groupby

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

def tournament(population, tour_size):
    chooses_index=[]

    i = 0
    while i < tour_size:
        random_index = randint(0, len(population)-1)
        if random_index not in chooses_index:
            chooses_index.append(random_index)
            i += 1

    chooses_ind = []
    for index in chooses_index:
        chooses_ind.append(population[index])

    chooses_ind.sort(key=operator.attrgetter('fitness'))

    # gets the best
    return chooses_ind[0]

def main(train_file, test_file, output_file_name, MAX_GEN=15, TAMANHO_POPULACAO = 50, PROB_CROSSOVER = 0.9, PROB_MUTATION = 0.05, TAMANHO_TORNEIO = 2, TAMANHO_ELITISMO = 2):

    MAX_GEN = int(MAX_GEN)
    TAMANHO_POPULACAO = int(TAMANHO_POPULACAO)
    TAMANHO_TORNEIO = int(TAMANHO_TORNEIO)
    TAMANHO_ELITISMO = int(TAMANHO_ELITISMO)
    PROB_CROSSOVER = float(PROB_CROSSOVER)
    PROB_MUTATION = float(PROB_MUTATION)

    output = open(output_file_name, 'w', encoding="utf-8")
    if not output:
        print_error('error on opening file ' + str(output_file_name))
        sys.exit(1)

    # get train files
    train_x, train_y, train_dim = get_values_csv(train_file)
    # get_test_files
    test_x, test_y, test_dim = get_values_csv(test_file)

    # write params:
    temp = str(output_file_name) + '\n' + str(train_file) + '\t' + str(test_file) + '\n\n'

    output.write(temp)

    output.write('Params:\n')
    output.write('MAX_GEN = ' + str(MAX_GEN) + \
            '\nTAMANHO_POPULACAO = ' + str(TAMANHO_POPULACAO) + \
            '\nPROB_CROSSOVER = ' + str(PROB_CROSSOVER) + \
            '\nPROB_MUTATION = ' + str(PROB_MUTATION) + \
            '\nTAMANHO_TORNEIO = ' + str(TAMANHO_TORNEIO) + \
            '\nTAMANHO_ELITISMO = ' + str(TAMANHO_ELITISMO) + '\n\n')

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

    for count_gen in range(1, MAX_GEN+1):
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
            ind = tournament(waiting_room, TAMANHO_TORNEIO)
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

        temp = '\nGeração ' + str(count_gen) + '\n'
        temp += 'Melhor Indivíduo: ' + str(population[0].fitness) + '\t' + str(population[0]) + '\n'
        temp += 'Pior Indivíduo: ' + str(population[-1].fitness) + '\t' + str(population[-1]) + '\n'
        temp += 'Média de erro: ' + str(media(valores)) + '\n'
        print_purple(temp)
        output.write(temp)

    # for ind in population:
    #     print(ind)

    temp = '\n-----------------------------------------\nGeração final: \n'
    temp += 'Melhor Indivíduo (Train): \t' + str(population[0].fitness) + '\n\t' + str(population[0]) + '\n'
    temp += 'Pior Indivíduo (Train): \t' + str(population[-1].fitness) + '\n\t' + str(population[-1]) + '\n'
    print_blue(temp)
    output.write(temp)

    output.write('\n-----------------------------------------\nIndivíduos:\n')
    values = []
    for ind in population:
        values.append(ind.set_fitness(test_x, test_y))
        output.write('******\n\t' + str(ind) + '\n\t' + str(ind.fitness) + '\n')

    # Check if test is OK
    temp = '\n-----------------------------------------\nTest:\n'
    temp += '5 melhores indivíduos:\n'
    for i in range(5):
        temp += str(population[i]) + '\n\t' + str(population[i].fitness) + '\n'

    temp += 'Media: \t' + str(media(valores)) + '\n'
    temp += 'Desvio padrão: \t' + str(desvio_padrao(valores)) + '\n'

    print_green(temp)
    output.write(temp)

    print_error('Quantidade de indivíduos repetidos!')
    output.write('\n Quantidade de indivíduos repetidos!\n')
    for x in [len(list(group)) for key, group in groupby(valores)]:
        if x > 1:
            print_error(str(x), end="\t")
            output.write(str(x) + '\t')
    print()
    output.write('\n')

    output.close()

if __name__ == '__main__':

    params = sys.argv[1:]

    if len(params) <= 2:
        print('TP1 - Genetic Programming - Yuri Niitsuma<ignitzhjfk@gmail.com>')
        description = '\tUsage: python3 gp.py train_data test_data output_data'
        description += ' [max_generations] [size_population] [p(crossover)] [p(mutation)]'
        description += ' [size_tournament] [size_elitims]'
        print(description)
        sys.exit(1)

    main(*params)
