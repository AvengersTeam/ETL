import sys
file_names = open('output/personas_temp.rdf','r')
file_fechas = open('output/fechas_temp.rdf','r')
file_corp = open('output/corporativos_temp.rdf','r')
file_corp2 = open('output/corporativos_temp2.rdf','w')
file_corp_output = open('output/corporativos.rdf','w')
file_names_output = open('output/personas_temp2.rdf','w')
file_fechas_output = open('output/fechas_temp2.rdf','w')
file_names_output2 = open('output/personas.rdf','w')
file_fechas_output2 = open('output/fechas_temp3.rdf','w')
#colocar enters
#caso autoridades
for linea in file_names:
        indice_act = 0
        aux = 0
        while 0 < len(linea):
                try:
                        indice_act = linea.index('><')                        
                except ValueError:
                        sublinea = linea[:aux+1]
                        file_names_output.write(sublinea)
                        linea = linea[aux+1:]
                aux = indice_act
                sublinea = linea[:indice_act+1]
                file_names_output.write(sublinea+'\n')
                linea = linea[indice_act+1:]
file_names_output.flush()
#caso fechas
for linea in file_fechas:
        indice_act2 = 0
        while 0 < len(linea):
                try:
                        indice_act2 = linea.index('><')
                except ValueError:
                        aux = 0
                sublinea = linea[:indice_act2+1]
                file_fechas_output.write(sublinea+'\n')
                linea = linea[indice_act2+1:]
file_fechas_output.flush()
#caso corporativos
for linea in file_corp:
        indice_act = 0
        aux = 0
        while 0 < len(linea):
                try:
                        indice_act = linea.index('><')                        
                except ValueError:
                        sublinea = linea[:aux+1]
                        #print sublinea
                        file_corp2.write(sublinea)
                        linea = linea[aux+1:]
                aux = indice_act
                sublinea = linea[:indice_act+1]
                #print sublinea
                file_corp2.write(sublinea+'\n')
                linea = linea[indice_act+1:]
file_corp2.flush()
#colocar tabs
#caso autoridades
file_names_output = open('output/personas_temp2.rdf','r')
count = 0
for linea in file_names_output:
        indice = linea.find('</owl')
        if indice != -1:
                count = count - 1
        indice = linea.find('</rdf')
        if indice != -1:
                count = count - 1
        if count == 0:
                file_names_output2.write(linea)
        elif count == 1:
                file_names_output2.write('\t'+linea)
        elif count == 2:
                file_names_output2.write('\t\t'+linea)
        else:
                file_names_output2.write('\t\t'+linea)
        indice = linea.find('<rdf')
        if indice != -1:
                count = count + 1        
        indice = linea.find('<owl')
        indice2 = linea.find('/>')
        if indice != -1 and indice2 == -1:
                count = count + 1        
file_names_output2.flush()
#caso corporativos
file_corp2 = open('output/corporativos_temp2.rdf','r')
count = 0
for linea in file_corp2:
        indice = linea.find('</owl')
        if indice != -1:
                count = count - 1
        indice = linea.find('</rdf')
        if indice != -1:
                count = count - 1
        if count == 0:
                file_corp_output.write(linea)
        elif count == 1:
                file_corp_output.write('\t'+linea)
        elif count == 2:
                file_corp_output.write('\t\t'+linea)
        else:
                file_corp_output.write('\t\t'+linea)
        indice = linea.find('<rdf')
        if indice != -1:
                count = count + 1        
        indice = linea.find('<owl')
        indice2 = linea.find('/>')
        if indice != -1 and indice2 == -1:
                count = count + 1        
file_corp_output.flush()
#caso fechas
file_fechas_output = open('output/fechas_temp2.rdf','r')
count = 0
for linea in file_fechas_output:
        indice = linea.find('</rdf')
        if indice != -1:
                count = count - 1
        if count == 0:
                file_fechas_output2.write(linea)
        elif count == 1:
                file_fechas_output2.write('\t'+linea)
        else:
                file_fechas_output2.write('\t\t'+linea)
        indice = linea.find('<rdf')
        if indice != -1:
                count = count + 1       
file_fechas_output2.flush()
print 'RDFs ordenados e identados.'
