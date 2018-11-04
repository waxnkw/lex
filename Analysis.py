class State(object):
    def __init__(self, id, is_end_state, edges, token):
        self.id = id
        self.is_end_state = is_end_state
        self.edges = edges
        self.token = token


state0 = State(0, True, {'a': 1, 'b': 2, 'c': 3}, ['t3'])
state1 = State(1, True, {'a': 4, 'b': 5}, ['t3'])
state2 = State(2, True, {}, ['t3'])
state3 = State(3, True, {}, ['t2'])
state4 = State(4, True, {'a': 4}, ['t3'])
state5 = State(5, True, {'c': 6}, ['t2'])
state6 = State(6, True, {}, ['t1'])
states = [state0, state1, state2, state3, state4, state5, state6]


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
            else:
                ret.append(cur.token[0])
    return ret


def lex_output(tokens, path):
    s = ''
    for token in tokens:
        s += str(token)+"  "
    s += '\n'
    with open(path, 'w+') as f:
        f.write(s)
        f.flush()


if __name__ == '__main__':
    import sys
    # input_path = sys.argv[1]
    # output_path = sys.argv[2]
    input_path = "testInputWords.txt"
    output_path = "testOutTokens.txt"
    in_text = get_input(input_path)
    tokens = analysis(in_text)
    if tokens is None:
        quit()
    lex_output(tokens, output_path)