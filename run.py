import os
import sys
from prettifier import prettify

print 'Autoridades:'

try:
    execfile('etl_autoridades.py')
except Exception:
	raise Exception('Error ETL-autoridades')

print 'Listo!'
print 'Obras:'

try:
    execfile('etl_obras.py')
except Exception:
	raise Exception('Error ETL-obras')

print 'Listo!'
print 'Corporativo:'

try:
    execfile('etl_corporativo.py')
except Exception:
	raise Exception('Error ETL-corporativo')

print 'Listo!'
print 'Todo Listo!'
