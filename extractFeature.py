import os
import xml.sax
import numpy as np
import extractData as ed
import pickle
import metadata

## sax solver
class ManifestHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.perList=[] 

	def startElement(self,tag,attributes):
		if tag=="uses-permission":
			try:
				attributes["android:name"]
			except Exception,e:
				# print(e)
				# print(attributes["n1:name"])
				self.perList.append(attributes["n1:name"])  #for chrome
			else:
				self.perList.append(attributes["android:name"])

	def endElement(self,tag):
		pass
	#content solver
	def characters(self,content):
		pass

## parse specificed xml
def parseXml(xmlPath):
	parser=xml.sax.make_parser()

	parser.setFeature(xml.sax.handler.feature_namespaces,0)

	Handler=ManifestHandler()
	parser.setContentHandler(Handler)

	# print(xmlPath)
	parser.parse(xmlPath)

	return Handler
	# print(Handler.perList)

## create feature vector as nn input
def createFeature(handler,perDict):
	perList=handler.perList
	size=93   #android permission size
	nnInput=[0]*size
	for per in perList:
		if(perDict.has_key(per)):
			nnInput[perDict[per]]=1
	# print(nnInput)
	return nnInput

# ##	redecompile apk
# def reDecompile(fullPath):
# 	#for benign
# 	fullPath=os.path.join(benignPath,fname)
# 	decompressPath=os.path.join(benignTmp,fname)
# 	apkIt="apktool d "+fullPath+" -f -o "+decompressPath

def shuffle(X,y):   #-----!!!-----
	assert X.shape[0] == y.shape[0]
	new_index=np.random.permutation(np.arange(X.shape[0]))
	return X[new_index,:],y[new_index]
	
def main():
	print("Processing Data as NN Input...")
	fr=open("/home/lxiao/metaQNN-Android/permissionList/permissionList-API28-pure-dict.txt",'r+')
	perDict=eval(fr.read())
	     
	#search malware xml file for permission
	mdecompiledPath="/home/lxiao/metaQNN-Android/malwareDecompress"
	mdecompiledFiles=os.listdir(mdecompiledPath) 
	mapkPath="/home/lxiao/metaQNN-Android/malwareSamples"
	mapkFiles=os.listdir(mapkPath)
	print("original malware: ",len(mapkFiles))
	print("decompiled malware: ",len(mdecompiledFiles))

	nnMalwareInput=[]
	xmlMalwarePathList=[]
	for filename in mdecompiledFiles:      
		xmlPath=os.path.join(mdecompiledPath,filename,"AndroidManifest.xml")
		xmlMalwarePathList.append(xmlPath) 
		if(not os.path.isfile(xmlPath)):  #if failed to read xml, redecompile
			ed.decompile(filename,"malware")
		fr=open(xmlPath,'r+')
		if(not len(fr.read())):
			ed.decompile(filename,"malware")       
		#xml Parse
		handler=parseXml(xmlPath)
		tmpInput=createFeature(handler,perDict)
		nnMalwareInput.append(tmpInput)
	# #to numpy
	# xmlMalwarePathList=np.array(xmlMalwarePathList)
	# nnMalwareInput=np.array(nnMalwareInput)

	#search benign xml file for permission
	bdecompiledPath="/home/lxiao/metaQNN-Android/benignDecompress"
	bdecompiledFiles=os.listdir(bdecompiledPath) 
	bapkPath="/home/lxiao/metaQNN-Android/benignSamples"
	bapkFiles=os.listdir(bapkPath)
	print("original benign: ",len(bapkFiles))
	print("decompiled benign: ",len(bdecompiledFiles))


	nnBenignInput=[]
	xmlBenignPathList=[]
	for filename in bdecompiledFiles:      
		xmlPath=os.path.join(bdecompiledPath,filename,"AndroidManifest.xml")
		xmlBenignPathList.append(xmlPath) 
		if(not os.path.isfile(xmlPath)):  #if failed to read xml, redecompile
			ed.decompile(filename,"benign")
		fr=open(xmlPath,'r+')
		if(not len(fr.read())):
			ed.decompile(filename,"benign")       
		#xml Parse
		handler=parseXml(xmlPath)
		tmpInput=createFeature(handler,perDict)
		nnBenignInput.append(tmpInput)
	# # to numpy
	# xmlBenignPathList=np.array(xmlBenignPathList)
	# nnBenignInput=np.array(nnBenignInput)


	#save data
	benignInput="/home/lxiao/metaQNN-Android/nnInput/Benign"
	malwareInput="/home/lxiao/metaQNN-Android/nnInput/Malware"
	#-benign
	b1=open(os.path.join(benignInput,"xmlName"),"w+")
	b2=open(os.path.join(benignInput,"inputVector"),"w+")
	b1.write(str(xmlBenignPathList))	
	b2.write(str(nnBenignInput))
	b1.close();b2.close()
	#-malware
	b3=open(os.path.join(malwareInput,"xmlName"),"w+")
	b4=open(os.path.join(malwareInput,"inputVector"),"w+")
	b3.write(str(xmlMalwarePathList))	
	b4.write(str(nnMalwareInput))
	b3.close();b4.close()

	#combine
	trPer=0.8   #train/total percentage
	ttlLen=len(bdecompiledFiles)+len(mdecompiledFiles)
	cPath="/home/lxiao/metaQNN-Android/nnInput/total"
	#-total data
	total={}
	nnBenignInput=np.array(nnBenignInput);nnMalwareInput=np.array(nnMalwareInput)
	dataTTL=np.r_[nnBenignInput,nnMalwareInput]
	labelTTL=np.array([0]*len(bdecompiledFiles)+[1]*len(mdecompiledFiles))
	# input()
	total["data"]=dataTTL  
	total["label"]=labelTTL
	output=open(os.path.join(cPath,"total"),"wb")
	pickle.dump(total,output)

	# metadata.benignNum=len(bdecompiledFiles)    #malware and benign num
	# metadata.malwareNum=len(mdecompiledFiles)

	dataTTL,labelTTL=shuffle(dataTTL,labelTTL)    #mix data
	print("dataTTL",dataTTL.shape[0]);print("labelTTL",labelTTL.shape[0])
	trainIndex=np.arange(int(ttlLen*trPer)+1);testIndex=np.arange(int(ttlLen*trPer)+1,ttlLen)
	#-train data
	train={}
	train["data"]=dataTTL[trainIndex,:]     #-------!!-------
	train["label"]=labelTTL[trainIndex]
	output=open(os.path.join(cPath,"train"),"wb")
	pickle.dump(train,output)
	#-test data
	test={}
	test["data"]=dataTTL[testIndex,:]
	test["label"]=dataTTL[testIndex]
	output=open(os.path.join(cPath,"test"),"wb")
	pickle.dump(test,output)

if __name__=="__main__":
	main()
