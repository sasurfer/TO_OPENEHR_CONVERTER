#!/usr/bin/python3
'''read a webtemplate and return it as json'''
import json
import logging

def read_wt(file):
	with open(file) as f:
		compositionjson = json.load(f)
#		logging.debug(f'webtemplate from {file}:/n {json.dumps(compositionjson, indent = 4, sort_keys=True)}')
	return compositionjson['tree'],compositionjson['defaultLanguage']


if __name__ == '__main__':
    main()
