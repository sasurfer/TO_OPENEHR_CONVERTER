from typing import Any,Callable
import re
import json
from json_tools import diff
import argparse
import logging
import collections


def compare(firstjson:json,secondjson:json)->None:
	'''
	compare the given jsons
	'''
	one=flatten(firstjson)
	two=flatten(secondjson)
	logging.info("Diff between first and second json")
	logging.info(json.dumps((diff(one,two)),indent=4))
	return

def readjson(filename:str)->json:
	'''read in the json file'''
	with open(filename,'r') as f:
		newjson = json.load(f)	
	return newjson

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


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--loglevel',help='the logging level:DEBUG,INFO,WARNING,ERROR or CRITICAL',default='INFO')
	parser.add_argument('--inputfiles',help='input filenames separated by a comma',default='input1,input2')
	parser.add_argument('--outputfilebasename',help='output file basename',default='output')
	args=parser.parse_args()

	loglevel=getattr(logging, args.loglevel.upper(),logging.WARNING)
	if not isinstance(loglevel, int):
		raise ValueError('Invalid log level: %s' % loglevel)
	logging.basicConfig(filename='./CompareTwoJsonFiles.log',filemode='w',level=loglevel)

	
	inputfiles=args.inputfiles.split(',')
	print(f'inputfiles: {inputfiles[0]} {inputfiles[1]}')
	logging.info(f'inputfiles: {inputfiles[0]} {inputfiles[1]}')

	firstjson=readjson(inputfiles[0])
	secondjson=readjson(inputfiles[1])

	firstchanged=change_naming(firstjson)
	secondchanged=change_naming(secondjson)

	compare(firstchanged,secondchanged)

	print(f'FINISHED SUCCESSFULLY')

if __name__ == '__main__':
	main()
