# -*- coding: cp1252 -*-
import xml.etree.ElementTree as ET
import lxml.etree as etree
import time

BASE_URI = 'http://datos.uchile.cl/'

dic = {
    'xmlns:owl': BASE_URI + 'ontologia/',
    'xmlns:foaf': 'http://xmlns.com/foaf/0.1/',
    'xmlns:bio': 'http://vocab.org/bio/0.1/',
    'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
}

output = {
    'person_root' : ET.Element( 'rdf:RDF', dic ), #Base element for authorities
    'year_root' : ET.Element( 'rdf:RDF', dic ) #Years
}


birthYearDict = {}; deathYearDict = {}
i = 0
for event, elem in ET.iterparse( 'input/autoridades-big.xml', events=( 'start', 'end', 'start-ns', 'end-ns' ) ):
    if event != 'start' or elem.tag != 'authority': continue
    authority = elem
    authIDElement = authority.find('authorityID')

    if authIDElement == None or authIDElement.text == None: continue
    authID = authIDElement.text

    personElement = ET.SubElement( output['person_root'], 'owl:NamedIndividual', {'rdf:about': BASE_URI + 'autoridad/' + authID} )

    nameElement = authority.find( ".//*[@tag='100']" )
    if nameElement == None or nameElement.text == None: continue
    
    marcEntryTextArray = nameElement.text.split('|')
    if len(marcEntryTextArray) == 1: continue

    for entry in marcEntryTextArray:
        if entry == '': continue

        # caso nombre
        if entry[0] == 'a':
            # arreglo apellido - nombre
            nameArray = entry[1:].split(',')

            # arreglo nombre - apellido
            nameArray = nameArray[::-1]

            # quitar espacios sobrantes por elemento
            nameArray = map(lambda e : e.strip() ,nameArray)

            # quitar elementos vacios del arreglo
            nameArray = filter(lambda e : e != '', nameArray)

            # crear elemento persona
            nameElement = ET.SubElement(personElement, 'foaf:name')
            nameElement.text = ' '.join(nameArray)

        # caso fechas
        if entry[0] == 'd':

            # arreglo de fechas nacimiento - muerte
            yearTextArray = entry[1:].split('-')

            # ver si la fecha es parseable
            # Sacar puntos, comas, espacios sobrantes
            # TODO: anhadir casos n. 1234 es nacimiento
            # TODO: anhadir casos m. 1234 es muerte
            # TODO: ver caso de fechas con 3 numeros
            for yearIndex in range(len(yearTextArray)):
                try:
                    time.strptime(yearTextArray[yearIndex].strip().strip(',').strip('.'), "%Y").tm_year
                    # fecha valida
                    yearTextArray[yearIndex] = yearTextArray[yearIndex].strip().strip(',').strip('.')
                except ValueError:
                    # fecha invalida
                    yearTextArray[yearIndex] = ''

            if yearTextArray[0] != '' and yearTextArray[0] not in birthYearDict:
                # crear elemento anho nacimiento en personas
                birthEventUri = BASE_URI + 'nacimiento/' + yearTextArray[0]
                ET.SubElement(personElement, 'bio:event', {'rdf:resource': birthEventUri})

                # crear elemento anho nacimiento en fechas
                yearElement = ET.SubElement(output['year_root'], 'owl:NamedIndividual', {'rdf:about': birthEventUri})
                ET.SubElement(yearElement, 'rdf:type', {'rdf:resource': 'http://purl.org/vocab/bio/0.1/Birth'})
                ET.SubElement(yearElement, 'bio:date').text = yearTextArray[0]

                # agregar al diccionario
                birthYearDict[yearTextArray[0]] = ''

            if len(yearTextArray) > 1:
                if yearTextArray[1] != '' and yearTextArray[1] not in deathYearDict:
                    # crear elemento anho muerte en personas
                    deathEventUri = BASE_URI + 'muerte/' + yearTextArray[1]
                    ET.SubElement(personElement, 'bio:event', {'rdf:resource': deathEventUri})

                    # crear elemento anho muerte en fechas
                    yearElement = ET.SubElement(output['year_root'], 'owl:NamedIndividual', {'rdf:about': deathEventUri})
                    ET.SubElement(yearElement, 'rdf:type', {'rdf:resource': 'http://purl.org/vocab/bio/0.1/Death'})
                    ET.SubElement(yearElement, 'bio:date').text = yearTextArray[1]

                    # agregar al diccionario
                    deathYearDict[yearTextArray[1]] = ''
    elem.clear();
    i += 1
    #if i > 100: break

print i
ET.ElementTree( output['person_root'] ).write( 'output/personas.rdf', 'utf-8' )
ET.ElementTree( output['year_root'] ).write( 'output/fechas.rdf', 'utf-8' )
with open( 'output/personas.rdf', 'r' ) as ini, open( 'output/personas_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True ) )
with open( 'output/fechas.rdf', 'r' ) as ini, open( 'output/fechas_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True ) )
