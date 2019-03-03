import xml.sax
import json
import extractFeature as ef
# import test1 as t1
# from test1 import tt
class ManifestHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.perList=[]

	def startElement(self,tag,attributes):
		if tag=="uses-permission":
			self.perList.append(attributes["android:name"])

	def endElement(self,tag):
		pass
	#content solver
	def characters(self,content):
		pass

## parse specificed xml
def parseXml():
	parser=xml.sax.make_parser()

	parser.setFeature(xml.sax.handler.feature_namespaces,0)

	Handler=ManifestHandler()
	parser.setContentHandler(Handler)

	parser.parse("./AndroidManifest.xml")

	return Handler
	# print(Handler.perList)

## extend to full permission and create dictionary
def addPermission():
	f1=open("/home/lxiao/metaQNN-Android/permissionList/permissionList-API28-pure.txt",'r')
	f2=open("/home/lxiao/metaQNN-Android/permissionList/permissionList-API28-pure-full.txt",'w+')
	f3=open("/home/lxiao/metaQNN-Android/permissionList/permissionList-API28-pure-dict.txt",'w+')
	cnt=0
	f2.truncate()
	perDict={}
	perList=[]
	line=f1.readline()
	while line:
		# print(line)
		line="android.permission."+line
		perDict[line[:-2]]=cnt
		# perList.append(line)
		f2.write(line)   
		cnt+=1
		line=f1.readline()
	# return perDict
	f3.write(str(perDict))
	f1.close();f2.close();f3.close()

## create feature vector as nn input
def createFeature(handler,perDict):
	perList=handler.perList
	size=93   #android permission size
	nnInput=[0]*size
	for per in perList:
		if(perDict.has_key(per)):
			nnInput[perDict[per]]=1
	print(nnInput)

def readDict():
	f3=open("/home/lxiao/metaQNN-Android/permissionList/permissionList-API28-pure-dict.txt",'r+')
	perDict=eval(f3.read())
	print(perDict)
	print(perDict["android.permission.ADD_VOICEMAIL"])
	f3.close()

def main():
	addPermission()

	handler=parseXml()
	createFeature(handler,perDict)

def judge():
	f3=open("/home/lxiao/metaQNN-Android/blank.txt",'r+')
	print(f3.read())
	if(not len(f3.read())):
		print("Blank")
	# tt()

def pickleTest():
	import pickle
	data1 = {'a': [1, 2.0, 3, 4+6j],
		 'b': ('string', u'Unicode string'),
		 'c': None}

	selfref_list = [1, 2, 3]
	selfref_list.append(selfref_list)

	output = open('data', 'wb')

	# Pickle dictionary using protocol 0.
	pickle.dump(data1, output)

	# Pickle the list using the highest protocol available.
	pickle.dump(selfref_list, output, -1)

	output.close()	

def pathTest():
	import metadata
	print(metadata.benignNum)

# main()
# addPermission()
# readDict()
# judge()
# pickleTest()
pathTest()

