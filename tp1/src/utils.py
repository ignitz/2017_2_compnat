import math

# Colorir letras. Testado apenas no Linux.
CYAN = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

"""
Abaixo contém funções para imprimir com cor no terminal
Alguns tem como propósito de DEBUG
"""
def print_purple(msg, end=None):
	if end is None:
		print(CYAN + str(msg) + ENDC)
	else:
		print(CYAN + str(msg) + ENDC, end=end)

def print_blue(msg, end=None):
	if end is None:
		print(BLUE + str(msg) + ENDC)
	else:
		print(BLUE + str(msg) + ENDC, end=end)

def print_green(msg, end=None):
	if end is None:
		print(GREEN + str(msg) + ENDC)
	else:
		print(GREEN + str(msg) + ENDC, end=end)

def print_bold(msg, end=None):
    if end is None:
        print(BOLD + str(msg) + ENDC)
    else:
        print(BOLD + str(msg) + ENDC, end=end)

def print_warning(msg, end=None):
    if end is None:
        print(WARNING + str(msg) + ENDC)
    else:
        print(WARNING + str(msg) + ENDC, end=end)

# print errors in RED
def print_error(msg, end=None):
	if end is None:
		print(FAIL + str(msg) + ENDC)
	else:
		print(FAIL + str(msg) + ENDC, end=end)


def media(valores):
    soma = 0.0
    for v in valores:
        soma+=v
    return soma/len(valores)

def variancia(valores):
    _media = media(valores)
    soma = 0.0
    _variancia = 0.0

    for valor in valores:
        soma += math.pow((valor - _media), 2)
    _variancia = soma / float(len(valores))
    return _variancia

def desvio_padrao(valores):
    return math.sqrt(variancia(valores))

