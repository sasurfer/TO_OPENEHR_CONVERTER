#!/usr/bin/python3
'''find an element in the BHPatient tree and return its index or not found'''
import xml.etree.ElementTree as ET
import logging

def mefinder(myleaf,listofitems):
	annotation=myleaf.get_annotation()
#	if (myleaf.get_id()=='date_of_start_of_targeted_therapy'):
#		print("*********************")
#		print("--------------------")
#		print(myleaf.get_annotation())
#		print(myleaf.get_annotation()['XSD label'])
	indexes=[]
	if ('XSD label' in annotation):
		logging.debug(f"looking for {annotation['XSD label']}")
		for index,(a,b,c), in enumerate(listofitems):
			if a==annotation['XSD label']:
				indexes.append(index)
		return indexes
	return indexes

def all_items(bhtree,ns):
	return [(remove_ns(elem.tag,ns),elem.text,elem.attrib) for elem in bhtree.iter()]

def remove_ns(tag,ns):
	return tag.replace(ns,'')

def meventfinder(myleaf,listofitems):
	annotation=myleaf.get_annotation()
#	if (myleaf.get_id()=='date_of_start_of_targeted_therapy'):
#		print("*********************")
#		print("--------------------")
#		print(myleaf.get_annotation())
#		print(myleaf.get_annotation()['XSD label'])
	indexes=[]
	if ('XSD label' in annotation):
#		logging.debug(f"looking for {annotation['XSD label']}")
		for index,(a,b,c), in enumerate(listofitems):
#			logging.debug(index)
			for k in c:
				logging.debug(f'c[k] {c[k]}')
				if c[k]==annotation['XSD label']:
					indexes.append(index)
#					logging.debug(f'FOUNDDDDDDDDD {index}')
		return indexes
	return indexes


def mtimefinder(annotation,listofitems):
	time="10/12/2008"
	logging.debug(f"TIME: listofitems {listofitems}")
	logging.debug(f"TIME: {annotation}")
	if ('XSD label' in annotation):
		logging.debug(f"TIME:looking for {annotation['XSD label']}")
		for item in listofitems: #c contains attribute name and eventtype. ex {'name': '10/11/2008', 'eventtype': 'Pharmacotherapy'}
			logging.debug(f"TIME:item {item}")
			if("eventtype" in item[2]):
				if item[2]["eventtype"]==annotation['XSD label']:
					time=item[2]["name"]
					return time
	return time

