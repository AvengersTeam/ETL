import sys
file_fechas_in = open('output/fechas_temp3.rdf','r')
file_fechas_out = open('output/fechas.rdf','w')
vistos = []
for linea in file_fechas_in:
	i = 0
	existe = False
	while i < len(vistos):
		if linea == vistos[i]:
			existe = True
			break
		i = i + 1
	if not existe:
		vistos.append(linea)
		file_fechas_out.write(linea)
print('Fechas unificadas.')