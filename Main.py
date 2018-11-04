from LexInput import *
from LexPreprocess import preprocess
from LexFA import *

INPUT_PATH = "input.txt"


def test_preprocess():
    s = {'t1': 'abc', 't2': 'ab|c', 't3': 'b|a*'}
    s = preprocess(s)
    print(s)


def test_re_to_nfa():
    s1 = construct_single_char('a')
    s2 = construct_single_char('b')
    s3 = concatenate_two_automatons(s1, s2)
    s3 = closure_one_automaton(s3)
    s3.show()
    print(s3.start_state)
    print(s3.end_state)


def test_regs_to_nfa():
    s = {'t1': 'abc', 't2': 'ab|c', 't3': 'b|a*'}
    s = preprocess(s)
    print(s)
    a = reg_to_nfa(s)
    print('--------------')
    # a.sort_states()
    a.show()
    print(collect_edges(a))
    # a.show_graph()


def test_epsilon_closure():
    s = {'t1': 'abc', 't2': 'ab|c', 't3': 'b|a*'}
    s = preprocess(s)
    print(s)
    a = reg_to_nfa(s)
    print('--------------')
    a.sort_states()
    # a.show()
    # a.show_graph()
    x = epsilon_closure(a.states[22])
    print(x)


def test_get_next_without_closure():
    s = {'t1': 'abc', 't2': 'ab|c', 't3': 'b|a*'}
    s = preprocess(s)
    a = reg_to_nfa(s)
    a.sort_states()
    x = epsilon_closure(a.states[1])
    print(x)
    t = get_next_state_without_epsilon_closure(a.states, x, 'b')
    print(t)
    t = get_next_state_with_epsilon_closure(a.states, x, 'b')
    print(t)


def test_nfa_to_dfa():
    s = {'t1': 'abc', 't2': 'ab|c', 't3': 'b|a*'}
    s = preprocess(s)
    a = reg_to_nfa(s)
    a.sort_states()
    edges = collect_edges(a)
    edges = sorted(edges)
    print(edges)
    s = nfa_to_dfa(a, edges)
    # s.show()
    s.show_simple()


def test_table_to_dfa():
    s = {'t1': 'abc', 't2': 'ab|c', 't3': 'b|a*'}
    s = preprocess(s)
    a = reg_to_nfa(s)
    a.sort_states()
    # a.show()
    edges = collect_edges(a)
    edges = sorted(edges)
    table = nfa_to_dfa(a, edges)
    dfa = convert_table_to_dfa(table, a)
    dfa.show()


def test_minimize_dfa():
    # x = get_group_id(4, [[1,2,3],[4,5,6],[77]])
    # print(x)
    s = {'t1': 'abc', 't2': 'ab|c', 't3': 'b|a*'}
    # s = {'t1': 'ab', 't2': 'abc'}
    s = preprocess(s)
    a = reg_to_nfa(s)
    a.sort_states()
    edges = collect_edges(a)
    # edges = sorted(edges)
    table = nfa_to_dfa(a, edges)
    dfa = convert_table_to_dfa(table, a)
    # x = classes_through_edges(4, dfa.states, [[],[x.id for x in dfa.states]], edges)
    x = dfa_minimize(dfa)
    # x.show()
    print(*[t.to_output_file() for t in x.states], sep='\n')


def test_lex_output():
    s = {'t1': 'abc', 't2': 'ab|c', 't3': 'b|a*'}
    s = preprocess(s)
    a = reg_to_nfa(s)
    a.sort_states()
    edges = collect_edges(a)
    table = nfa_to_dfa(a, edges)
    dfa = convert_table_to_dfa(table, a)
    x = dfa_minimize(dfa)
    print(*[t.to_output_file() for t in x.states], sep='\n')
    import LexOutput
    LexOutput.my_out_put("./testPython.py", dfa)


if __name__ == '__main__':
    # test_preprocess()
    # test_re_to_nfa()
    # test_regs_to_nfa()
    # test_epsilon_closure()
    # test_get_next_without_closure()
    # test_nfa_to_dfa()
    # test_table_to_dfa()
    # test_minimize_dfa()
    test_lex_output()