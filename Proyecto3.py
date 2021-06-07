# Universidad del Valle de Guatemala
# Diseno de Lenguajes de Programacion - Seccion 10
# Proyecto 3
# Maria Fernanda Estrada 14198
# Junio 2021



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

tokens, ignore, text_file = leer_atg(sys.argv[1])

text_file += '''
from Scanner import extract_tokens
import sys

past_token = {}
detected_tokens = []

def lookahead(token):
  global detected_tokens
  if(detected_tokens[0]['id'] == token):
    return True
  else:
    return False

def advance(token):
  global detected_tokens
  global past_token
  if(detected_tokens[0]['id'] == token):
    past_token = detected_tokens.pop(0)
  else:
    raise Exception('ERROR: token {}'.format(token))

def last_token():
  global past_token
  return past_token

detected_tokens = extract_tokens(sys.argv[1])

print('--- Leyendo archivo: {} ---\n'.format(sys.argv[1]))

try:
  Expr()
except Exception as e:
  print(e)
'''

f = open('Parser.py', 'w', encoding='utf-8')
f.write(text_file)
f.close()

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
    for afd in afds:
        active_afds.append(afd)
    current_states = []

    for afd in afds:
        current_states.append(afd['afd']['initial_state'])

    cadena_i = 0
    palabra = ''
    tokens_encontrados = []
    encontrado = False
    token_id = ''
    token_found_at = -1
    while(cadena_i < len(cadena)):
        s = cadena[cadena_i]
        j = 0
        one_found = False
        while j < len(active_afds):
            
            afd = active_afds[j]['afd']
            
            found_transition = False
            for transition in afd['transitions']:
                if(transition['from'] == current_states[j] and transition['symbol'] == s):
                    current_states[j] = transition['to']
                    found_transition = True
                    one_found = True
                    break
            if(found_transition == False or cadena_i+1 == len(cadena)):
                if(current_states[j] in afd['final_states']):
                    token = active_afds[j]['token']
                    token_id = token['id']
                    token_found_at = cadena_i
                    encontrado = True
                active_afds.pop(j)
                current_states.pop(j)
            else:
                j+=1

        if(one_found):
            palabra += chr(s)
            cadena_i += 1

        if(len(active_afds) == 0):
            if(encontrado):
                #print('TOKEN ENCONTRADO: {} | string: {}'.format(token_id, repr(palabra)))
                tokens_encontrados.append({'id': token_id, 'value': palabra})
                token_id = ''
                encontrado = False
            else:
                print('TOKEN INVALIDO | string: {}'.format(repr(palabra)))

            palabra = ''

            active_afds = []
            for afd in afds:
                active_afds.append(afd)
            current_states = []
            for afd in afds:
                current_states.append(afd['afd']['initial_state'])

    return tokens_encontrados

def extract_tokens(filename):
    f = open(filename, 'r', encoding='utf-8')
    cadena = f.read()
    f.close()

    cadena_int = []

    for c in cadena:
        if(c not in ignore):
            cadena_int.append(ord(c))

    return simulate_det(cadena_int, afds)
'''

f = open('Scanner.py', 'w', encoding='utf-8')
f.write(archivo_string)
f.close()
