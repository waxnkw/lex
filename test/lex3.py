class State(object):
    def __init__(self, id, is_end_state, edges, token):
        self.id = id
        self.is_end_state = is_end_state
        self.edges = edges
        self.token = token
state0 = State(0, True, {'0': 1, '1': 1, '2': 1, '3': 1, '4': 2, '5': 1, '6': 1, '7': 3, '8': 1, '9': 1, '@': 4, 'a': 6, 'b': 9, 'c': 22, 'd': 23, 'e': 24, 'l': 11, 'm': 25, 'q': 12, 'w': 13}, ['many_m'])
state1 = State(1, False, {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, '@': 4}, None)
state2 = State(2, False, {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 15, '6': 1, '7': 1, '8': 1, '9': 1, '@': 4}, None)
state3 = State(3, False, {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 16, '9': 16, '@': 4}, None)
state4 = State(4, False, {'q': 5}, None)
state5 = State(5, False, {'q': 17}, None)
state6 = State(6, False, {'c': 10}, None)
state7 = State(7, False, {'c': 9}, None)
state8 = State(8, False, {'c': 19}, None)
state9 = State(9, False, {'a': 7, 'b': 9, 'd': 23}, None)
state10 = State(10, False, {'a': 7, 'b': 9, 'd': 29}, None)
state11 = State(11, False, {'c': 22, 'l': 11}, None)
state12 = State(12, False, {'q': 12, 'w': 13}, None)
state13 = State(13, False, {'e': 26}, None)
state14 = State(14, False, {'e': 30}, None)
state15 = State(15, False, {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 27, '7': 1, '8': 1, '9': 1, '@': 4}, None)
state16 = State(16, False, {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 28, '8': 1, '9': 1, '@': 4}, None)
state17 = State(17, False, {'d': 18}, None)
state18 = State(18, False, {'o': 20}, None)
state19 = State(19, False, {'o': 21}, None)
state20 = State(20, False, {'t': 8}, None)
state21 = State(21, False, {'m': 31}, None)
state22 = State(22, True, {}, ['token2'])
state23 = State(23, True, {}, ['token1'])
state24 = State(24, True, {}, ['token2'])
state25 = State(25, True, {'m': 25}, ['many_m'])
state26 = State(26, True, {}, ['token3'])
state27 = State(27, True, {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, '@': 4}, ['token3'])
state28 = State(28, True, {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 28, '6': 1, '7': 1, '8': 1, '9': 1, '@': 4}, ['token5'])
state29 = State(29, True, {'d': 14}, ['token1'])
state30 = State(30, True, {}, ['token2'])
state31 = State(31, True, {}, ['qq_mail_address'])
states = [state0, state1, state2, state3, state4, state5, state6, state7, state8, state9, state10, state11, state12, state13, state14, state15, state16, state17, state18, state19, state20, state21, state22, state23, state24, state25, state26, state27, state28, state29, state30, state31]
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