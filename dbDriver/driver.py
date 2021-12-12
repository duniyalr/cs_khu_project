"""
    this module provides the basic functions for working with the database
"""

import sqlite3
from . import whereConditions as wc
import functools
import os
from .utils import *
from pathlib import Path

"""
    checking the database file. if there is no db file it will create one.
"""
IS_DATABASE_CREATED = False
DB_VERSION = "001"

if not os.path.exists(os.getcwd() + '/dbDriver/db_files') : os.mkdir(os.getcwd() + '/dbDriver/db_files')
PATH_TO_DATABASE_FILE = Path(os.getcwd() + "/dbDriver/db_files/db" + DB_VERSION)

if os.path.isfile(PATH_TO_DATABASE_FILE) : IS_DATABASE_CREATED = True

try:
    con = sqlite3.connect(PATH_TO_DATABASE_FILE)
except Exception as e:
    print('connection to database can not established.')
    print(e)
    exit()

cur = con.cursor()
print('database connected')

def createDatabase():
    f = open(Path(os.getcwd() + "/dbDriver/sql/schema.sql"), 'r')
    sql = f.read()
    con.executescript(sql)

def insertExampleRecords():
    f = open(Path(os.getcwd() + "/dbDriver/sql/exampleRecords.sql"), 'r')
    sql = f.read()
    con.executescript(sql)

if not IS_DATABASE_CREATED:
    createDatabase()
    insertExampleRecords()


"""
    insert function is the primary function for adding records to database.
    inputs:
        table_name(str) -> name of table that you want to insert to it;
        doc(dict) -> the data that you want to insert to database.
            be careful every key should be column name;
    return:
        returns True if adding was and raise an error if there was a problem.
"""
def insert(
    table_name,
    doc
):
    columns = list(doc.keys())
    values = list(doc.values())

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
    return True

"""
    select function is primary function for reading from the database.
    inputs:
        table_name(str) -> the table name that you want to read from;
        columns(list) -> which columns of the table you want to read. put an empty list
            if you want return all the columns.
        where(dict) -> this is a where dictionary that indicates which records should be 
            select. read more about where dictionary in the doc.
    return:
        returns a list that contains the records that match the where dictionary conditions.
        if not found any thing it returns a empty list.
"""
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

"""
    this is primary function function for deleting records from database.
    inputs:
        table_name(str) -> the table name that you want delete records from it;
        where(dict) -> the where dictionary that indicates which records should delete.
        read more about where dictionary in docs.
    
    return:
        returns True if action was successfull and raise an error if there was a problem.
"""
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

"""
    the primary function for updating records in database.
    inputs:
        table_name(str) -> the table name that you want update records
        doc(dict) -> indicates the new values for updating the values. the keys in this
            dictionary indicates the column name and value indicates the new value for record.
        where(dict) -> its a where dictionary that indicates which records should be updated.
            read more about where dict in docs.
    return:
        returns true if updating was successfull and raises an error if there was an problem.
"""

def update(
    table_name,
    doc,
    where
):
    columns = doc.keys()
    values = doc.values()
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
    cur.execute(SQL)
    con.commit()