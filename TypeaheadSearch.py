"""
These codes are all written by myself.
                Changyun Gong
"""
"""
database is an ordered dictionary. If a new record comes, it will beappended.
When deleting, just find the unique id, then delete it.
When querying, create a result ordered dictionary, sort each time, so that the remaining can be the most valuable and latest.
When wquerying, similar as querying. The difference is the weight.
"""
#!usr/bin/env python

import string
from collections import OrderedDict
import sys


NRANGE = range(0, 100000)
ADDRANGE = range(0, 40000)
DELRANGE = range(0, 10000)
QUERYRANGE = range(0, 20000)
WQUERYRANGE = range(0, 1000)
BOOSTRANGE = range(0, 25)
SCORERANGE =[x*0.1 for x in range(0,1000)]
DATASTRINGLENGTHRANGE = range(0, 100)

OPERATIONS = ('ADD', 'DEL', 'QUERY', 'WQUERY')
TYPES = ('USER', 'TOPIC', 'QUESTION', 'BOARD')

database = OrderedDict()

def operationAdd(comdata):
    """
    do the add operation
    input: one command
    return: success or fail
    """
    items = comdata.split(' ',3)
    m_type = items[0].upper()
    m_id = items[1]
    m_score = float(items[2])
    m_datastring = items[3]
    if m_type not in TYPES:
        print 'error type'
        return False
    if m_id in database.keys():
        print 'the id has been existed'
        return False
    if m_score not in SCORERANGE:
        print 'error score range'
        return False
    if len(m_datastring) not in DATASTRINGLENGTHRANGE:
        print 'error: the string length'
        return False
    database[m_id] = {'type':m_type, 'score': m_score, 'data':m_datastring}
    return True

def operationDEL(comdata):
    """
    do the del operation
    input: id
    return: success or fail
    """
    key = comdata.split(' ')
    key = key[0]
    if key in database.keys():
        del database[key]
        return True
    return False

def operationQuery(comdata):
    """
    do the query operation
    input: some words
    output: a list of records
    """
    splits = comdata.split(' ',1)
    number = int(float(splits[0]))
    if number == 0:
        return {}
    strings = splits[1].split(' ')
    if number>20:
        number = 20
    result = OrderedDict()
    flag = True
    for key in database.keys():
        for string in strings:
            if database[key]['data'].upper().find(string.upper()) == -1:
                flag = False
                break
        if flag == True:
            k = result.keys()
            k = sorted(k, key = result.__getitem__)
            if len(k) >= number:
                if database[k[0]]['score'] > database[key]['score']:
                    flag = True
                    continue
                del result[k[0]]
                result[key] = database[key]['score']
            else:
                result[key] = database[key]['score']
        flag = True
        continue
    return result

def operationWquery(comdata):
    """
    do the query operation
    input: some words and optiinal things
    output: a list of records
    """
    result = OrderedDict()
    items = comdata.split(' ',2)
    number_of_results = int(float(items[0]))
    number_of_boosts = int(float(items[1]))
    items = items[2].split(' ', number_of_boosts)
    boostsDic = {}
    for i in range(number_of_boosts):
        boost = items[i].split(':')
        if boost[0].upper() in TYPES:
            boostsDic[boost[0].upper()] = int(float(boost[1])*10)*0.1
        else:
            boostsDic[boost[0]] = int(float(boost[1])*10)*0.1
    strings = items[number_of_boosts].split(' ')
    flag = True
    for key in database.keys():
        m_score = database[key]['score']
        for string in strings:
            if database[key]['data'].upper().find(string.upper()) == -1:
                flag = False
                break
        if flag == True:
            k = result.keys()
            k = sorted(k, key = result.__getitem__)
            boosts = boostsDic.keys()
            m_score = database[key]['score']
            m_type = database[key]['type']
            m_id  = key
            if m_id in boosts:
                m_score = int(m_score * boostsDic[m_id]*10000)*0.0001
            if m_type in boosts:
                m_score = int(m_score * boostsDic[m_type]*10000)*0.0001
            if len(k) >= number_of_results:
                if m_score < result[k[0]]:
                    flag = True
                    continue
                del result[k[0]]
                result[m_id] = m_score

            else:
                result[m_id] = m_score
        flag = True
        continue
    return result

def operationClassify(command):
    """
    analysis one command, then call different functions
    input: one command
    output: none
    """
    items = command.split(' ',1)
    items[0] = items[0].upper()    # case insentive
    if items[0] not in OPERATIONS:
        print 'operation error'
        return
    if items[0] == OPERATIONS[0]:
        boolop = operationAdd(items[1])
    if items[0] == OPERATIONS[1]:
        boolop = operationDEL(items[1])
    if items[0] == OPERATIONS[2]:
        dicop = operationQuery(items[1])
        k = dicop.keys()
        if len(k) == 0:
            print '\n'
        else:
            k = sorted(k,key = dicop.__getitem__ )
            k.reverse()
            print ''.join('%s ' %(key) for key in k)
    if items[0] == OPERATIONS[3]:
        dicop = operationWquery(items[1])
        k = dicop.keys()
        if len(k) == 0:
            print '\n'
        else:
            k = sorted(k,key = dicop.__getitem__ )
            k.reverse()
            print ''.join('%s ' %(key) for key in k)
    return

def printDatabase():
    formatString = 'type:%s id:%s score:%f  %s '
    for key in database.keys():
        print formatString % (database[key]['type'], key, database[key]['score'],database[key]['data'])

def readFromFile(path):
    """
    read from file
    input: path
    output:fail or success
    """
    try:
        file_open = open(path, 'r')
    except:
        print 'Error: invalid path'
        return
    all_buffer = file_open.readlines()
    file_open.close()
    for line in all_buffer:
        if line[-1] == '\n':
            line = line[:-1]
        operationClassify(line)
    # printDatabase()
        # printDatabase()
        # print ""

if __name__ == '__main__':
        times = int(raw_input())
        for i in range(times):
            text = raw_input()
            operationClassify(text)
    # readFromFile('a.txt')


