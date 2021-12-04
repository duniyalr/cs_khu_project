import sqlite3
import whereConditions as wc
import functools

PATH_TO_DATABASE_FILE = "./db_files/db"

try:
    con = sqlite3.connect(PATH_TO_DATABASE_FILE)
except Exception as e:
    print('connection to database can not established.')
    print(e)
    exit()

cur = con.cursor()
print('database connected')

# checking the tables
table_names = ['users']

# tables that are not exists should recreate
tables_to_make = []
for table_name in table_names:
    cur.execute(f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
    ''')
    res = cur.fetchall()
    if not res:
        tables_to_make.append(table_name)

# creating tables
tables_sql = {
    "users" : 
        [
            '''
                CREATE TABLE users (
                    username text unique,
                    password text
                );
            ''',
            '''
                CREATE INDEX usernameI ON users (username);
            '''
        ]
}
for table_name in tables_to_make:
    for stm in tables_sql[table_name]:
        cur.execute(stm)

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
# primary functions for creating driver api
# table_name(str), columns(list), values(list) -> if success 1 else 0
def insert(
    table_name,
    columns,
    values
):
    if (type(table_name) is not str):
        raise TypeError('table_name should be string')
    if (type(columns) is not list):
        raise TypeError('columns should be list')
    if (type(values) is not list):
        raise TypeError('values should be list')
    
    PART1 = f'INSERT INTO {table_name} '
    PART2 = columnNamesToString(columns) + ' '
    PART3 = 'VALUES ' + valuesToString(values)
    SQL = PART1 + PART2 + PART3
    
    cur.execute(SQL)
    con.commit()

# table_name(str), columns(list), where(dict?) -> (list)
def select(
    table_name,
    columns,
    where
):
    if (type(table_name) is not str):
        raise TypeError('table_name should be string')
    if (type(columns) is not list):
        raise TypeError('columns should be list')
    if (type(where) is not dict and type(where) is not list):
        raise TypeError('where should be dict')
    
    PART1 = 'SELECT ' + columnNamesToString(columns, False) + ' '
    PART2 = f'FROM {table_name} ' 
    PART3 = 'WHERE ' + whereToString(where)
    SQL = PART1 + PART2 + PART3
    
    print(SQL)
    cur.execute(SQL)
    res = cur.fetchall()

    return res

def delete(
    table_name,
    where
):
    if (type(table_name) is not str):
        raise TypeError('table_name should be string')
    if (type(where) is not dict and type(where) is not list):
        raise TypeError('where should be dict')

    PART1 = f'DELETE FROM {table_name} '
    PART2 = 'WHERE ' + whereToString(where)

    SQL = PART1 + PART2
    cur.execute(SQL)
    con.commit()

def update(
    table_name,
    columns,
    values,
    where
):
    if (type(table_name) is not str):
        raise TypeError('table_name should be string')
    if (type(columns) is not list):
        raise TypeError('columns should be list')
    if (type(values) is not list):
        raise TypeError('values should be list')
    if (type(where) is not dict and type(where) is not list):
        raise TypeError('where should be dict')
    
    PART1 = f'UPDATE {table_name} '
    PART2 = f'SET {toSetExpression(columns, values)} '
    PART3 = f'WHERE {whereToString(where)}'
    SQL = PART1 + PART2 + PART3
    print(SQL)
    cur.execute(SQL)
    con.commit()

# delete('users', [wc.equal('username', 'duniyal')])
# insert('users', ['username', 'password'], ['fbdsafsdgs', '1gfdsgsd234'])
# update('users', ['username'], ['omidjadidffdsafdaf'],[wc.equal('username', 'omidjadidfg')])
# print(select('users',[], []))