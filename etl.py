import xml.etree.ElementTree as ET
from xml.dom import minidom
import time

def prettify(elem):
    # Return a pretty-printable XML string for the Element
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

base_uri = 'http://datos.uchile.cl/'

input_tree = ET.parse('input/autoridades.xml')
input_root = input_tree.getroot()

# Base element for authorities
output_person_root = ET.Element('rdf:RDF', {'xmlns:owl': base_uri + 'ontologia/',
                                            'xmlns:foaf': 'http://xmlns.com/foaf/spec/',
                                            'xmlns:bio': 'http://someuri.com/',
                                            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})

# Base element for years
output_year_root = ET.Element('rdf:RDF', {'xmlns:owl': base_uri + 'ontologia/',
                                         'xmlns:foaf': 'http://xmlns.com/foaf/spec/',
                                         'xmlns:bio': 'http://someuri.com/',
                                         'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})

n_authorities = len(input_root.findall('authority'))
i = 1

birthYearDict = {}
deathYearDict = {}

# Iterate through authorities
for authority in input_root.iterfind('authority'):

    # Get the authority ID
    authID = authority.find('authorityID').text

    # Create person instance
    personElement = ET.SubElement(output_person_root, 'owl:NamedIndividual', {'rdf:about': base_uri + 'autoridad/' + authID})

    # Get marcEntry element with tag attr == 100
    marcEntryTextArray = authority.find(".//*[@tag='100']").text.split(',')

    # **REQUIRED FIELD** filter
    if len(marcEntryTextArray) == 1: continue

    # Create name element
    nameElement = ET.SubElement(personElement, 'foaf:name')
    nameElement.text = marcEntryTextArray[1].strip() + ' ' + marcEntryTextArray[0].strip()

    # Birth and death case
    if len(marcEntryTextArray) == 3:
        yearTextArray = marcEntryTextArray[2].split('-')
        # Filter trash or weird data
        # TODO: handle cases 'xxxx a.C' and 'xxxx o x' with any variants included
        for yearIndex in range(len(yearTextArray)):
            try:
                time.strptime(yearTextArray[yearIndex].strip(), "%Y").tm_year
            except ValueError:
                yearTextArray[yearIndex] = ''

        # Create birth element and instance if the year exists
        if yearTextArray[0] != '':
            birthEventUri = base_uri + 'nacimiento/' + yearTextArray[0].strip()
            ET.SubElement(personElement, 'bio:event', {'rdf:resource': birthEventUri})
            ET.SubElement(output_year_root, 'owl:NamedIndividual', {'rdf:about': birthEventUri})
            try:
                birthYearDict[yearTextArray[0].strip()]
            except KeyError:
                birthYearDict[yearTextArray[0].strip()] = ''

        # Create death element and instance if the year exists
        if yearTextArray[1] != '':
            deathEventUri = base_uri + 'muerte/' + yearTextArray[1].strip()
            ET.SubElement(personElement, 'bio:event', {'rdf:resource': deathEventUri})
            ET.SubElement(output_year_root, 'owl:NamedIndividual', {'rdf:about': deathEventUri})
            try:
                deathYearDict[yearTextArray[1].strip()]
            except KeyError:
                deathYearDict[yearTextArray[1].strip()] = ''

    # Progress feedback
    if i%100 == 0:
         print str(round(i*100.0/n_authorities,2)) + '%'
    i += 1

# Write the output
output_person_tree = ET.ElementTree(output_person_root)
output_person_tree.write('output/personas.rdf', 'utf-8')

output_year_tree = ET.ElementTree(output_year_root)
output_year_tree.write('output/fechas.rdf', 'utf-8')

print '100.00%'

# For debugging
print prettify(output_year_root)
