import xml.etree.ElementTree as ET
from xml.dom import minidom
import lxml.etree as etree
import time

def prettify(elem):
    # Return a pretty-printable XML string for the Element
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

base_uri = 'http://datos.uchile.cl/'
with open('input/autoridades-corporativos.xml','r') as xml_file:
    input_tree = ET.parse(xml_file)
input_root = input_tree.getroot()

# Base element for corporativo
output_corporativo_root = ET.Element('rdf:RDF', {'xmlns:owl': base_uri + 'ontologia/',
                                            'xmlns:foaf': 'http://xmlns.com/foaf/spec/',
                                            'xmlns:bio': 'http://someuri.com/',
                                            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})

n_authorities = len(input_root.findall('authority'))
i = 1

# Iterate through authorities
for authority in input_root.iterfind('authority'):

    # Get the authority ID
    authID = authority.find('authorityID').text

    # Create corporative instance
    corporativeElement = ET.SubElement(output_corporativo_root, 'owl:NamedIndividual', {'rdf:about': base_uri + 'autoridad/' + authID})

    # Get marcEntry element with tag attr == 110 corporate name
    marcEntryTextArray = authority.find(".//*[@tag='110']").text

    #print marcEntryTextArray.__class__

    # **REQUIRED FIELD** filter
    if len(marcEntryTextArray) == 1: continue

    # Create name element
    nameElement = ET.SubElement(corporativeElement, 'foaf:name')
    nameElement.text = marcEntryTextArray.strip()

    #

    #print nameElement
    #print ET.tostring(nameElement,"utf-8").decode('utf-8')
    
# Write the output
output_corporativo_tree = ET.ElementTree(output_corporativo_root)
output_corporativo_tree.write('output/corporativo.rdf', 'utf-8')
with open( 'output/corporativo.rdf', 'r' ) as ini, open( 'output/corporativo_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )

print 'RDF Corporativo formado.'


