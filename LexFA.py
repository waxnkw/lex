from LexPreprocess import is_op
import networkx as nx
from pylab import show

Epsilon = 'epsilon'


def merge_two_list(l1, l2):
    for x in l2:
        if x not in l1:
            l1.append(x)
    return l1


class State(object):
    cnt = 0

    def __init__(self, is_end_state):
        # 更新编号
        self.id = State.cnt
        State.cnt += 1

        # 是否为结束状态
        self.is_end_state = is_end_state
        self.edges = {}

        self.token = None

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return self.__str__()

    def add_edge(self, state, edge):
        if edge not in self.edges:
            self.edges[edge] = []
        self.edges[edge].append(state)
        # print(self.edges)

    def to_output_file(self):
        s = 'state'+str(self.id)+' = '+'State('
        s += str(self.id)+", "
        s += str(self.is_end_state)+", "
        s += str(self.edges)+", "
        s += str(self.token) + ")"
        return s


def construct_single_char(c):
    """
    构建单个字符的自动机
    eg: s1---a-->s2
    :param c: single char
    :return: 改自动机
    """
    s1 = State(False)
    s2 = State(False)
    s1.add_edge(s2, c)

    am = Automaton()
    am.states.append(s1)
    am.states.append(s2)
    am.start_state = s1
    am.end_state = s2
    return am


class Automaton(object):
    """
    自动机
    """

    def __init__(self):
        self.states = []
        self.start_state = None
        self.end_state = None

    def show(self):
        for state in self.states:
            if state.is_end_state:
                print(state.id, state.edges, state.token)
            else:
                print(state.id, state.edges)
        print("start_state: ", self.start_state.id)

    def show_graph(self):
        G = nx.DiGraph()
        pos = {}
        for state in self.states:
            G.add_node(state.id)
            pos[state.id] = (state.id, state.id)
        labels = {}
        for state in self.states:
            for key, val in state.edges.items():
                for tar_state in val:
                    G.add_edge(state.id, tar_state.id)
                    labels[(state.id, tar_state.id)] = key
        pos = nx.spring_layout(G)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx(G, pos)
        show()

    def head_add(self, to_add_state, edge):
        """
        在开始状态之前增加状态
        :param to_add_state: 需要增加的state
        :param edge: 需要增加的边
        :return:
        """
        to_add_state.add_edge(self.start_state, edge)
        self.start_state = to_add_state
        if to_add_state not in self.states:
            self.states.append(to_add_state)

    def end_add(self, to_add_state, edge):
        """
        在结束状态之后增加状态
        :param to_add_state: 需要增加的state
        :param edge: 需要增加的边
        :return:
        """
        self.end_state.add_edge(to_add_state, edge)
        self.end_state = to_add_state
        if to_add_state not in self.states:
            self.states.append(to_add_state)

    def extend(self, a, edge):
        self.end_state.add_edge(a.start_state, edge)
        self.end_state = a.end_state
        self.states.extend(a.states)
        # self.states = [set(self.states)]

    def sort_states(self):
        """
        将自身的state按照id asc排序
        :return:
        """
        self.states = sorted(self.states, key=lambda state: state.id)

    def find_end_states(self):
        """
        查找所有终止状态
        :return: 终止状态
        """
        ret = []
        for state in self.states:
            if state.is_end_state:
                ret.append(state)
        return ret

class Table(object):
    """
    table dfa状态转移表
    """
    def __init__(self, rows, cols, elements):
        self.rows = rows
        self.cols = cols
        self.elements = elements

    def add_row(self, row):
        self.rows.append(row)

    def show(self):
        s = "       "
        for col in self.cols:
            s += str(col) + "   "
        print(s)
        for row, i in zip(self.rows, range(len(self.rows))):
            s = str(row)+":  "
            x = self.elements[i]
            for j in range(len(self.cols)):
                s += str(x[j])+"   "
            print(s)

    def show_simple(self):
        s = "       "
        for col in self.cols:
            s += str(col) + "   "
        print(s)
        for row, i in zip(self.rows, range(len(self.rows))):
            s = str(self.rows.index(row)) + ":  "
            x = self.elements[i]
            for j in range(len(self.cols)):
                s += str(self.rows.index(x[j]) if x[j] is not None else None) + "   "
            print(s)

    def get(self, state_id, edge):
        i = self.rows.index(state_id)
        j = self.cols.index(edge)
        return self.elements[i][j]


def concatenate_two_automatons(a1, a2):
    """
    '.'号运算,连接两个自动机
    a.b:  s1--a-->s2--epsilon-->s3---b--->s4
    :param a1: 在前的自动机
    :param a2: 在后的自动机器
    :return:
    """
    a1.extend(a2, Epsilon)
    return a1


def or_two_automatons(a1, a2):
    """
    '|'运算两个自动机a, b
    a|b:
         / --s4------a----->s6-----\
         epsilon                    epsilon
       /                             ↘
    s1                                s2
       \                             ↗
        epsilon                     epsilon
         \----s3------>b-----s5----/
    :param a1: 第一个自动机
    :param a2: 第二个自动机
    :return:
    """
    a = Automaton()
    s1 = State(False)
    s2 = State(False)

    # 连接初始边和结束边
    s1.add_edge(a1.start_state, Epsilon)
    s1.add_edge(a2.start_state, Epsilon)
    a1.end_state.add_edge(s2, Epsilon)
    a2.end_state.add_edge(s2, Epsilon)

    # 给新自动机赋初始状态和结束状态
    a.start_state = s1
    a.end_state = s2

    # 扩展状态列表,  最后去重
    a.states.extend([s1, s2])
    a.states.extend(a1.states)
    a.states.extend(a2.states)
    # a.states = [set(a.states)]
    return a


def closure_one_automaton(a):
    """
    '*'操作, 构建自动机a的闭包
    例如:
                          /-epsilon-e3-\
                         ↙             \
        s1-e1-epsilon--->s3------a------>s4--epsilon---e4-> s2
         \                                            ↗
          \-------e2---------epsilon-----------------/
    :param a:
    :return: 构建好的闭包
    """
    s1 = State(False)
    s2 = State(False)
    # 新增 e1 e2
    s1.add_edge(s2, Epsilon)
    s1.add_edge(a.start_state, Epsilon)

    # 新增 e3 e4
    a.end_state.add_edge(s2, Epsilon)
    a.end_state.add_edge(a.start_state, Epsilon)

    # 更新初始状态
    a.start_state = s1
    a.end_state = s2

    a.states.append(s1)
    a.states.append(s2)
    # a.states = [set(a.states)]
    return a


def single_reg_to_nfa(reg):
    """
    :param reg:
    :return:
    """
    stack = []
    for c in reg:
        # is op
        if c == '.':
            a2 = stack.pop()
            a1 = stack.pop()
            a = concatenate_two_automatons(a1, a2)
            stack.append(a)
        elif c == '|':
            a2 = stack.pop()
            a1 = stack.pop()
            a = or_two_automatons(a1, a2)
            stack.append(a)
        elif c == '*':
            a = stack.pop()
            a = closure_one_automaton(a)
            stack.append(a)
        # 不是操作符
        else:
            stack.append(construct_single_char(c))
    return stack.pop()


def reg_to_nfa(token_regs):
    """
    从token和reg的序列构建各自的自动机, 并且连接到同一个初始状态
    :param token_regs:
    :return: automaton of all states
    """
    nfas = []
    for token, reg in token_regs.items():
        a = single_reg_to_nfa(reg)
        a.end_state.token = token
        a.end_state.is_end_state = True
        nfas.append(a)

    # init return automaton
    s = State(False)
    ret = Automaton()
    ret.start_state = s
    ret.states.append(s)

    for nfa in nfas:
        s.add_edge(nfa.start_state, Epsilon)
        ret.states.extend(nfa.states)

    return ret


def epsilon_closure(start):
    """
    求由状态a开始的epsilon闭包
    :param start: 起始状态
    :return: epsilon闭包中状态的id的set
    """
    stack = [start]
    ret = [start.id]
    while len(stack) > 0:
        state = stack.pop()
        to_add_states = [epsilon_state for epsilon_state in state.edges.get(Epsilon, [])]
        to_add_state_ids = [epsilon_state.id for epsilon_state in state.edges.get(Epsilon, [])]
        # 防止死循环,在ret中的不加入
        stack.extend([x for x in to_add_states if x.id not in ret])
        ret.extend(to_add_state_ids)
    return set(ret)


def collect_edges(automaton):
    """
    从一个自动机中收集所有边
    :param automaton: 目标自动机
    :return: 自动机所有边
    """
    ret = [s.edges.keys() for s in automaton.states]
    import itertools
    ret = itertools.chain.from_iterable(ret)
    ret = list(set(ret))
    if Epsilon in ret:
        ret.remove(Epsilon)
    return sorted(ret)


def states_id_through_edge(state, edge):
    """
    从当前state通过edge边到达的状态们
    :param state: type is Stare
    :param edge:
    :return:
    """
    next_states = state.edges.get(edge, [])
    ret = set([x.id for x in next_states])
    return list(ret)


def get_next_state_without_epsilon_closure(states, new_state, edge):
    """
    得到求epsilon闭包之前的新状态集合
    :param states: State的集合
    :param new_state: set(1,2,3)
    :param edge 通过的边
    :return: list[1,2,3] states id list   如果没有新状态,返回None
    """
    ret = []
    for i in new_state:
        tmp = states_id_through_edge(states[i], edge)
        ret.extend(tmp)
    return ret if len(ret) > 0 else None


def get_next_state_with_epsilon_closure(states, new_state, edge):
    """
    得到求epsilon闭包之后的新状态集合
    :param states: State的集合
    :param new_state: set(1,2,3)
    :param edge 通过的边
    :return: set(4,5,6) states id list   如果没有新状态,返回None
    """
    without_epc = get_next_state_without_epsilon_closure(states, new_state, edge)
    # 如果为空直接返回
    if without_epc is None:
        return None

    ret = []
    # 求每一个闭包,总和求此状态集合的闭包
    for state_index in without_epc:
        epc = epsilon_closure(states[state_index])
        ret.append(list(epc))
    import itertools
    return set(list(itertools.chain.from_iterable(ret)))


def nfa_to_dfa(nfa, edges):
    # 排序状态,并取出
    nfa.sort_states()
    states = nfa.states

    start = nfa.start_state
    new_states = [epsilon_closure(start)]
    new_state_table = []
    # last_len_of_new_state = len(new_state_table)

    cur_index = 0
    # 构建dfa
    while cur_index < len(new_states):
        cur_state = new_states[cur_index]

        table_row = []
        for edge in edges:
            table_ele = get_next_state_with_epsilon_closure(states, cur_state, edge)

            # 如果是新的状态,填入需要探索的新状态
            if table_ele is not None \
                and table_ele not in new_states:
                new_states.append(table_ele)

            table_row.append(table_ele)

        # 表中填入一整行
        new_state_table.append(table_row)

        # 新增当前index
        cur_index += 1
    return Table(rows=new_states, cols=edges, elements=new_state_table)


def convert_table_to_dfa(table, automaton):
    """
    将dfa转状态转换表转换为automaton
    :param table: dfa状态转换表
    :param automaton: 简化前的nfa
    :return: 转化后的dfa
    """
    end_states = automaton.find_end_states()
    end_states_ids = [x.id for x in end_states]

    raw_dfa_states = table.rows
    edge_vals = table.cols

    dfa_states = [State(False) for i in range(len(raw_dfa_states))]

    for i, state in zip(range(len(dfa_states)), dfa_states):
        state.id = i

        # 判断是否是终止状态
        for possible_state_id in raw_dfa_states[i]:
            # TODO 判断优先级 if 之类的
            # 现在默认写在前面的优先级更高
            if possible_state_id in end_states_ids:
                index = end_states_ids.index(possible_state_id)
                state.is_end_state = True
                if state.token is None:
                    state.token = []
                state.token.append(end_states[index].token)

        # 构造每一个state的边
        edges = table.elements[i]
        state.edges = {edge_val: dfa_states[raw_dfa_states.index(tar_state)]
                       for edge_val, tar_state in zip(edge_vals, edges) if tar_state is not None}

    ret = Automaton()
    ret.states = dfa_states
    ret.start_state = dfa_states[0]
    return ret


def get_group_id(state_id, groups):
    """
    得到state_id对应的state所属的group
    :param state_id: 目标state_id
    :param groups: 当前groups
    :return: state所对应的group编号
    """
    for i, group in zip(range(len(groups)), groups):
        if state_id in group:
            return i


def classes_through_edges(cur_state_id, states, groups, edges, cnt=[0]):
    ret = []
    for edge in edges:
        cur_state = states[cur_state_id]
        next_state = cur_state.edges.get(edge, None)
        if next_state is None:
            ret.append(None)
        else:
            ret.append(get_group_id(next_state.id, groups))
        # 全是None的不能合并
        if ret == [None for i in range(len(edges))]:
            ret.append(cnt[0])
            cnt[0] += 1

    return ret


def divide(cur_group, groups, states, edges):
    """
    将当下group按照现有的规则分割成多个group
    :param cur_group: 待分割group
    :param groups: 当前所有groups
    :param states: 当前所有states, 用来提供规则支持
    :param edges: 所有边
    :return:
    """
    classes_table = [classes_through_edges(cur_state_id, states, groups, edges)
                        for cur_state_id in cur_group]
    unique_classes = []
    # 去重
    for classes in classes_table:
        if classes not in unique_classes:
            unique_classes.append(classes)

    ret = [[] for i in range(len(unique_classes))]

    for classes, i in zip(classes_table, range(len(cur_group))):
        j = unique_classes.index(classes)
        ret[j].append(cur_group[i])

    return ret


def get_states_from_group(groups, states):
    ret = [State(False) for i in range(len(groups))]
    for i, state, group in zip(range(len(ret)), ret, groups):
        edges = {edge: ret[get_group_id(next_state.id, groups)]
                 for edge, next_state in states[group[0]].edges.items()}
        state.edges = edges
        state.id = i
        # 终止状态考虑 TODO 优先级
        for j in group:
            tmp = states[j]
            if tmp.is_end_state:
                state.is_end_state = True
                if state.token is None:
                    state.token = []
                state.token.extend(tmp.token)
        if state.token is not None:
            state.token = list(set(state.token))
    return ret


def dfa_minimize(dfa):
    """
    将dfa最小化
    :param dfa:
    :return:
    """
    # dfa = Automaton(dfa)

    end_states = dfa.find_end_states()
    end_states_ids = [x.id for x in end_states]
    edges = collect_edges(dfa)

    states = dfa.states
    # 初始化需分类的的list
    to_be_classified = [[x.id for x in states if x.id not in end_states_ids], end_states_ids]

    # 浅拷贝一个states用来做初步分类
    is_change = True
    while(is_change):
        is_change = False
        new_groups = []

        for group in to_be_classified:
            divided_groups = divide(group, to_be_classified, states, edges)
            new_groups.extend(divided_groups)
            if len(divided_groups)>1:
                is_change = True

        # 赋新值
        to_be_classified = new_groups

    # cons dfa
    states = get_states_from_group(to_be_classified, states)
    ret = Automaton()
    ret.states = states
    ret.start_state = states[0]
    return ret

