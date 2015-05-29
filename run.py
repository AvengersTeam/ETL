import os
import sys
from prettifier import prettify

try:
    execfile('etl-autoridades.py')
except Exception:
	raise Exception('Error ETL-autoridades')

try:
    execfile('etl-obras.py')
except Exception:
	raise Exception('Error ETL-obras')

try:
    execfile('etl-corporativo.py')
except Exception:
	raise Exception('Error ETL-corporativo')

print('Listo!')

