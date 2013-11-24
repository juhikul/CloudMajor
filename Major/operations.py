#!/bin/python

from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

import collections

def insert(columnFamily, key, values) :
	"insert values in a given column family"	
	column = ColumnFamily(pool, columnFamily)
	print key,values
	column.insert(key,values)
	print key,values


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
#		print k		
		d[k] = get(columnFamily,k)
#	print "MULTI GET :::" , collections.OrderedDict(d)
        return d
 
def get_all(columnFamily) :
        "select values in a given column family"
	column = ColumnFamily(pool, columnFamily)
        result = column.get_range()
	return result

def remove_column(columnFamily, uid, columns) :
	"To remove columns from a key"
	try:
		column = ColumnFamily(pool, columnFamily)
		column.remove(uid,columns)
	except:
		return {'status':0}

def remove_row(columnFamily, uid) :
	"To remove row from a column family"
	column = ColumnFamily(pool, columnFamily)
	column.remove(uid)

def get_count(columnFamily, uid): 
	"get number of columns in a row" 
	column = ColumnFamily(pool, columnFamily) 
	count = column.get_count(uid) 
	print uid, count 
	return count

pool = ConnectionPool('Keyspace1')
