from lxml import etree

def prettify(filename):
    ugly_xml = open(filename, 'r')
    tree = etree.parse(ugly_xml)
    return tree.write(filename[0:-4] + '_pretty.rdf', pretty_print=True, encoding='utf-8')

