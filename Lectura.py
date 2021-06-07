# Universidad del Valle de Guatemala
# Diseno de Lenguajes de Programacion - Seccion 10
# Proyecto 3
# Maria Fernanda Estrada 14198
# Junio 2021



seccion_actual = 'inicio'
current_id = ''
characters = {}
tokens = []

def create_character(id, st):
    global characters
    new_set = set()
    comillas = False
    char_range = False
    last_char = -1
    word = ''
    prev_op = '+'
    for s in st:
        if(s=='"' or s=="'"):
            comillas = not comillas
        elif(comillas):
            if(char_range and last_char != 1):
                for i in range(last_char, ord(s)+1):
                    new_set.add(i)
                last_char = -1
                char_range = False
            else:
                new_set.add(ord(s))
                last_char = ord(s)
        elif(word.startswith('CHR(') and word.endswith(')')):
            new_set.add(int(word[4:-1]))
            word = ''
        else:
            if(s in ' +-.'):
                if(word == 'ANY'):
                    for i in range(256):
                        new_set.add(i)
                    word = ''
                elif(word.strip() == '..'):
                    char_range = True
                    word = ''
                elif(word in characters):
                    if(prev_op == '+'):
                        new_set.update(characters[word])
                    else:
                        new_set -= characters[word]
                    word = ''
                if(s == '.'):
                    word += '.'
                if(s in '+-'):
                    prev_op = s
            else:
                word += s

    character = {
        id: new_set 
    }

    characters[id] = new_set

    print(character)

def create_token(id, st, is_keyword):
    global characters
    comillas = False
    except_keywords = False
    word = ''
    regex = []
    for s in st:
        if(s=='"'):
            comillas = not comillas
        if(s!='"' and comillas):
            regex.append(ord(s))
        elif(s in ' ()}{][|".'):
            if(word.strip() == 'EXCEPT KEYWORDS'):
                except_keywords = True
                word = ''
                continue
            if(word.strip() in characters):
                regex.append('(')
                for c in characters[word.strip()]:
                    regex.append(c)
                    regex.append('|')
                regex = regex[:-1]
                regex.append(')')
                word = ''
            if(s == '{'):
                regex.append('(')
            elif(s == '}'):
                regex.append(')')
                regex.append('*')
            elif(s == '['):
                regex.append('(')
            elif(s == ']'):
                regex.append(')')
                regex.append('?')
            elif(s not in ' ."'):
                regex.append(s)
            elif(s == ' '):
                word += ' '
        else:
            word += s

    token = {
        'id': id.strip(),
        'regex': regex,
        'is_keyword': is_keyword,
        'except_keywords': except_keywords
    }

    tokens.append(token)

def find_end(raw, index):
    opens = 1
    for i in range(index+1, len(raw)):
        if(raw[index] == '('):
            if(raw[i] == '('):
                opens += 1
            elif(raw[i] == ')'):
                opens -= 1
        elif(raw[index] == '{'):
            if(raw[i] == '{'):
                opens += 1
            elif(raw[i] == '}'):
                opens -= 1
        elif(raw[index] == '['):
            if(raw[i] == '['):
                opens += 1
            elif(raw[i] == ']'):
                opens -= 1

        if(opens == 0):
            return i
    return -1

def production(raw, indents, productions, first_call=False):
    global tokens
    is_code = False
    is_new_token = False
    out_code = ''
    word_buffer = ''
    token_buffer = ''
    first_tokens = set()
    first_tokens_complete = False
    if_tokens = set()
    if_position = 0
    if(not first_call and '|' in raw):
        indents += 1
    i=0
    while(i < len(raw)):
        if(raw[i] == '(' and i+1 < len(raw) and raw[i+1] == '.'):
            is_code = True
            out_code += '  '*indents
            i += 2
            continue

        elif(raw[i] == '.' and i+1 < len(raw) and raw[i+1] == ')'):
            is_code = False
            out_code += '\n'
            i += 2
            continue

        if(is_code):
            out_code += raw[i]
            i+=1
            continue

        if(raw[i] == '"'):
            is_new_token = not is_new_token
            if(not is_new_token):
                print('NEW TOKEN: ' + token_buffer)
                token = {
                    'id': token_buffer,
                    'regex': [ord(token_buffer)],
                    'is_keyword': False,
                    'except_keywords': False
                }

                tokens.append(token)
                out_code += '  '*indents
                out_code += "advance('{}')".format(token_buffer)
                out_code += '\n'
                if(not first_tokens_complete):
                    first_tokens.add(token_buffer)
                    if_tokens.add(token_buffer)
                    first_tokens_complete = True
            token_buffer = ''
            i+=1
            continue

        if(is_new_token):
            token_buffer += raw[i]
            i+=1
            continue

        if(raw[i] in '({['):
            end = find_end(raw, i)
            new_indents = indents
            if(raw[i] in '{['):
                new_indents += 1
            new_code, ft = production(raw[i+1:end], new_indents, productions)
            if(not first_tokens_complete):
                first_tokens.update(ft)
                if_tokens.update(ft)
            if(raw[i] == '{'):
                out_code += '  '*indents
                out_code += 'while('
                for f in ft:
                    out_code += "lookahead('{}') or ".format(f)
                out_code = out_code[:-4]
                out_code += '):'
                out_code += '\n'
                first_tokens_complete = True
            elif(raw[i] == '['):
                out_code += '  '*indents
                out_code += 'if('
                for f in ft:
                    out_code += "lookahead('{}') or ".format(f)
                out_code = out_code[:-4]
                out_code += '):'
                out_code += '\n'
            out_code += new_code
            i = end+1
            continue

        if(raw[i] == '|'):
            new_if_line = '  '*(indents-1)
            new_if_line += 'if('
            for f in if_tokens:
                new_if_line += "lookahead('{}') or ".format(f)
            new_if_line = new_if_line[:-4]
            new_if_line += '):\n'
            out_code = out_code[:if_position] + new_if_line + out_code[if_position:]
            if_position = len(out_code)
            first_tokens_complete = False
            if_tokens = set()
            i+=1
            continue

        if(raw[i] in '	 \n'):
            i+=1
            continue

        word_buffer += raw[i]

        if(i+1 == len(raw) or (raw[i+1] in '	 )(][}{|"\n' and raw[i] not in ' 	')):
            word_buffer = word_buffer.strip()
            found = False
            for token in tokens:
                if(word_buffer == token['id']):
                    out_code += '  '*indents
                    out_code += "advance('{}')".format(word_buffer)
                    out_code += '\n'
                    if(not first_tokens_complete):
                        first_tokens.add(token['id'])
                        if_tokens.add(token['id'])
                        first_tokens_complete = True
                    found = True
                    break
            if(not found):
                if('<' in word_buffer and '>' in word_buffer):
                    word_buffer = word_buffer.replace('<','(')
                    word_buffer = word_buffer.replace('>',')')
                else:
                    word_buffer += '()'
                if(not first_tokens_complete):
                    for p in productions:
                        if(p['name'][:p['name'].index('(')] == word_buffer[:word_buffer.index('(')]):
                            first_tokens.update(p['first_tokens'])
                            if_tokens.update(p['first_tokens'])
                            first_tokens_complete = True
                            break
                out_code += '  '*indents
                out_code += word_buffer
                out_code += '\n'
            word_buffer = ''
            i+=1
            continue
        i+=1

    if(if_position != 0):
        new_if_line = '  '*(indents-1)
        new_if_line += 'elif('
        for f in if_tokens:
            new_if_line += "lookahead('{}') or ".format(f)
        new_if_line = new_if_line[:-4]
        new_if_line += '):\n'
        out_code = out_code[:if_position] + new_if_line + out_code[if_position:]

    return out_code, first_tokens

def leer_atg(filename):
    global tokens
    global characters
    ignore = set()
    production_name = ''
    lines_buffer = ''
    out_file = ''
    productions = []
    with open(filename, 'r', encoding='utf-8') as fp:
        for line in fp:
            line = line.strip()
            if(line.startswith('COMPILER')):
                seccion_actual = 'compiler'
            elif(line.startswith('CHARACTERS')):
                seccion_actual = 'characters'
            elif(line.startswith('KEYWORDS')):
                seccion_actual = 'keywords'
            elif(line.startswith('TOKENS')):
                seccion_actual = 'tokens'
            elif(line.startswith('PRODUCTIONS')):
                seccion_actual = 'productions'
            elif(line.startswith('IGNORE')):
                arreglo = line.strip().split(' ', 1)
                if(arreglo[1] in characters):
                    ignore = characters[arreglo[1]]

            if(seccion_actual == 'compiler'):
                continue
            elif(seccion_actual == 'characters'):
                if('=' in line):
                    arreglo = line.split('=', 1)
                    create_character(arreglo[0].strip(), arreglo[1].strip())
            elif(seccion_actual == 'keywords'):
                if('=' in line):
                    arreglo = line.split('=', 1)
                    create_token(arreglo[0].strip(), arreglo[1].strip(), True)
                    
            elif(seccion_actual == 'tokens'):
                if('=' in line):
                    arreglo = line.split('=', 1)
                    create_token(arreglo[0].strip(), arreglo[1].strip(), False)

            elif(seccion_actual == 'productions'):
                line = line.strip()
                if(len(line) == 0):
                    continue
                if(not production_name):
                    if('=' in line):
                        arreglo = line.split('=', 1)
                        production_name = arreglo[0].strip()
                        if('<' in production_name and '>' in production_name):
                            production_name = production_name.replace('<','(')
                            production_name = production_name.replace('>',')')
                        else:
                            production_name += '()'
                        
                        lines_buffer += arreglo[1].strip()
                        if(len(lines_buffer) > 0 and lines_buffer[-1] == '.'):
                            productions.append({'name': production_name, 'body': lines_buffer[:-2], 'first_tokens':set()})
                            lines_buffer = ''
                            production_name = ''
                elif(line[-1] == '.'):
                    if(len(line) > 0):
                        lines_buffer += line[:-1]
                    productions.append({'name': production_name, 'body': lines_buffer[:-2], 'first_tokens':set()})
                    lines_buffer = ''
                    production_name = ''
                else:
                    lines_buffer += line

    for p in reversed(productions):
        code, first_tokens = production(p['body'], 1, productions, True)
        p['first_tokens'] = first_tokens
        print('{}: {}'.format(p['name'],p['first_tokens']))
        out_file += 'def ' + p['name'] + ':'
        out_file += '\n'
        out_file += code
        out_file += '\n\n'

    print(out_file)
    return tokens, ignore, out_file
                