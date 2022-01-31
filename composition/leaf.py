#!/usr/bin/python3
'''leaf class definition'''
from rm.rmclasses import DV_BOOLEAN,DV_DATE,DV_TEXT,DV_CODED_TEXT,DV_DATE_TIME, \
			DV_IDENTIFIER,DV_DURATION,CODE_PHRASE,PARTY_PROXY,ISM_TRANSITION

import logging
from datetime import datetime as dt

class Leaf:
	def __init__(self,myid,name,path,rmtype,cardinality_min,
		cardinality_max,acceptable_values,compulsory,annotation):
		self.id=myid
		self.name=name
		self.pathnoid=path
		self.path=path
	#	self.path=path+"/"+self.id
		self.annotation=annotation
		self.rmtype=rmtype
		self.cardinality_min=cardinality_min
		self.cardinality_max=cardinality_max
		self.acceptable_values=acceptable_values
		self.compulsory=compulsory



	def get_id(self):
		return self.id

	def get_name(self):
		return self.name

	def get_path(self):
		return self.path

	def get_pathnoid(self):
		return self.pathnoid

	def get_annotation(self):
		return self.annotation

	def get_rmtype(self):
		return self.rmtype

	def get_cardinality(self):
		return self.cardinality_min,self.cardinality_max

	def get_acceptable_values(self):
		return self.acceptable_values

	def is_compulsory(self):
		return self.compulsory

	def get_all(self):
		return self.id,self.name,self.path,self.rmtype, \
		self.cardinality_min,self.cardinality_max,self.acceptable_values,self.annotation
	
	def set_path(self,path):
		self.path=path



class ActualLeaf(Leaf):
	def __init__(self,leaf,data,positioninXML,isnull=False):
		myid=leaf.get_id()
		name=leaf.get_name()
		path=leaf.get_path()
		rmtype=leaf.get_rmtype()
		cardinality_min,cardinality_max=leaf.get_cardinality()
		acceptable_values=leaf.get_acceptable_values()
		annotation=leaf.get_annotation()
		comp=leaf.is_compulsory()
		#print(leaf.get_all())
		super().__init__(myid,name,path,rmtype,cardinality_min,
		cardinality_max,acceptable_values,comp,annotation)
		self.positioninXML=positioninXML
		self.data=data
		self.isnull=isnull
		self.instantiate_data()

		logging.debug(f"INSTANT: {self.path} {self.pathnoid} {self.data}")

	def setnull(self,boolvalue):
		self.isnull=boolvalue

	def getnull(self):
		return self.isnull

	def get_positioninXML(self):
		return self.positioninXML

	def get_data(self):
		return self.data

	def set_data(self,data):
		self.data=data
		self.instantiate_data()

	def get_all(self):
		all=super_get_all()
		return all,positioninXML

	def instantiate_data(self):
		'''instantiate  according to rmtype and null boolean'''
		if self.isnull==True:
			self.rmobject=DV_CODED_TEXT(self.path,self.data)
		elif(self.rmtype=='DV_TEXT'):
			self.rmobject=DV_TEXT(self.path,self.data)
		elif(self.rmtype=="DV_CODED_TEXT" ):
			self.rmobject=DV_CODED_TEXT(self.path,self.data)
		elif(self.rmtype=="CODE_PHRASE"):
			self.rmobject=CODE_PHRASE(self.path,self.data)
		elif(self.rmtype=="DV_BOOLEAN"):
			self.rmobject=DV_BOOLEAN(self.path,self.data)
		elif(self.rmtype=="DV_DATE"):
			self.rmobject=DV_DATE(self.path,self.data)
		elif(self.rmtype=="DV_DATE_TIME"):
			if("T" not in self.data):
				if(self.data.count("/")==2):
					firstslash=self.data.find("/")
					if(firstslash==2):
						#dd/mm/yyyy
						date_obj = dt.strptime(self.data, '%d/%m/%Y')
						self.data=dt.strftime(date_obj, '%Y-%m-%d')+"T00:00:00.00Z"
					elif(firstslash==4):
						#yyyy/mm/dd
						date_obj = dt.strptime(self.data, '%Y/%m/%d')
						self.data=dt.strftime(date_obj, '%Y-%m-%d')+"T00:00:00.00Z"
				elif(self.data.count("-")==2):
					self.data=self.data+"T00:00:00.00Z"
				else:#only year provided
					self.data=self.data+"-01-01T00:00:00.00Z"
			self.rmobject=DV_DATE_TIME(self.path,self.data)
		elif(self.rmtype=="DV_IDENTIFIER"):
			self.rmobject=DV_IDENTIFIER(self.path,self.data)
		elif(self.rmtype=="DV_DURATION"):
			if(self.data[0]!='P'):
				if("suffix" in self.acceptable_values[0]):
					if(self.acceptable_values[0]['suffix']=="year"):
						value="P"+self.data+"Y"
						self.data=value
					elif(self.acceptable_values[0]['suffix']=="week"):
						value="P"+self.data+"W"
						self.data=value
			self.rmobject=DV_DURATION(self.path,self.data)
		elif(self.rmtype=="PARTY_PROXY"):
			self.rmobject=PARTY_PROXY(self.path,self.data)
		elif(self.rmtype=="ISM_TRANSITION"):
			self.rmobject=ISM_TRANSITION(self.path,self.data)
		else:
			logging.debug(f'rmtype not implemented yet {self.rmtype}')

	def createandcorrecttotalpath(self,listofoccurrences):
		'''search for a given path section and change it with the right occurence'''
		#in occurrences occurrence,position,label,path
		logging.debug(f"NNNNNNNNNNNNNNNN {self.get_id()}")
		logging.debug(f'occurrences={listofoccurrences}')
		self.totalpath=self.rmobject.get_path()
		logging.debug(f"totalpath {self.totalpath}")
		#get keys. each key is a path
		times=0
		k=list(self.totalpath.keys())[0]
		#each path has the same position and word so I'll do it once
		logging.debug("AAAAAAAAAAAAAAAAAAAAAAAAAA")
		logging.debug(k)
		logging.debug(f'self.positioninXML={self.positioninXML}')
		myoc={}
		for i,(oc,pos,label,path) in enumerate(listofoccurrences):
			logging.debug(f'i {i},oc {oc}, pos {pos}, label {label}, path {path}')
			logging.debug(self.positioninXML)
			if(pos<self.positioninXML):
				myoc[path]=oc
			else:
				break
			#extract words,position of 0 before :0
		logging.debug(f'myoc {myoc}')
		found=0
		listofindex=[]
		while found != -1:
			logging.debug(f'found {found}')
			found=k.find(":0",found+1)
			if (found > -1):
				slashbefore=k.rfind("/",0,found)
				name=k[slashbefore+1:found]
				logging.debug(f'path {k}')
				logging.debug(f'name {name} found {found} slashbefore {slashbefore}')
				listofindex.append([found,name])
		logging.debug(f' listofindex {listofindex} ')
		#now we correct
		#newtotalpath={}
		listofchanges=[]
		logging.debug(f'self.totalpath={self.totalpath}')
		logging.debug(f'myoc={myoc}')
		for k,v in self.totalpath.items():
			myk=k
			kfound=0
			for koc in myoc:
				if (koc in k):
					newk=myk[0:len(koc)-1]+str(myoc[koc])+myk[len(koc):]
					value=v
					logging.debug(f'k,newk {k} {newk}')
					kfound+=1
					myk=newk
			if(kfound>0):
				listofchanges.append([k,myk,value])

		for [kold,knew,value] in listofchanges:
			del self.totalpath[kold]
			self.totalpath[knew]=value
			logging.debug(f'FINAL k,newk,value {kold} {knew} {value}')
				#newtotalpath[myk]=value
				#k[len(koc)-2:len(koc)-1]=str(myoc[koc])

#		for k,v in newtotalpath.items():
#			self.totalpath[k]=v
	
		return self.totalpath

class NoLeaf(Leaf):
	def __init__(self,myid,name,path,rmtype,cardinality_min,
		cardinality_max,compulsory,annotation):
		super().__init__(myid,name,path,rmtype,cardinality_min,
		cardinality_max,[],compulsory,annotation)
		self.path=path	

	def get_all(self):
		return self.id,self.name,self.path,   \
		self.rmtype,self.cardinality_min,self.cardinality,self.annotation

class ActualNoLeaf(NoLeaf):
	def __init__(self,noleaf,positioninXML):
		myid=noleaf.get_id()
		name=noleaf.get_name()
		path=noleaf.get_path()
		rmtype=noleaf.get_rmtype()
		cardinality_min,cardinality_max=noleaf.get_cardinality()
		annotation=noleaf.get_annotation()	
		compulsory=noleaf.is_compulsory()
		super().__init__(myid,name,path,rmtype,cardinality_min,
		cardinality_max,compulsory,annotation)
		self.positioninXML=positioninXML

	def get_all(self):
		all=super_get_all()
		return all,positioninXML	

	def get_positioninXML(self):
		return self.positioninXML