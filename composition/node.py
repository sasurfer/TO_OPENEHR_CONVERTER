#!/usr/bin/python3
'''node class definition'''
import logging

class Node:
	def __init__(self,nodeid,nodepath,nodecardinality_min,
		nodecardinality_max,nodeannotation,nodetoleaf=None):
		self.nodeid=nodeid
		self.nodepath=nodepath
		self.nodecardinality_min=nodecardinality_min
		self.nodecardinality_max=nodecardinality_max
		self.nodeannotation=nodeannotation
		self.nodetoleaf=nodetoleaf

	def get_id(self):
		return self.nodeid

	def get_path(self):
		return self.nodepath

	def get_leaf(self):
		return self.nodetoleaf

	def get_cardinality(self):
		return self.nodecardinality_min,self.nodecardinality_max

	def get_annotation(self):
		return self.nodeannotation

	def get_all(self):
		return self.nodeid,self.nodepath, \
		self.nodecardinality_min,self.nodecardinality_max,self.nodeannotation
