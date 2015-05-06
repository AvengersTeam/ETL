import os
import sys
from prettifier import prettify

if len(sys.argv) == 1:
    execfile('etl.py')
if len(sys.argv) == 2 and (sys.argv[1] == '-p' or sys.argv[1] == '--pretty'):
    execfile('etl.py')
    prettify('output/personas.rdf')
    prettify('output/fechas.rdf')
    os.remove('output/personas.rdf')
    os.remove('output/fechas.rdf')
else:
    raise Exception
print('Listo!')

