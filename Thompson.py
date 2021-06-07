# Universidad del Valle de Guatemala
# Diseno de Lenguajes de Programacion - Seccion 10
# Proyecto 3
# Maria Fernanda Estrada 14198
# Junio 2021



# Para generar graficas
from graphviz import Digraph


# Simbolos y variables
epsilon = 'ε'
or_symbol = "|"
and_symbol = "~"
kleen_symbol = "*"
positive_closure_symbol = "+"
zero_or_one_symbol = "?"
state_id_counter = 0


# Crear diccionario con informacion del automata
def create_fa():
    fa = {
        'states': set(),
        'transitions': [],
        'initial_state': '',
        'final_states': []      
    }
    return fa


# OR (Thompson)
def create_or_fa(fas,fat):
    global state_id_counter

    # Estado inicial
    new_fa = create_fa()
    initial_state = state_id_counter
    state_id_counter += 1
    new_fa['states'].add(initial_state)
    new_fa['initial_state'] = initial_state

    # Estado final
    final_state = state_id_counter
    state_id_counter += 1
    new_fa['states'].add(final_state)
    new_fa['final_states'].append(final_state)
    
    # Juntar en el AF las transiciones y estados de FAS y FAT
    new_fa['states'].update(fas['states'])
    new_fa['states'].update(fat['states'])
    new_fa['transitions'] += fas['transitions']
    new_fa['transitions'] += fat['transitions']

    # Transiciones segun grafica de OR
    new_fa['transitions'].append({
        'from':initial_state,
        'to':fas['initial_state'],
        'symbol':epsilon
    })
    new_fa['transitions'].append({
        'from':initial_state,
        'to':fat['initial_state'],
        'symbol':epsilon
    })
    new_fa['transitions'].append({
        'from':fas['final_states'][0],
        'to':final_state,
        'symbol':epsilon
    })
    new_fa['transitions'].append({
        'from':fat['final_states'][0],
        'to':final_state,
        'symbol':epsilon
    })

    return new_fa


# AND (Thompson)
def create_and_fa(fas,fat):
    # Estado inicial y final
    new_fa = create_fa()
    new_fa['initial_state'] = fas['initial_state']
    new_fa['final_states'].append(fat['final_states'][0])
    
    # Transiciones segun grafica AND
    # Las transiciones y estados de cualquiera de las dos FA se copian normal
    new_fa['states'].update(fas['states'])
    new_fa['transitions'] += fas['transitions']
    
    # Se debe verificar que el estado final de FAS se convierta en el estado inicial de FAT, cambiar transiciones y estados correspondientes
    for state in fat['states']:
        if(state != fat['initial_state']):
            new_fa['states'].add(state)
    for transition in fat['transitions']:
        if(transition['from'] == fat['initial_state']):
            transition['from'] = fas['final_states'][0]
        new_fa['transitions'].append(transition)

    return new_fa


# KLEEN (Thompson)
def create_kleen_fa(fas):
    global state_id_counter

    # Estado inicial
    new_fa = create_fa()
    initial_state = state_id_counter
    state_id_counter += 1
    new_fa['states'].add(initial_state)
    new_fa['initial_state'] = initial_state

    # Estado final
    final_state = state_id_counter
    state_id_counter += 1
    new_fa['states'].add(final_state)
    new_fa['final_states'].append(final_state)
    
    # Se juntan las transiciones y estados de FAS
    new_fa['states'].update(fas['states'])
    new_fa['transitions'] += fas['transitions']

    # Transiciones segun grafica KLEEN
    new_fa['transitions'].append({
        'from':initial_state,
        'to':fas['initial_state'],
        'symbol':epsilon
    })
    new_fa['transitions'].append({
        'from':fas['final_states'][0],
        'to':final_state,
        'symbol':epsilon
    })
    new_fa['transitions'].append({
        'from':initial_state,
        'to':final_state,
        'symbol':epsilon
    })
    new_fa['transitions'].append({
        'from':fas['final_states'][0],
        'to':fas['initial_state'],
        'symbol':epsilon
    })

    return new_fa


# POSITIVE CLOSURE (Thompson)
def create_positive_closure_fa(fas):
    global state_id_counter

    # Estado inicial
    new_fa = create_fa()
    initial_state = state_id_counter
    state_id_counter += 1
    new_fa['states'].add(initial_state)
    new_fa['initial_state'] = initial_state

    # Estado final
    final_state = state_id_counter
    state_id_counter += 1
    new_fa['states'].add(final_state)
    new_fa['final_states'].append(final_state)
    
    # Juntar los estados y transiciones de FAS
    new_fa['states'].update(fas['states'])
    new_fa['transitions'] += fas['transitions']

    # Transiciones segun grafica POSITIVE CLOSURE (igual a KLEEN pero tiene que estar al menos 1 vez)
    new_fa['transitions'].append({
        'from':initial_state,
        'to':fas['initial_state'],
        'symbol':epsilon
    })
    new_fa['transitions'].append({
        'from':fas['final_states'][0],
        'to':final_state,
        'symbol':epsilon
    })
    new_fa['transitions'].append({
        'from':fas['final_states'][0],
        'to':fas['initial_state'],
        'symbol':epsilon
    })

    return new_fa


# ZERO OR ONE (Thompson)
def create_zero_one_fa(fas):
    global state_id_counter

    # Estado inicial
    new_fa = create_fa()
    initial_state = state_id_counter
    state_id_counter += 1
    new_fa['states'].add(initial_state)
    new_fa['initial_state'] = initial_state

    # Estado final
    final_state = state_id_counter
    state_id_counter += 1
    new_fa['states'].add(final_state)
    new_fa['final_states'].append(final_state)
    
    # Juntar los estados y transiciones de FAS
    new_fa['states'].update(fas['states'])
    new_fa['transitions'] += fas['transitions']

    # Transiciones segun grafica ZERO OR ONE (igual a KLEEN pero no puede estar varias veces, solo 1 o ninguna)
    new_fa['transitions'].append({
        'from':initial_state,
        'to':fas['initial_state'],
        'symbol':epsilon
    })
    new_fa['transitions'].append({
        'from':fas['final_states'][0],
        'to':final_state,
        'symbol':epsilon
    })
    new_fa['transitions'].append({
        'from':initial_state,
        'to':final_state,
        'symbol':epsilon
    })

    return new_fa


# Para leer dentro del arbol  hasta abajo y formar AFN
def recursive(node):
    global state_id_counter

    # Si son hojas (alfabeto)
    if(node['left_node'] == None and node['right_node'] == None):
        new_fa = create_fa()
        initial_state = state_id_counter
        state_id_counter += 1
        new_fa['states'].add(initial_state)
        new_fa['initial_state'] = initial_state

        final_state = state_id_counter
        state_id_counter += 1
        new_fa['states'].add(final_state)
        new_fa['final_states'].append(final_state)

        new_fa['transitions'].append({
            'from':initial_state,
            'to':final_state,
            'symbol':node['content']
        })

        return new_fa

    # Si el nodo tiene un simbolo OR
    if(node['content'] == or_symbol):
        fas = recursive(node['left_node'])
        fat = recursive(node['right_node'])
        return create_or_fa(fas, fat)

    # Si el nodo tiene un simbolo AND
    elif(node['content'] == and_symbol):
        fas = recursive(node['left_node'])
        fat = recursive(node['right_node'])
        return create_and_fa(fas, fat)
    
    # Si el nodo tiene un simbolo KLEEN
    elif(node['content'] == kleen_symbol):
        fas = recursive(node['left_node'])
        return create_kleen_fa(fas)
    
    # Si el nodo tiene un simbolo POSITIVE CLOSURE
    elif(node['content'] == positive_closure_symbol):
        fas = recursive(node['left_node'])
        return create_positive_closure_fa(fas)
    
    # Si el nodo tiene un simbolo ZERO OR ONE
    elif (node['content'] == zero_or_one_symbol):
        fas = recursive(node['left_node'])
        return create_zero_one_fa(fas)


# Thompson
def thompson(node):
    fan = recursive(node)
    return fan