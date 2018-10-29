from urllib import parse


# 解密经过加密的dataMp3内容
def dataMp3(s):
    # 得到表示行数元素的后一个下标
    num_next = s.find('h')
    # 通过字符串切片拿到表示行数的元素并转换为int类型
    rows = int(s[0:num_next])
    # 拿到真实url的长度
    str_len = len(s) - num_next
    # 长度对行数取整得到每一行至少有close个元素
    row_min = int(str_len / rows)
    # 长度对行数取余得到比close多一个元素的行数
    row_inc = str_len % rows
    # 通过切片得到表示真实url的str并将其转换成list
    url_str = list(s[num_next:])
    # 设置变量添加每次得到的单个元素
    output = ''
    # 遍历生成的list，根据规律拿出特定元素，逐次添加到变量中得到真实url
    for i in range(len(url_str)):
        # 元素对整体求余得到行数
        x = i % rows
        # 元素对整体取整得到列数
        y = i / rows
        # 声明变量表示当前元素在str中的下标
        # index = 0
        if x <= row_inc:
            # 如果当前元素在多一个元素的行中，那么它在字符串中的下标等于行数和最少元素数量加一的乘积与列数的和
            index = x * (row_min + 1) + y
        else:
            # 如果当前元素不在多一个元素的行中，那么它在字符串中的下标等于元素在多一个元素的行数和最少元素数量加一的乘积与当前行数和元素在多一个元素的行数的差与最少元素的乘积和当前列数的和
            index = row_inc * (row_min + 1) + (x - row_inc) * row_min + y
        # print(p)
        # print(output)
        output += url_str[int(index)]
    return parse.unquote(output).replace('^', '0')


s = '7h%1.3F3E59%.t2.n3315E35mtFxe83%16Epp%it27227563%2a%1%F56383Fm2%5%28_7AfiF2E5%966'

print(dataMp3(s))