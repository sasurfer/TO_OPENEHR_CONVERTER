#!/usr/bin/python3
'''Writes the XML understable by the converter 
'''
import json
import logging
from lxml import etree
from config import data_elements,form_number
import argparse
import sys
from datetime import datetime


def format_data_element_name(json_data_element_name):
	return json_data_element_name.replace('urn:ccdg:', '').replace('dataelement', 'Dataelement').replace(':', '_')

def generate_data_element_block(block_data, parent):
	for key in block_data.keys():
		if key in ('lastChangedBy', 'lastChangedDate', 'formType'):
			continue
		formatted_key = format_data_element_name(key)
		block = etree.SubElement(parent, formatted_key)
		block.attrib['name'] = data_elements[formatted_key]
		if formatted_key == 'Dataelement_68_2':
			convert_data_element_68_2(block_data[key]['column'], block)
		else:
			block.text = f'{block_data[key]}'

def convert_data_element_68_2(json_data_element,parent):
	if isinstance(json_data_element, dict):
		value = etree.SubElement(parent, 'Value')
		value.text = json_data_element['urn:ccdg:dataelement:68:2']
	else: # multiple values
		for v in json_data_element:
			value = etree.SubElement(parent, 'Value')
			value.text = v['urn:ccdg:dataelement:68:2']

def get_name_from_episode_data(time_data):
    dt = datetime.strptime(time_data, '%Y-%m-%d %H:%M:%S.%f')
    return datetime.strftime(dt, '%d/%m/%Y')

def create_header():
	'''create general header'''
	BHImport = etree.Element("BHImport")
	BHImport.attrib['xmlns'] = 'http://registry.samply.de/schemata/import_v1'
	mdr = etree.SubElement(BHImport, 'Mdr')
	url = etree.SubElement(mdr, 'URL')
	url.text = 'https://mdr.osse-register.de/v3/api/mdr'
	namespace = etree.SubElement(mdr, 'Namespace')
	namespace.text = 'urn:ccdg'	
	return BHImport

def main():
	print('FROM CSV to XML BBMRI')
	parser = argparse.ArgumentParser()
	parser.add_argument('--loglevel',help='the logging level:DEBUG,INFO,WARNING,ERROR or CRITICAL',default='WARNING')
	parser.add_argument('--inputfile',help="csv containing the patients' data",default='inputfile')
	parser.add_argument('--baseoutputfile',help='basename for output file',default='output')

	args=parser.parse_args()


	loglevel=getattr(logging, args.loglevel.upper(),logging.WARNING)
	if not isinstance(loglevel, int):
		raise ValueError('Invalid log level: %s' % loglevel)
	logging.basicConfig(filename='./FromDbCSVtoXML.log',filemode='w',level=loglevel)


	inputfile=args.inputfile
	print(f'inputfile given: {inputfile}')
	logging.info(f'inputfile given: {inputfile}')

	baseoutputfile=args.baseoutputfile

	BHImport=create_header()
	
	f = open(inputfile, "r")
	line = f.readline()

	g=open(baseoutputfile+"_1.xml",'wb')


	# each bhpatient
	patientcounter=0
	a=True
	while a:
		#read rows from csv into a list until a new PatientId comes
		#then put it into a buffer list
		data=[]
		line = f.readline().split("|")
		patientcounter+=1
		patientid=line[11]
		logging.debug('******************************')
		logging.debug(f'PATIENT {patientid} patient_order: {line[0]}')
		data.append(line)

		b=True
		while b:
			last_pos=f.tell()
			line = f.readline()
			if(line==''):#end of file
				logging.debug('end of file')
				b=False
				a=False			
			else:
				line=line.split("|")
				if(line[11]==patientid):
					data.append(line)
				else:
					f.seek(last_pos)
					b=False

		#list for patient completed
		c=data[0][5]
		for ii,d in enumerate(data):
			if(d[5] != c):
				logging.debug(f'patient {patientid} patient_order={line[0]}')
				logging.debug(f'basic data differ')
				logging.debug(f'1st {c}')
				if(ii+1==2):
					logging.debug(f'{ii+1}nd {d[5]}')	
				elif(ii+1==3):
					logging.debug(f'{ii+1}rd {d[5]}')
				else:
					logging.debug(f'{ii+1}th {d[5]}')
		BHPatient = etree.SubElement(BHImport, 'BHPatient')
		identifier = etree.SubElement(BHPatient, 'Identifier')
		identifier.attrib['encrypted'] = 'false'
		identifier.text = f'{patientid}'
		locations = etree.SubElement(BHPatient, 'Locations')
		location = etree.SubElement(locations, 'Location')
		location.attrib['name'] = data[0][2]
		basic_data = etree.SubElement(location, 'BasicData')
		form = etree.SubElement(basic_data, 'Form')
		form.attrib['name'] = data[0][4]
		#logging.debug(line[5])
		generate_data_element_block(json.loads(data[0][5]), form)

		# # create the events part for every patient
		events = etree.SubElement(location, 'Events')
		for d in data:
			event = etree.SubElement(events, 'Event')
			event.attrib['eventtype']=d[6]
			event.attrib['name']=get_name_from_episode_data(json.loads(d[7])['timestamp'])
			longitudinal_data = etree.SubElement(event, 'LogitudinalData')
			if(d[6].lower() not in form_number):
				logging.error(f'form number not found for {d[6]}')
				sys.exit(1) 
			form_event_data = etree.SubElement(longitudinal_data, 'Form'+form_number[d[6].lower()])#we have form,form1,form2,form3,form4
			form_event_data.attrib['name']=d[8]
			#logging.debug(d[9])
			generate_data_element_block(json.loads(d[9]), form_event_data)

		if(a==True and (patientcounter%1000)==0):#every 1000 patients I wrote a file
			etree.indent(BHImport)
		#	g.write(etree.tostring(BHImport, pretty_print=True,method='text', encoding="UTF-8"))
			g.write(etree.tostring(BHImport, encoding="UTF-8"))
			g.close()
			print(f'wrote first {patientcounter} patients')
			logging.debug(f'wrote first {patientcounter} patients')
			#create new header and open file for next 1000 patients
			BHImport=create_header()
			thous=patientcounter/1000
			thous_string=str(int(thous+1))
			g=open(baseoutputfile+"_"+thous_string+".xml",'wb')



	# # write and close file
	etree.indent(BHImport)
#	g.write(etree.tostring(BHImport, pretty_print=True,method='text', encoding="UTF-8"))
	g.write(etree.tostring(BHImport, encoding="UTF-8"))
	g.close()

	print(f'globally wrote {patientcounter} patients')
	logging.debug(f'globally wrote {patientcounter} patients')


if __name__ == '__main__':
	main()
