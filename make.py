import os
variables= {}
#execfile("etl.py", variables)
execfile("etl2.py", variables)
execfile("ordenar.py", variables)
execfile("unificar_fechas.py", variables)
print('Removiendo archivos temporales.')
os.remove('output/personas_temp2.rdf')
os.remove('output/fechas_temp2.rdf')
os.remove('output/fechas_temp3.rdf')
os.remove('output/corporativo_temp.rdf')
os.remove('output/corporativo_temp2.rdf')
print('Listo!')
