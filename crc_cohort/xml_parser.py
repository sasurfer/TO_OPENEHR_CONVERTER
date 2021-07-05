#!/usr/bin/python3
'''parse an xml crc_cohort file and returns a list containing bhpatient trees'''
import xml.etree.ElementTree as ET

def find_ns(bhtree):
	'''find the namespace from a bhtree'''
	ns=''
	try:
		i=bhtree.tag.index('BHPatient')
		ns=bhtree.tag[0:i]
		print(f"namespace={ns}")
	except ValueError:
		print('namespace not found')	
	return ns


def parse_xml(file):
	'''return a list of trees, one tree for each BHPatient'''
	mytree = ET.parse(file)
	myroot = mytree.getroot()
	listoftrees=[]
	ns=''
	nop=0
	for ch in myroot:
		if (ch.tag.find('BHPatient') != -1):
			nop+=1
#			print('found')
#			print(ch.tag)
			listoftrees.append(ch)
	print(f"Found {nop} patients in file {file}")
	return listoftrees

def main():
	file="/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CRC_COHORT/import_example.xml"
	listoftrees=parse_xml(file)
	# for tree in listoftrees:
	# 	myroot=tree
	# 	print(myroot.tag)
	# 	print(myroot.attrib)
	# 	print("-----------------------------")
	# 	for x in myroot:
	# 		print("x------")
	# 		print('\t',x.tag,x.attrib,x.text)
	# 		for y in x:
	# 			print("---y")
	# 			print('\t\t',y.tag,y.attrib,y.text)
	for elem in listoftrees[0].iter():
		print(elem.tag,elem.text,elem.attrib)
	# 	for pippo in myroot.findall('{http://registry.samply.de/schemata/import_v1}BHPatient'):
	# 		print('\n\n',pippo.tag,pippo.attrib)
	# 		for p in pippo:
	# 			print(p.tag,p.attrib)

if __name__ == '__main__':
    main()
