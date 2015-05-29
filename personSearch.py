# -*- coding: utf-8 -*-

#this code only will work for the following structure of xml
#...
# <owl:NamedIndividual rdf:about="http://datos.uchile.cl/autoridad/201-0138321">
#   <foaf:name>Raisuddin Ahmed</foaf:name>
# </owl:NamedIndividual>
#...
#the code can be generalized, but at the lack of optimisation

class personDictionary:
	dictionary = None
	def getDictionary(self):
		return self.dictionary
	def get(self, keyword):
		return self.dictionary.get(keyword, None)
	def __init__(self, dictionary):
		if dictionary:
			self.dictionary = dictionary


#as stated above, this method won't accept any rdf/xml file
def makeDictionary(filepath, keyTag, attribute):
	import xml.etree.ElementTree as ET
	import lxml.etree as etree
	
	dictionary = {}

	for event, tree in ET.iterparse( filepath, events=( 'start', 'end', 'start-ns', 'end-ns' ) ):
		key = None
		value = None
		if event != 'end': continue
		for child in tree:
			if child.tag == keyTag:
				key = child.text
				value = tree.attrib[attribute]
		if key and value:
			dictionary[key] = value
	return personDictionary(dictionary) 

makeDictionary(
	filepath = 'output/personas_pretty.rdf', 
	keyTag = '{http://xmlns.com/foaf/0.1/}name', 
	attribute = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'
	)