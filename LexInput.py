
def lex_input(ipath):
    """
    :param ipath: 输入文件路径
    :return: {(token: regular expression), }
    """
    ret = {}
    with open(ipath, 'r') as f:
        for line in f.readlines():
            # 空串不处理
            if line.strip() == '':
                continue

            strs = line.strip().split(" ")
            ret[strs[0]] = strs[1]
    return ret