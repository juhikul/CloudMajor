#!/bin/python

from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

import collections

def insert(columnFamily, key, values) :
        "insert values in a given column family"
        column = ColumnFamily(pool, columnFamily)
        column.insert(key,values)


def get(columnFamily, key) :
        "select values in a given column family"
        try :
		column = ColumnFamily(pool, columnFamily)
        	return column.get(key)
	except:
		return {'status':0}

def get_reverse(columnFamily, key) :
        "select values in a given column family"
        try :
	        column = ColumnFamily(pool, columnFamily)
	        return column.get(key,column_reversed=True)
	except:
		return {'status':0}

def multi_get(columnFamily, key) :
        "select values in a given column family"
        column = ColumnFamily(pool, columnFamily)
	d = {}
	for k in key :
		print k		
		d[k] = get(columnFamily,k)
	print "MULTI GET :::" , collections.OrderedDict(d)
        return d
 
def get_range(columnFamily, uid, key1, key2) :
        "select values in a given column family"
	column = ColumnFamily(pool, columnFamily)
        result = column.get(uid,column_start=str(key1), column_finish=str(key2))
        return result

def remove_column(columnFamily, uid, columns) :
	"To remove columns from a key"
	column = ColumnFamily(pool, columnFamily)
	column.remove(uid,columns)

def remove_row(columnFamily, uid) :
	"To remove row from a column family"
	column = ColumnFamily(pool, columnFamily)
	column.remove(uid)

pool = ConnectionPool('Keyspace1')
