general_ops = ['.', '*', '|', '(', ')']
normal_ops = ['.', '*', '|']
ops_rule = {
    '.': 3,
    '*': 2,
    '|': 1,
}


def is_op(c):
    return c in normal_ops


def preprocess(token_regs):
    """
    预处理到后缀表达式
    :param token_regs:
    :return: {(token: reg(suffix))}
    """
    ret = {key: prefix_to_suffix(add_points(reg)) for (key, reg) in token_regs.items()}
    return ret


def add_points(reg):
    """
    给reg加 '.'
    :param reg: reg without '.'
    :return: reg with '.'
    """
    ret = ''

    # 如果reg只有一个字符返回
    if len(reg) == 0:
        return reg

    for i in range(len(reg)):
        c = reg[i]
        next_c = reg[i + 1] if i + 1 < len(reg) else None

        ret += c
        if i == len(reg)-1:
            break

        if (next_c not in general_ops and c not in general_ops) \
            or (c not in general_ops and next_c == '(') \
            or (c == ')' and next_c not in general_ops):
            ret += '.'

    return ret


def prefix_to_suffix(reg):
    expression = ''
    ops = []
    for item in reg:
        if item in normal_ops:
            while len(ops) >= 0:
                if len(ops) == 0:
                    ops.append(item)
                    break
                op = ops.pop()
                if op == '(' or ops_rule[item] > ops_rule[op]:
                    ops.append(op)
                    ops.append(item)
                    break
                else:
                    expression += op
        elif item == '(':
            ops.append(item)
        elif item == ')':
            while len(ops) > 0:
                op = ops.pop()
                if op == '(':
                    break
                else:
                    expression += op
        else:
            expression += item

    while len(ops) > 0:
        expression += ops.pop()

    return expression