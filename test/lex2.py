class State(object):
    def __init__(self, id, is_end_state, edges, token):
        self.id = id
        self.is_end_state = is_end_state
        self.edges = edges
        self.token = token
state0 = State(0, True, {'!': 1, '#': 1, '$': 1, '%': 1, '&': 2, '+': 3, '-': 4, '/': 5, '0': 6, '1': 6, '2': 6, '3': 6, '4': 6, '5': 6, '6': 6, '7': 6, '8': 6, '9': 6, '=': 7, '@': 1, '^': 1, 'a': 8, 'b': 8, 'c': 8, 'd': 8, 'e': 8, 'f': 8, 'g': 8, 'h': 8, 'i': 8, 'j': 8, 'k': 8, 'l': 8, 'm': 8, 'n': 8, 'o': 8, 'p': 8, 'q': 8, 'r': 8, 's': 8, 't': 8, 'u': 8, 'v': 8, 'w': 8, 'x': 8, 'y': 8, 'z': 8}, ['Var', 'Special', 'Num'])
state1 = State(1, True, {'!': 1, '#': 1, '$': 1, '%': 1, '@': 1, '^': 1}, ['Special'])
state2 = State(2, True, {}, ['And'])
state3 = State(3, True, {}, ['Add'])
state4 = State(4, True, {}, ['Minus'])
state5 = State(5, True, {}, ['Divide'])
state6 = State(6, True, {'0': 6, '1': 6, '2': 6, '3': 6, '4': 6, '5': 6, '6': 6, '7': 6, '8': 6, '9': 6}, ['Num'])
state7 = State(7, True, {}, ['Equal'])
state8 = State(8, True, {'a': 8, 'b': 8, 'c': 8, 'd': 8, 'e': 8, 'f': 8, 'g': 8, 'h': 8, 'i': 8, 'j': 8, 'k': 8, 'l': 8, 'm': 8, 'n': 8, 'o': 8, 'p': 8, 'q': 8, 'r': 8, 's': 8, 't': 8, 'u': 8, 'v': 8, 'w': 8, 'x': 8, 'y': 8, 'z': 8}, ['Var'])
states = [state0, state1, state2, state3, state4, state5, state6, state7, state8]
def get_input(path):
    ret = []
    with open(path) as f:
        for line in f.readlines():
            ret.extend(line.strip().split(' '))
    return ret


def analysis(texts):
    ret = []
    for word, i in zip(texts, range(len(texts))):
        cur = state0
        for c, j in zip(word, range(len(word))):
            next = cur.edges.get(c, None)
            if next is None:
                print('在第'+str(i+1)+'个单词'+str(j+1)+'个字符处, 正规表达式无法匹配')
                return None
            cur = states[next]
        if cur.is_end_state:
            if cur.token is None:
                print("在第", i+1, '个单词处, 单词未结束或书写错误, 正规表达式无法匹配')
                return None
            else:
                ret.append(cur.token[0])
        else:
            print("在第", i+1, '个单词处, 单词未结束或书写错误, 正规表达式无法匹配')
            return None
    return ret


def lex_output(tokens, path):
    s = ''
    for token in tokens:
        s += str(token)+"  "
    s += "\n"
    with open(path, 'w+') as f:
        f.write(s)
        f.flush()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('未指定完全输入输出路径')
        quit()
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    in_text = get_input(input_path)
    tokens = analysis(in_text)
    if tokens is None:
        quit()
    lex_output(tokens, output_path)