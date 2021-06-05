# Universidad del Valle de Guatemala
# Diseno de Lenguajes de Programacion - Seccion 10
# Proyecto 1 - Algoritmo Directo (Generacion de AFD a partir de regex)
# Maria Fernanda Estrada 14198
# Marzo 2021



# Para generar graficas
from graphviz import Digraph
from Arbol import create_node
from Thompson import create_fa


# Simbolos y variables
epsilon = 'ε'
or_symbol = "|"
and_symbol = "~"
kleen_symbol = "*"
positive_closure_symbol = "+"
zero_or_one_symbol = "?"


# Agregar hashtag hasta arriba
def add_hashtag(node):
    hashtag = create_node('#')
    root = create_node(and_symbol,node,hashtag)
    return root


# Calcular first pos y last pos de cada nodo
def add_first_last_pos(node, symbols):
    if(node['left_node'] and 'first_pos' not in node['left_node']):
        add_first_last_pos(node['left_node'], symbols)

    if(node['right_node'] and'first_pos' not in node['right_node']):
        add_first_last_pos(node['right_node'], symbols)

    if(not node['left_node'] and not node['right_node']):
        symbols.append(node['content'])
        symbol_number = len(symbols) - 1
        if(node['content'] == epsilon):
            node['nullable'] = True
        else:
            node['nullable'] = False
        node['first_pos'] = {symbol_number}
        node['last_pos'] = {symbol_number}

    else:
        if(node['content'] == and_symbol):
            node['first_pos'] = set()
            node['first_pos'].update(node['left_node']['first_pos'])

            if(node['left_node']['nullable'] == True):
                node['first_pos'].update(node['right_node']['first_pos'])

            node['last_pos'] = set()
            node['last_pos'].update(node['right_node']['last_pos'])

            if(node['right_node']['nullable'] == True):
                node['last_pos'].update(node['left_node']['last_pos'])

            if(node['left_node']['nullable'] and node['right_node']['nullable']):
                node['nullable'] = True

            else:
                node['nullable'] = False

        elif(node['content'] == or_symbol):
            node['first_pos'] = set()
            node['first_pos'].update(node['left_node']['first_pos'])
            node['first_pos'].update(node['right_node']['first_pos'])

            node['last_pos'] = set()
            node['last_pos'].update(node['right_node']['last_pos'])
            node['last_pos'].update(node['left_node']['last_pos'])

            if(node['left_node']['nullable'] or node['right_node']['nullable']):
                node['nullable'] = True
            else:
                node['nullable'] = False

        elif(node['content'] == kleen_symbol or node['content'] == zero_or_one_symbol):
            node['first_pos'] = set()
            node['first_pos'].update(node['left_node']['first_pos'])

            node['last_pos'] = set()
            node['last_pos'].update(node['left_node']['last_pos'])
            node['nullable'] = True

        elif(node['content'] == positive_closure_symbol):
            node['first_pos'] = set()
            node['first_pos'].update(node['left_node']['first_pos'])

            node['last_pos'] = set()
            node['last_pos'].update(node['left_node']['last_pos'])
            node['nullable'] = False

    return symbols


# Calcular follow pos segun reglas vistas en clase
def get_follow_pos(node, symbol, follow_pos = set()):
    if(node['left_node'] != None):
        follow_pos.update(get_follow_pos(node['left_node'], symbol, follow_pos))

    if(node['right_node'] != None):
        follow_pos.update(get_follow_pos(node['right_node'], symbol, follow_pos))

    if(node['content'] == and_symbol):
        if(symbol in node['left_node']['last_pos']):
            follow_pos.update(node['right_node']['first_pos'])

    elif(node['content'] == kleen_symbol or node['content'] == positive_closure_symbol):
        if(symbol in node['last_pos']):
            follow_pos.update(node['first_pos'])

    return follow_pos


# Verificar estados y generar AFD
def check_state(node, afd, state, symbols, alphabet):
    for letter in alphabet:
        new_state = set()
        for i in range(len(symbols)):
            if(symbols[i] == letter and i in state):
                new_state.update(get_follow_pos(node, i, set()))
        if(len(new_state)>0):
            new_state = frozenset(new_state)
            if(new_state not in afd['states']):
                afd['states'].add(new_state)
                if(symbols.index('#') in new_state):
                    afd['final_states'].append(new_state)
                check_state(node, afd, new_state, symbols, alphabet)
            afd['transitions'].append({'from': state, 'to': new_state, 'symbol': letter})


# Directo
def make_direct_afd(node, symbols, alphabet):
    afd = create_fa()
    initial_state = node['first_pos']
    initial_state = frozenset(initial_state)
    afd['initial_state'] = initial_state
    afd['states'].add(initial_state)
    if(symbols.index('#') in initial_state):
        afd['final_states'].append(initial_state)
    check_state(node, afd, initial_state, symbols, alphabet)

    return afd