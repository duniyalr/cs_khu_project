def columnNamesToString(columns, insertParanthesis = True):
    if not columns: return '*'

    if insertParanthesis:
        return '('+','.join(columns)+')'
    return ','.join(columns)

def valuesToString(values):
    values = list(map(wc.stringer, values))
    
    return '(' + ','.join(values) + ')'

# this function turns a where dict to the string
def whereToString(where, joiner = 'AND'):
    if not where: return '1=1'
    res = ''
    if type(where) is list:
        res += ' AND '.join([str(condition) for condition in where])
    if type(where) is dict:
        for _joiner, _conditions in where.items():
            res += f'({whereToString(_conditions, _joiner)}) '
    return res

def toSetExpression(columns, values):
    columns_res = []
    for i in range(len(columns)):
        print(i, 'i is here')
        columns_res.append(f'{columns[i]}={wc.stringer(values[i])}')
    
    return ', '.join(columns_res)