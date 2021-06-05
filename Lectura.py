
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
        'id': id,
        'regex': regex,
        'is_keyword': is_keyword,
        'except_keywords': except_keywords
    }

    tokens.append(token)

def leer_atg(filename):
    global tokens
    global characters
    ignore = set()
    leer_atg
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
    return tokens, ignore
                