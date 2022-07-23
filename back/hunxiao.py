import keyword
import random
import re


def generate_random_string(length=4):
    # 生成随机字符串
    res = 'Abcd'
    while res[0].isupper() and res[1:].islower():
        res = ''.join(
            random.sample(
                'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                length))
    return res


def _add_space(c):
    return ' ' * random.randint(0, 10) + c + ' ' * random.randint(0, 10)


def process_variables(code):
    chars = r'@-=+()*&^%!<>{}[]\|?/;:,. '  # 符号

    words = []  # 所有的单词分割后
    all = []  # 所有的字符块分割后
    # 格式：[[第一行里面分割的东西], [第二行...], ...]

    now = ''  # 暂存没有分析完的单词

    # 新增一行
    all.append([])
    words.append([])
    for wd in code:
        # 逐字分析
        if wd == '\n':
            # 如果是回车，保存当前单词、清空单词缓存并创建新行
            if now:
                all[-1].append(now)
                words[-1].append(now)
                now = ''
            all.append([])
            words.append([])
        elif wd == ' ':
            # 如果是空格，忽略
            continue
        elif wd in chars:
            # 如果是符号，那么意味着上一个单词结束了，将单词添加到列表并清空单词暂存
            if now:
                all[-1].append(now)
                words[-1].append(now)
                now = ''
            # 将符号也添加到列表
            all[-1].append(wd)
        else:
            # 是合法变量字符，添加到单词暂存
            now += wd

    variables = []  # 可能是变量的字符
    not_variables = keyword.kwlist  # 绝对不是变量的字符
    for line in range(len(all)):
        # 逐行分析
        for index in range(len(all[line])):
            # 逐词分析
            if any([
                    # 已经筛出的非变量格式
                    all[line][index] not in words[line],
                    # 空
                    not all[line][index] or all[line][index].isspace(),
                    # 已经识别的非变量
                    all[line][index] in not_variables,
                    # Python关键字
                    keyword.iskeyword(all[line][index]),
            ]):
                # 忽略
                ...
            elif any([
                    # ICode场景特判：大写变量不混淆
                    all[line][index][0].isupper(),
                    # 以数字开头不可能是变量
                    all[line][index][0].isdigit(),
                    # 保险措施：再次对类的属性和方法以及函数进行特判
                    index > 0 and all[line][index - 1] in ['.', 'def'],
                    len(all[line]) > index + 1 and all[line][index + 1] == '('
            ]):
                # 添加到非变量列表
                not_variables.append(all[line][index])
            else:
                # 可能是变量
                variables.append(all[line][index])

    # 去重
    variables = list(set(variables))
    # 再次剔除不可能是变量的字符
    for name in variables:
        if name in not_variables:
            variables.remove(name)

    used_variables = variables + ['']  # 已使用的变量名，防重复
    res = code  # 返回值

    for i in variables:
        new_name = ''
        while new_name in used_variables:
            new_name = generate_random_string()
        res = re.sub(r'(\b)' + i + r'(\b)', new_name, res)

    return res


def add_space(code):
    chars = [
        '+', '-', '*', '/', '%', '=', '>', '<', '&', '|', '^', '!', '~', '?',
        '==', '!=', '>=', '<=', '&&', '||', '<<', '>>', '>>>', '+=', '-=',
        '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '>>>=', ';', ':',
        ',', '{', '}', '[', ']', '(', ')'
    ]
    # chars = ['=', '+']
    for i in chars:
        if any([j in '*.?+$^[](){}|\\/' for j in i]):
            continue
        t = ''
        while t in code:
            t = generate_random_string()
        code = re.sub(r'(\b| )' + i + r'(\b| )', t, code)
        code = code.replace(t, _add_space(i))
    return code


def hunxiao(code):
    code = process_variables(code)
    code = add_space(code)
    return code


if __name__ == '__main__':
    print(
        hunxiao('''#  找出Dev的行走规律，将for语句内部的代码补充完整

a = 1
for i in range(8):
    Dev.step(a)
    Dev.turnRight()
    a += 1'''))
