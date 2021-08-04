#!/usr/bin/python3
'''Composition class definition'''
import json
import logging
import config

class Composition:
	def __init__(self,l_actleafs,l_actnoleafs,l_occurences):
		self.l_actleafs=l_actleafs
		self.l_actnoleafs=l_actnoleafs
		self.l_occurences=l_occurences
		self.createComposition()
		self.remove_starting_slash()

	def writeComposition(self,file):
		composition=json.dumps(self.composition,indent=4)
		with open(file,'w') as f:
			f.write(composition)


	def createComposition(self):
		self.composition={}
		for ll in self.l_actleafs:
			self.composition.update(ll.createandcorrecttotalpath(self.l_occurences))

	def remove_starting_slash(self):
		newcomposition={}
		for k,v in self.composition.items():
			logging.debug(f"k,v {k} {v}")
#			print("---")
			oldk=k
			newk=k[1:len(k)]
#			print (oldk,newk)
			if(isinstance(v, dict)):
				for mykey,myvalue in v.items():
					newkt=newk+'|'+mykey
					newcomposition[newkt]=myvalue
			else:
				newcomposition[newk]=v
		self.composition=newcomposition
