#!/usr/bin/env python3

# encoding: UTF-8

"""
TP3 - Redes Neurais Artificiais
Yuri Diego Santos Niitsuma (2011039023)
"""

import sys
import time

import keras

# vamos usar o modulo do Keras chamado Sequential 
from keras.models import Sequential

# Como estamos construindo um modelo simples vamos utilizar
# camadas densas, que sao simplesmente camadas onde cada unidade
# ou neuronio estara conectado a cada neurônio na proxima camada.
from keras.layers import Dense

# Modulo do Keras responsavel por varias rotinas de pre-processamento 
# (https://keras.io/utils/).
from keras.utils import np_utils

# Nosso amigo numpy
import numpy as np

# for balance class
from sklearn.utils import class_weight

# plot graphics
import matplotlib.pyplot as plt


def get_values_from_csv(file_name):
	"""
	Ler dados do arquivo CSV, divide em train e test 
	"""

	data = np.loadtxt(file_name, dtype=object, delimiter=';')

	np.random.shuffle(data)
	n = len(data)
	K = int(2*n/3)
	training, test = data[:K], data[K:]

	n = len(training[0])

	# Slice
	training = training[:,:n-1].astype(float), training[:,n-1]
	test = test[:,:n-1].astype(float), test[:,n-1]

	return training, test


def handle_classes(input_classes):
	"""
	Praticamente uma variável aleatória que mapeia a um número
	"""
	classes = list(set(input_classes))

	mapeia = list()

	for x in input_classes:
		mapeia.append(classes.index(x))

	assert(len(input_classes) == len(mapeia))

	return mapeia

# Modelo basico de "num_hlayers" camada onde inicializamos um modelo sequencial
# com suas funcoes de ativacao, e o compilamos usando um otimizador e
# acuracia como metrica.
def base_model(num_features, num_neurons, num_classes, num_hlayers, learn_rate):
	model = Sequential()

	# input layer
	model.add(Dense(num_neurons, input_dim=num_features, kernel_initializer='normal', activation='sigmoid'))

	# hidden layers
	for i in range(num_hlayers-1):
		model.add(Dense(num_neurons, kernel_initializer='normal', activation='sigmoid'))
	
	# Output layer
	model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax', name='preds'))

	# Adam optimizer
	# recomendado para quantidade maiores de layers
	adam = keras.optimizers.Adam(lr=learn_rate)
	model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

	return model


def main(input_file, epochs, hlayers, neuros, bsize, learn_rate):
	head_of_file = 'Epochs: ' + epochs + '\n'
	head_of_file += 'Hidden Layers: ' + hlayers + '\n'
	head_of_file += 'Number of neuros: ' + neuros + '\n'
	head_of_file += 'Batch Size: ' + bsize + '\n'
	head_of_file += 'Learn Rate: ' + learn_rate + '\n\n'

	output_file_name = 'out_epochs_' + epochs + '__hlayers_' + hlayers \
	 + '__neuros_' + neuros + '__bsize_' + bsize + '__learn_rate_' + learn_rate


	# handle types
	epochs = int(epochs)
	hlayers = int(hlayers)
	neuros = int(neuros)
	bsize = int(bsize)
	learn_rate = float(learn_rate)

	(X_train, y_train), (X_test, y_test) = get_values_from_csv(input_file)

	# insanity check
	assert(len(set(y_train)) == len(set(y_test)))

	c_w = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)

	y_train = np_utils.to_categorical(handle_classes(y_train))
	y_test = np_utils.to_categorical(handle_classes(y_test))

	num_classes = y_train.shape[1]
	num_features = X_train.shape[1]

	model = base_model(num_features, neuros, num_classes, hlayers, learn_rate)

	# O metodo summary revela quais sao as camadas
	# que formam o modelo, seus formatos e o numero
	# de parametros envolvidos em cada etapa.
	model.summary()

	result = model.fit(X_train, y_train, validation_data=(X_test, y_test),
		epochs=epochs,
		batch_size=bsize,
		verbose=0,
		class_weight=c_w)

	# Avaliacao da performance do nosso primeiro modelo.
	scores = model.evaluate(X_test, y_test, verbose=0)
	print("Erro de: %.2f%%" % (100-scores[1]*100))
	# print(result.history['acc'])
	# print(len(result.history['acc']))

	plt.plot(range(len(result.history['acc'])), result.history['acc'])
	plt.xlabel('Epochs')
	plt.ylabel('Acc')
	# plt.show()
	plt.savefig(output_file_name + '.png')

	with open(output_file_name + '.txt', 'w') as f:
		f.write(head_of_file)
		f.write("Accuracy: %.2f%%\n" % scores[1])
		f.write("Erro de: %.2f%%" % (100-scores[1]*100))


if __name__ == '__main__':
	params = sys.argv[1:]

	# epochs
	# hidden layers
	# neurons
	# batch size
	# learn rate

	if len(params) < 5:
		print('TP3 - Redes Neurais Artificiais - Yuri Niitsuma<ignitzhjfk@gmail.com>')
		description = '\tUsage: python3 main.py input_data epochs hlayers neuros bsize learnrate'
		print(description)
		sys.exit(1)

	main(*params)


