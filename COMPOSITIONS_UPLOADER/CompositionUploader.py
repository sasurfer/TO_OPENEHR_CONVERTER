#!/usr/bin/python3
'''Post the compositions in a given directory filtered or not by a basename
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
	#get ehr summary by subject_id , subject_namespace
	payload = {'subject_id':'patient1','subject_namespace':'CRS4'}
	ehrs = client.get(EHR_SERVER_BASE_URL + 'ehr',  params=payload,headers={'Authorization':auth,'Content-Type':'application/JSON','Accept': 'application/json'})
	logging.debug(ehrs.status_code)
	logging.debug(ehrs.url)
	logging.debug(ehrs.headers)
	logging.debug(ehrs.text)
	ehrid=''
	if (ehrs.text):
		ehrid=json.loads(ehrs.text)["ehr_id"]["value"]
	else:
		print(f'Cannot connect to ehrbase')
		logging.error(f'Cannot connect to ehrbase')
		sys.exit(1)

	print(f'ehr_id={ehrid}')
	logging.info(f'ehr_id={ehrid}')

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

#   loop over files and load them
	myurl=url_normalize(EHR_SERVER_BASE_URL_FLAT)
	compinserted=0
	compok=0
	for i,file in enumerate(filelist):
		print(f'********FILE {i+1}/{nfiles}  {file}********')
		logging.info(f'********FILE {i+1}/{nfiles}  {file}********')
		filename=os.path.join(inputdir, file)
		with open(filename) as json_file:
			compositionjson = json.load(json_file)
#		logging.debug(f'{compositionjson}')
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
			if(check):
				#get composition created and compare with the one posted
				compositionUid=json.loads(response.text)["compositionUid"]
				logging.debug(f'compositionUid={compositionUid}')
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
					logging.debug('Checking the composition retrieved against the one given')					
					origjson=json.loads(compositionjson)
					retrievedjson=json.loads(response.text)["composition"]
					origchanged=change_naming(origjson)
					retrchanged=change_naming(retrievedjson)

					comparison_results=compare(origchanged,retrchanged)
					ndiff=analyze_comparison(comparison_results)
					if(ndiff>0):
						logging.info('original and retrieved json differ')
					else:
						logging.info('original and retrieved json do not differ')
						compok+=1

	print(f'{compinserted}/{nfiles} compositions inserted successfully')
	logging.info(f'{compinserted}/{nfiles} compositions inserted successfully')
	if(check):
		print(f'{compok}/{compinserted} checked successfully')
		logging.info(f'{compok}/{compinserted} checked successfully')


if __name__ == '__main__':
	main()
