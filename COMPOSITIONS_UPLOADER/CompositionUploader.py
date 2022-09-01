#!/usr/bin/python3
'''Post the compositions in a given directory filtered or not by a basename
   now one ehr per composition
'''
import json
import logging
import requests
from url_normalize import url_normalize
import sys
import argparse
import os
from typing import Any,Callable
import re
from json_tools import diff
import collections
import uuid

def compare(firstjson:json,secondjson:json)->None:
	'''
	compare the given jsons
	'''
	one=flatten(firstjson)
	two=flatten(secondjson)
	return json.dumps((diff(one,two)),indent=4)


def change_naming(myjson:json)->json:
	'''change naming convention on the json'''
	return change_dict_naming_convention(myjson,convertcase)

def flatten(d:dict, parent_key:str='', sep:str='_')->dict:
	items = []
	for k, v in d.items():
		new_key = parent_key + sep + k if parent_key else k
		if isinstance(v, collections.abc.MutableMapping):
				items.extend(flatten(v, new_key, sep=sep).items())
		else:
				items.append((new_key, v))
	return dict(items)

def change_dict_naming_convention(d:Any, convert_function:Callable[[str],str])->dict:
	"""
	Convert a nested dictionary from one convention to another.
	Args:
		d (dict): dictionary (nested or not) to be converted.
		convert_function (func): function that takes the string in one convention and returns it in the other one.
	Returns:
			Dictionary with the new keys.
	"""
	if not isinstance(d,dict):
			return d
	new = {}
	for k, v in d.items():
		new_v = v
		if isinstance(v, dict):
				new_v = change_dict_naming_convention(v, convert_function)
		elif isinstance(v, list):
				new_v = list()
				for x in v:
						new_v.append(change_dict_naming_convention(x, convert_function))
		new[convert_function(k)] = new_v
	return new


def convertcase(name:str)->str:
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def analyze_comparison(comparison_results:list)->int:
	ndifferences=0
	for l in comparison_results:
		if "add" in l:
			if("_uid" in l['add']): #ignore if it is _uid 
				continue
			else:
				ndifferences+=1
				logging.debug(f"difference add:{l['add']} value={l['value']}")
		elif "remove" in l:
			ndifferences+=1
			logging.debug(f"difference remove:{l['remove']} value={l['value']}")

		elif "replace" in l:
			if(l['replace'].endswith("time")):
				if(l['value'][:18]==l['prev'][:18]):
					continue
				ndifferences+=1
				logging.debug(f"difference replace:{l['replace']} value={l['value']} prev={l['prev']}")				
			elif(l['value'].startswith('P') and l['value'].endswith('D')):
				continue
			else:
				ndifferences+=1
				logging.debug(f"difference replace:{l['replace']} value={l['value']} prev={l['prev']}")		
	return ndifferences			

def create_ehr(client,EHR_SERVER_BASE_URL, auth,patientid):
	logging.debug('----POST EHR----')
	body1='''
	{
	  "_type" : "EHR_STATUS",
	  "name" : {
	    "_type" : "DV_TEXT",
	    "value" : "EHR Status"
	  },
	  "subject" : {
	    "_type" : "PARTY_SELF",
	    "external_ref" : {
	      "_type" : "PARTY_REF",
	      "namespace" : "BBMRI",
	      "type" : "PERSON",
	      "id" : {
	        "_type" : "GENERIC_ID",
	'''
	body2=f'	"value" : "{patientid}",'
	body3='''
	        "scheme" : "BBMRI"
	      }
	    }
	  },
	  "archetype_node_id" : "openEHR-EHR-EHR_STATUS.generic.v1",
	  "is_modifiable" : true,
	  "is_queryable" : true
	}
	'''
	body=body1+body2+body3
	logging.debug(f'body={body}')
#	sys.exit(0)
	ehrs = client.post(EHR_SERVER_BASE_URL + 'ehr', \
	                   params={},headers={'Authorization':auth,'Content-Type':'application/JSON','Accept': 'application/json','Prefer': 'return={representation|minimal}'},\
	                   data=body)


	print(f'create ehr status_code={ehrs.status_code}')
	logging.info(f'create ehr: status_code={ehrs.status_code}')
	logging.debug(f'ehr url={ehrs.url}')
	logging.debug(f'ehrs.headers={ehrs.headers}')
	logging.debug(f'ehrs.text={ehrs.text}')
	logging.debug(f'ehrs.json={ehrs.json}')

	if(ehrs.status_code==409 and 'Specified party has already an EHR set' in json.loads(ehrs.text)['message']):
		#get ehr summary by subject_id , subject_namespace
		payload = {'subject_id':patientid,'subject_namespace':'BBMRI'}
		ehrs = client.get(EHR_SERVER_BASE_URL + 'ehr',  params=payload,headers={'Authorization':auth,'Content-Type':'application/JSON','Accept': 'application/json'})
		print('ehr already existent')
		logging.info('ehr already existent')
		logging.debug('----GET EHR----')
		print(f'get ehr: status_code={ehrs.status_code}')
		logging.info(f'get ehr: status_code={ehrs.status_code}')		
		logging.debug(f'ehr url={ehrs.url}')
		logging.debug(f'ehr.headers={ehrs.headers}')
		logging.debug(f'ehr.text={ehrs.text}')
		logging.debug(f'ehr.json={ehrs.json}')

		ehrid=json.loads(ehrs.text)["ehr_id"]["value"]
		print(f'Patient {patientid}: retrieved ehrid={ehrid}')
		logging.info(f'Patient {patientid}: retrieved ehrid={ehrid}')
		return ehrid

#	print(f'ehrheaders={ehrs.headers}')
	urlehrstring = ehrs.headers['Location']
	ehridstring = "{"+urlehrstring.split("v1/ehr/",2)[2]
	ehrid=uuid.UUID(ehridstring)
	print(f'Patient {patientid}: ehrid={str(ehrid)}')
	logging.info(f'Patient {patientid}: ehrid={str(ehrid)}')
	return ehrid






def main():
	print('COMPOSITIONS UPLOADER')
	parser = argparse.ArgumentParser()
	parser.add_argument('--loglevel',help='the logging level:DEBUG,INFO,WARNING,ERROR or CRITICAL',default='WARNING')
	parser.add_argument('--inputdir',help='dir containing the compositions',default='RESULTS')
	parser.add_argument('--basename',help='basename to filter compositions')
	parser.add_argument('--templatename',help='template to use when posting',default='crc_cohort')
	parser.add_argument('--check',action='store_true', help='check the missing leafs for leafs that should be there but are not')
	args=parser.parse_args()


	loglevel=getattr(logging, args.loglevel.upper(),logging.WARNING)
	if not isinstance(loglevel, int):
		raise ValueError('Invalid log level: %s' % loglevel)
	logging.basicConfig(filename='./CompositionUploader.log',filemode='w',level=loglevel)


	inputdir=args.inputdir
	print(f'inputdir given: {inputdir}')
	logging.info(f'inputdir given: {inputdir}')

	if not os.path.exists(inputdir):
		print(f'directory {inputdir} does not exist')
		logging.error(f'directory {inputdir} does not exist')
		sys.exit(1)

	basename=args.basename

	if(basename):
		logging.info(f'basename given: {basename}')
		print(f'basename given: {basename}')
		
	check=False
	if args.check:
		check=True
		print ('Check is set to true')
		logging.info('Check is set to true')



	#get the list of files
	filelist=[]
	if basename:
		for file in os.listdir(inputdir):
			if file.startswith(basename) and file.endswith(".json"):
				logging.debug(f'file added {os.path.join(inputdir, file)}')
				filelist.append(file)
	else:
		for file in os.listdir(inputdir):
			if file.endswith(".json"):
				logging.debug(f'file added {os.path.join(inputdir, file)}')
				filelist.append(file)    	


#	Now sort the list
	filelist.sort(key=lambda a: int(a.split('_')[1]))
	for i,f in enumerate(filelist):
		logging.info(f'file {i+1} = {f}')


# 	Initialize the connection to ehrbase
	EHR_SERVER_BASE_URL = 'http://localhost:8080/ehrbase/rest/openehr/v1/'
	EHR_SERVER_BASE_URL_FLAT = 'http://localhost:8080/ehrbase/rest/ecis/v1/composition/'
	client = requests.Session()
	client.auth = ('ehrbase-user','SuperSecretPassword')
	auth="Basic ZWhyYmFzZS11c2VyOlN1cGVyU2VjcmV0UGFzc3dvcmQ="

	nfiles=len(filelist)
	print(f'{nfiles} to insert')
	logging.info(f'{nfiles} to insert')

	#check if the template is already in the db
	templatename=args.templatename

	myurl=url_normalize(EHR_SERVER_BASE_URL  + 'definition/template/adl1.4')
	response = client.get(myurl,params={'format': 'JSON'},headers={'Authorization':auth,'Content-Type':'application/JSON'})
	templates=[a["template_id"] for a in json.loads(response.text)]
	if(templatename not in templates):
		print(f'Missing template {templatename}')
		logging.error(f'Missing template {templatename}')
		sys.exit(1)


#   loop over files and upload the compositions
	myurl=url_normalize(EHR_SERVER_BASE_URL_FLAT)
	compinserted=0
	compok=0
	for i,file in enumerate(filelist):
		print(f'********FILE {i+1}/{nfiles}  {file}********')
		logging.info(f'********FILE {i+1}/{nfiles}  {file}********')
		filename=os.path.join(inputdir, file)
		with open(filename) as json_file:
			compositionjson = json.load(json_file)	
		patientid='Patient'+compositionjson[templatename+'/context/case_identification/patient_pseudonym']			
		print(f'Patientid={patientid}')
		logging.info(f'Patientid={patientid}')
#		create ehr
		ehrid=create_ehr(client,EHR_SERVER_BASE_URL, auth,patientid)
# 		post composition
		compositionjson=json.dumps(compositionjson)
		response = client.post(myurl,
					   params={'ehrId':str(ehrid),'templateId':templatename,'format':'FLAT'}, \
					   headers={'Authorization':auth,'Content-Type':'application/json','Prefer':'return=representation'}, \
					   data=compositionjson  \
					  )
		if(response.status_code != 200 and response.status_code != 201):
			print(f"Couldn't post the composition. Error={response.status_code}")
			print(f'response.text {response.text}')
			logging.info(f"Couldn't post the composition. Error={response.status_code}")
			logging.info(f'response.headers {response.headers}')
			logging.info(f'response.text {response.text}')
		else:
			compinserted+=1
			print(f'Composition inserted')
			compositionUid=json.loads(response.text)["compositionUid"]
			print(f'compositionUid={compositionUid}')
			logging.info(f'compositionUid={compositionUid}')			
			if(check):
				print(f'checking...')
				logging.info(f'checking...')
				#get composition created and compare with the one posted
				myurlu=url_normalize(EHR_SERVER_BASE_URL_FLAT+compositionUid) 
				response = client.get(myurlu, \
					   params={'ehrId':str(ehrid),'templateId':templatename,'format':'FLAT'}, \
					   headers={'Authorization':auth,'Content-Type':'application/json'}, \
					  )
				if(response.status_code != 200 and response.status_code != 201):
					print(f"Couldn't retrieve the composition. Error{response.status_code}")
					logging.info(f"Couldn't retrieve the composition. Error{response.status_code}")
					logging.info(f'response.headers {response.headers}')
					logging.info(f'response.text {response.text}')	
				else:			
					origjson=json.loads(compositionjson)
					retrievedjson=json.loads(response.text)["composition"]
					origchanged=change_naming(origjson)
					retrchanged=change_naming(retrievedjson)

					comparison_results=compare(origchanged,retrchanged)
					ndiff=analyze_comparison(comparison_results)
					if(ndiff>0):
						print('original and retrieved json differ')
						logging.info('original and retrieved json differ')
						logging.debug(f'comparison_results:')
						logging.debug(comparison_results)
					else:
						print('original and retrieved json do not differ')
						logging.info('original and retrieved json do not differ')
						compok+=1

	print(f'{compinserted}/{nfiles} compositions inserted successfully')
	logging.info(f'{compinserted}/{nfiles} compositions inserted successfully')
	print(f'{nfiles-compinserted}/{nfiles} compositions with errors')
	if(check):
		print(f'{compok}/{compinserted} checked successfully')
		logging.info(f'{compok}/{compinserted} checked successfully')
		print(f'{compinserted-compok}/{compinserted} checked unsuccessfully')
		logging.info(f'{compinserted-compok}/{compinserted} checked unsuccessfully')

if __name__ == '__main__':
	main()
