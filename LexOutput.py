from LexFA import *

pre_code = "class State(object):\n"
pre_code += "    def __init__(self, id, is_end_state, edges, token):\n"
pre_code += "        self.id = id\n"
pre_code += "        self.is_end_state = is_end_state\n"
pre_code += "        self.edges = edges\n"
pre_code += "        self.token = token\n"

after_code = '''def get_input(path):
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
    s += "\\n"
    with open(path, 'w+') as f:
        f.write(s)
        f.flush()


if __name__ == '__main__':
    import sys
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    # input_path = "testInputWords.txt"
    # output_path = "testOutTokens.txt"
    in_text = get_input(input_path)
    tokens = analysis(in_text)
    if tokens is None:
        quit()
    lex_output(tokens, output_path)'''


def my_out_put(path, dfa):
    s = pre_code

    states = [t.to_output_file() for t in dfa.states]
    for state in states:
        s += state+"\n"
    s += "states = ["
    for i in range(len(dfa.states)):
        s += "state"+str(i)
        if i != len(dfa.states)-1:
            s += ", "
    s += "]\n"

    s += after_code
    with open(path, 'w+') as f:
        f.write(s)
        f.flush()
        print('complete')