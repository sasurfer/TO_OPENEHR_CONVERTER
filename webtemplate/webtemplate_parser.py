#!/usr/bin/python3
'''parse a webtemplate tree given in json format and return a list of all the leafs with and without annotation and all the no leafs annotated'''
import json
import logging
from .webtemplate_reader import read_wt
import composition
from composition.leaf import Leaf,NoLeaf
from composition.node import Node
import rm
import logging

#rmtype_leafs=["DV_CODED_TEXT","PARTY_PROXY","CODE_PHRASE","DV_DURATION",
#	"DV_TEXT","DV_DATE","DV_DATE_TIME","ISM_TRANSITION","DV_IDENTIFIER",
#	"DV_BOOLEAN"]

def parse_wt(cj):
	path="/"
	for i in cj:
		logging.info(i)
	#root
	path=path+cj['id']
	print(f"path={path}")
#	for i in cj['children']:
#		print(i['id'])
	#context,category,language,territory,composer are treated
	#in another subroutine
	comp=True#compulsory flag
	listofleafs=[]	
	listofnoleafsannotated=[]
	listofNodes=[]
	for ch in cj['children']:
		# if ( ch['id']=='category' or ch['id']=='language'  
		# 	or ch['id']=='territory' or ch['id']=='composer' ):
		# 	continue
#		print(ch['id'])
		findleaf(ch,path,listofleafs,listofnoleafsannotated,comp,listofNodes)
#		print (f'LISTOFLEAFS-1 {listofleafs[0].get_all()}')
	logging.debug(f"len(listofleafs)={int(len(listofleafs))}")

	count = sum(map(lambda x : x.get_annotation() !='Not mapped', listofleafs))
	logging.debug(f"count of annotated leafs {count}")
	# with open("temp",'w') as f:
	# 	for i in listofleafs:
	# 		f.write((i.get_path()+'\n'))
#	pippo=Leaf("id","name",path,"Aaa","AA",3)
#id,name,path,mappedto,rmtype,cardinality
#	print(pippo.get_all())
#	print (f'LISTOFLEAFS {listofleafs[0].get_all()}')
	return listofleafs,listofnoleafsannotated,listofNodes
	

def findleaf(root,path,listofleafs,listofnoleafsannotated,comp,listofNodes):
	if (root['id']=="clinical_synopsis"):
 		logging.debug(f"SYNOPSYS {path} {root['min']} {root['max']}")
	if(comp):
		if 'min' in root:
			if (root['min']<1):
				comp=False	
	if 'children' in root:
		if( 'max' in root and ( root['max']==-1 or root['max']>1 )):
			path=path+'/'+root['id']+':0'
			if 'annotations' in root:
				annotations=root['annotations']
				if 'XSD label' in annotations:
					annotations['XSD label']=annotations['XSD label'].strip()
			else:
				annotations='Not mapped'
			if 'name' not in root:
				root['name']=root['id']
				logging.debug(f"added {root['name']} that was missing")
			pippo=NoLeaf(root['id'],root['name'],path, \
				root['rmType'],root['min'],root['max'],comp,annotations)
			listofnoleafsannotated.append(pippo)
			pluto=Node(root['id'],path,root['min'],root['max'],annotations,pippo)
			listofNodes.append(pluto)
		else:
			path=path+'/'+root['id']
			if 'annotations' in root:
				annotations=root['annotations']
				if 'XSD label' in annotations:
					annotations['XSD label']=annotations['XSD label'].strip()
			else:
				annotations='Not mapped'			
			pluto=Node(root['id'],path,root['min'],root['max'],annotations)
			listofNodes.append(pluto)
#		print(path)
		for ch in root['children']:
			findleaf(ch,path,listofleafs,listofnoleafsannotated,comp,listofNodes)
	else:
		#add to listofleafs
		path=path+"/"+root["id"]
#		print(path)
		#logging.debug(root['id'],root['rmType'])
		if 'inputs' in root:
			inputs=root['inputs']
		else:
			inputs=[]
		if 'annotations' in root:
			annotations=root['annotations']
			if 'XSD label' in annotations:
				annotations['XSD label']=annotations['XSD label'].strip()
		else:
			annotations='Not mapped'

		if 'name' not in root:
			root['name']=root['id']
			logging.debug(f"added {root['name']} that was missing")

		pippo=Leaf(root['id'],root['name'],path,   \
				root['rmType'],root['min'],root['max'], \
				inputs,comp,annotations)
		pluto=Node(root['id'],path+'/'+root['id'],root['min'],root['max'],annotations,pippo)
		listofleafs.append(pippo)
		listofNodes.append(pluto)
		#print("ARGH")
		#print(len(listofleafs))
		#print(listofleafs[len(listofleafs)-1].get_rmtype())
		#print("HGRA")
		return

if __name__ == '__main__':
    main()





	
