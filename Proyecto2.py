# Universidad del Valle de Guatemala
# Diseno de Lenguajes de Programacion - Seccion 10
# Proyecto 2 - Programa principal (lectura de regex y cadena)
# Maria Fernanda Estrada 14198
# Abril 2021



# Para generar graficas
from graphviz import Digraph
# Importar funciones para generar Arbol
from Arbol import *
#
from Directo import *

from Lectura import leer_atg

import time
import sys


# Simbolos
epsilon = 'ε'
or_symbol = "|"
and_symbol = "~"
kleen_symbol = "*"
positive_closure_symbol = "+"
zero_or_one_symbol = "?"

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

tokens, ignore = leer_atg(sys.argv[1])

afds = []

for token in tokens:
    regex = token['regex']
    id = token['id']

    print('PROCESANDO TOKEN {} : {} | {} | {}'.format(id, regex, token['is_keyword'], token['except_keywords']))

    letters = remove_values_from_list(regex, '|')
    letters = remove_values_from_list(regex, '*')
    letters = remove_values_from_list(regex, '+')
    letters = remove_values_from_list(regex, '?')
    letters = remove_values_from_list(regex, '(')
    letters = remove_values_from_list(regex, ')')

    alphabet = set()
    for l in letters:
        alphabet.add(l)

    # Generar arbol
    node = create_node(regex)
    read_r(node, alphabet)
    d = Digraph(comment='Tree')
    grph(node, d)
    #d.render('Arbol 1.gv', view=True)


    # Directo
    node_pos = add_hashtag(node)
    sym = add_first_last_pos(node_pos, [])
    d2 = Digraph(comment='Tree2')
    grph_2(node_pos,d2)
    #d2.render('Arbol 2.gv', view=True)

    afd_direct = make_direct_afd(node_pos, sym, alphabet)

    afd = {
        'token': token,
        'afd' : afd_direct
    }

    afds.append(afd)
    
    #grph_fas(afd_direct, 'AFD (Directo)')

archivo_string = 'afds = ' + str(afds)
archivo_string += '\nignore = ' + str(ignore)
archivo_string += '''

import sys

def simulate_det(cadena, afds):
    active_afds = []
    for i in range(len(afds)):
        active_afds.append(i)
    current_states = []

    for afd in afds:
        current_states.append(afd['afd']['initial_state'])

    cadena_i = 0
    palabra = ''
    while(cadena_i < len(cadena)):
        s = cadena[cadena_i]
        encontrado = False
        encontrado_keyword = False
        one_found = False
        token_id = ''
        j = 0
        while j < len(active_afds):
            indx = active_afds[j]
            current_states[indx]
            afd = afds[indx]['afd']
            found_transition = False
            for transition in afd['transitions']:
                if(transition['from'] == current_states[indx] and transition['symbol'] == s):
                    current_states[indx] = transition['to']
                    found_transition = True
                    one_found = True
                    break
            if(found_transition == False or cadena_i+1 == len(cadena)):
                if(current_states[indx] in afd['final_states']):
                    token = afds[indx]['token']
                    if(not encontrado):
                        if(token['is_keyword']):
                            encontrado_keyword = True
                        token_id = token['id']
                    elif(encontrado_keyword and not token['is_keyword'] and not token['except_keywords']):
                        token_id = token['id']
                        encontrado_keyword = False
                    encontrado = True
                active_afds.remove(indx)
                j -= 1
            j += 1

        cadena_i += 1

        if(one_found):
            palabra += chr(s)

        if(len(active_afds) == 0):
            if(len(palabra) == 0):
                palabra += chr(s)
            elif(cadena_i+1 < len(cadena)):
                cadena_i -= 1

            if(encontrado):
                print('TOKEN ENCONTRADO: {} | string: {}'.format(token_id, repr(palabra)))
            else:
                print('TOKEN INVALIDO | string: {}'.format(repr(palabra)))
            
            active_afds = []
            for i in range(len(afds)):
                active_afds.append(i)
            current_states = []
            for afd in afds:
                current_states.append(afd['afd']['initial_state'])

            palabra = ''
            
f = open(sys.argv[1], 'r', encoding='utf-8')
cadena = f.read()
f.close()

cadena_int = []

for c in cadena:
    if(c not in ignore):
        cadena_int.append(ord(c))

simulate_det(cadena_int, afds)
'''

f = open('Scanner.py', 'w', encoding='utf-8')
f.write(archivo_string)
f.close()






    
