# Universidad del Valle de Guatemala
# Diseno de Lenguajes de Programacion - Seccion 10
# Proyecto 1 - Generacion de Arbol para Thompson y Directo
# Maria Fernanda Estrada 14198
# Marzo 2021



# Para generar graficas
from graphviz import Digraph


# Simbolos
epsilon = 'ε'
or_symbol = '|'
and_symbol = '~'
kleen_symbol = '*'
positive_closure_symbol = '+'
zero_or_one_symbol = '?'


# Crear diccionario con informacion del nodo
def create_node(content, left_node = None, right_node = None):
    node = {
        'content': content,
        'left_node': left_node,
        'right_node': right_node      
    }
    return node

# Leer contenido dentro de regex y convertir a un arbol
def read_r(node, alphabet):

    content = node['content']

    if type(content) is int or len(content) == 0:
        return

    if len(content) == 1:
        node['content'] = content[0]
        return

    k = -1
    # Identificar OR antes que el resto
    parenthesis = 0
    for i in reversed(range(len(content))):
        if(content[i] == ')'):
            parenthesis += 1
        elif(content[i] == '('):
            parenthesis -= 1
        elif(content[i] == or_symbol):
            if(parenthesis == 0):
                k = i
                break

    # Si es OR, separar la cadena en el indice donde se encuentre
    if(k!=-1):
        left_i = content[:k]
        right_i = content[k+1:]
        node['content'] = or_symbol
        node['left_node'] = create_node(left_i)
        node['right_node'] = create_node(right_i)
        read_r(node['left_node'], alphabet)
        read_r(node['right_node'], alphabet)

    # Si no es OR
    elif(content[-1] == ')'):
        parenthesis = 0
        for a in reversed(range(len(content))):
            if(content[a] == ')'):
                parenthesis += 1
            elif(content[a] == '('):
                parenthesis -= 1
                if(parenthesis == 0):
                    if(a == 0):
                        node['content'] = content[1:-1]
                        read_r(node, alphabet)
                        break
                    else:
                        node['content'] = and_symbol
                        node['left_node'] = create_node(content[:a])
                        node['right_node'] = create_node(content[a:])
                        read_r(node['left_node'], alphabet)
                        read_r(node['right_node'], alphabet)
                        break

    # Si es + , * o ?
    elif(content[-1] == kleen_symbol or content[-1] == positive_closure_symbol or content[-1] == zero_or_one_symbol):
        if(content[-2] == ')'):
            parenthesis = 0
            for a in reversed(range(len(content))):
                if(content[a] == ')'):
                    parenthesis += 1
                elif(content[a] == '('):
                    parenthesis -= 1
                    if(parenthesis == 0):
                        if(a == 0):
                            node['content'] = content[-1]
                            node['left_node'] = create_node(content[:-1])
                            read_r(node['left_node'], alphabet)
                        else:
                            node['content'] = and_symbol
                            node['left_node'] = create_node(content[:a])
                            node['right_node'] = create_node(content[-1], create_node(content[a:-1]))
                            read_r(node['left_node'], alphabet)
                            read_r(node['right_node']['left_node'], alphabet)
                        break
        else:
            if(len(content) == 2):
                node['content'] = content[-1]
                node['left_node'] = create_node(content[-2])
                read_r(node['left_node'], alphabet)
            else:
                node['content'] = and_symbol
                node['left_node'] = create_node(content[:-2])
                node['right_node'] = create_node(content[-1], create_node(content[-2]))
                read_r(node['left_node'], alphabet)
                read_r(node['right_node']['left_node'], alphabet)
    else:
        node['content'] = and_symbol
        node['left_node'] = create_node(content[:-1])
        node['right_node'] = create_node(content[-1])
        read_r(node['left_node'], alphabet)
        read_r(node['right_node'], alphabet)


# Para graficar el arbol de la expresion regular
count = 0
def grph(node, d):
    global count
    count2 = count
    d.node(str(count2), label = str(node['content']), shape='circle')
    count += 1
    if (node['left_node']):
        d.edge(str(count2), str(count))
        grph(node['left_node'], d)
    if (node['right_node']):
        d.edge(str(count2), str(count))
        grph(node['right_node'], d)


# Para graficar el arbol del algoritmo Directo
def grph_2(node, d):
    global count
    count2 = count
    d.node(str(count2), label = str(node['content']) + '\n' + str(node['first_pos']) + str(node['last_pos']), shape='circle')
    count += 1
    if (node['left_node']):
        d.edge(str(count2), str(count))
        grph_2(node['left_node'], d)
    if (node['right_node']):
        d.edge(str(count2), str(count))
        grph_2(node['right_node'], d)

# Para graficar Thompson o Subconjuntos o Directo
def grph_fas(fas, name):
    di = Digraph(comment='Finite State Machine')
    di.node("start")
    di.edge("start", str(fas["initial_state"]))
    di.attr(rankdir='LR')
    for state in fas['states']:
        if(state in fas['final_states']):
            di.node(str(state), shape="doublecircle")
        else:
            di.node(str(state), shape="circle")
    for transition in fas['transitions']:
        di.edge(str(transition['from']), str(transition['to']), label=str(transition['symbol']))
    di.render(name + '.gv', view=True)