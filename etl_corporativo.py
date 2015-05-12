# -*- coding: cp1252 -*-
import xml.etree.ElementTree as ET
import lxml.etree as etree
import time
import pprint #for debugg print

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def print_countries():
    for country in countries_set:
        print "C: " + country

BASE_URI = 'http://datos.uchile.cl/'
log_file = open('logs/log_corporativo.rtf', 'w')

dic = {
    'xmlns:owl': BASE_URI + 'ontologia/',
    'xmlns:foaf': 'http://xmlns.com/foaf/0.1/',
    'xmlns:bio': 'http://vocab.org/bio/0.1/',
    'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'xmlns:rdfs': 'http://www.w3.org/2000/01/rdf-schema#'
}

output = {
    'corporation_root' : ET.Element( 'rdf:RDF', dic ), #Base element for authorities
}

pp = pprint.PrettyPrinter(indent=4)

countries_set = set([])
i = 0
for event, elem in ET.iterparse( 'input/autoridades-corporativos.xml', events=( 'start', 'end' ) ):
    if event != 'start' or elem.tag != 'authority': continue
    authority = elem
    authIDElement = authority.find('authorityID')

    if authIDElement == None or authIDElement.text == None: 
        '''
        stringers = "ERROR AUTH_ID 'None' en autoridad. Control number = '" + (authority.find(".//*[@tag='001']").text if authority.find(".//*[@tag='001']") != None else "undefined") + "'\n"
        log_file.write( stringers) #Imprimir en log debug
        stringors = "terrible error" + authority.find(".//*[@tag='001']").text if authority.find(".//*[@tag='001']") != None else "undefined" 
        print(stringors)
        '''
        continue
    authID = authIDElement.text

    # Obtener mark 110 
    nameElement = authority.find( ".//*[@tag='110']" )
    if nameElement == None or nameElement.text == None: continue

    corporationElement = ET.SubElement( output['corporation_root'], 'owl:NamedIndividual', {'rdf:about': BASE_URI + 'corporacion/' + authID} )

    nElement = ET.SubElement(corporationElement, 'foaf:name')
    nElement.text = nameElement.text
    nLabelElement = ET.SubElement(corporationElement, 'rdfs:label')
    nLabelElement.text = nameElement.text
    # Reviso si el nombre contiene una localidad entre parentesis
    
    name = pp.pformat(nameElement.text)

    start_index = name.find("(")
    if start_index != -1: 
    	name_tail = name[start_index:]
    	end_index = name_tail.find(")")
    	if end_index != -1:
    		loc = name[start_index+1:end_index+start_index]
    		#Chequear si loc no tiene numeros
    		if not hasNumbers(loc):
    			#Registros no pueden contener caracter ':'
    			if loc.find(":") != -1: 
    				log_file.write("ERROR LOCALIDAD nombre localidad '" + loc + "'' en autoridad '" + name + "'\n") #Imprimir en log debug
    				continue

    			loc_arr = loc.split(",")
    			countries_set.add(loc_arr[len(loc_arr) - 1].strip())

    elem.clear()
    i += 1
print i
log_file.close()
ET.ElementTree( output['corporation_root'] ).write( 'output/corporaciones.rdf', 'utf-8' )

with open( 'output/corporaciones.rdf', 'r' ) as ini, open( 'output/corporaciones_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )


