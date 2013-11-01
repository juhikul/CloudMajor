#!/bin/python

from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

def insert(columnFamily, key, values) :
	"insert values in a given column family"
	column = ColumnFamily(pool, columnFamily)
	column.insert(key,values)


def get(columnFamily, key) :
	"select values in a given column family"
	column = ColumnFamily(pool, columnFamily)
	return column.get(key)






pool = ConnectionPool('Keyspace1')

