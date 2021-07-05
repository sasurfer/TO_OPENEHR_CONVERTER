#!/usr/bin/python3
'''rm classes definition'''

class RM_CLASS_ONE():
	def __init__(self,name,value):
		self.name=name
		self.value=value

	def get_name(self):
		return self.name

	def get_value(self):
		return self.value

	def get_path(self):
		return {self.name:self.value}


class RM_CLASS_MULTI():
	def __init__(self,name,values):
		self.name=name
		self.values=values

	def get_name(self):
		return self.name

	def get_value(self):
		return self.values

	def get_path(self):
		return {self.name:self.values}


class DV_DURATION(RM_CLASS_ONE):
	def __init__(self,name,duration):
		super().__init__(name,duration)

class DV_DATE_TIME(RM_CLASS_ONE):
	def __init__(self,name,datetime):
		super().__init__(name,datetime)

class DV_DATE(RM_CLASS_ONE):
	def __init__(self,name,date):
		super().__init__(name,date)

class DV_TEXT(RM_CLASS_ONE):
	def __init__(self,name,text):
		super().__init__(name,text)

class DV_CODED_TEXT(RM_CLASS_MULTI):
	'''common parameters are code, value, terminology'''
	def __init__(self,name,codedtext):
		super().__init__(name,codedtext)

class CODE_PHRASE(RM_CLASS_MULTI):
	'''common parameters are code,terminology'''
	def __init__(self,name,codephrase):
		super().__init__(name,codephrase)

class PARTY_PROXY(RM_CLASS_MULTI):
	'''common parameters are id,id_scheme,id_namespace,name'''
	def __init__(self,name,partyproxy):
		super().__init__(name,partyproxy)	

class DV_BOOLEAN(RM_CLASS_ONE):
	def __init__(self,name,dvboolean):
		super().__init__(name,dvboolean)

	def get_path(self):
#		print(f'BOOLEAN {self.value}')
		if(self.value=="FALSE" or self.value=="false" or self.value=="False"):
			self.value=False
		elif(self.value=="TRUE" or self.value=="true" or self.value=="True"):
			self.value=True
		else:
			logging.debug(f'Boolean value not understood {self.value}')
#		print ({self.name:self.value})
		return {self.name:self.value}


class DV_IDENTIFIER(RM_CLASS_MULTI):
	'''common parameters are id,issuer,assigner,types'''
	def __init__(self,name,dvidentifier):
		super().__init__(name,dvidentifier)	
	
class ISM_TRANSITION(RM_CLASS_MULTI):
	'''common parameters are current_value (coded text), transition, careflow_step, reason'''
	def __init__(self,name,ism):
		super().__init__(name,ism)

def main():
	a=DV_TEXT('testname','testvalue')
	print(a.get_path())

	b=DV_CODED_TEXT('testname',{code:'mycode',value:'myvalue',terminology:'myterminology'})
	print (b.get_path())



if __name__ == '__main__':
    main()


