# -*- coding: cp1252 -*-
def nameParser(name):
	# arreglo apellido - nombre
    name = name.split(',')

    #remover fechas en el nombre (formatos : "Bello, Andrés, 2000-2050")
    if len(name) == 3:
    	name = [name[0], name[1]]
    # arreglo nombre - apellido
    name = name[::-1]

    # quitar espacios sobrantes por elemento
    name = map(lambda e : e.strip() ,name)

    # quitar elementos vacios del arreglo
    name = filter(lambda e : e != '', name)

    #juntar todo
    result = ' '.join(name)

    return result