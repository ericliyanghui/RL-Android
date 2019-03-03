import xml.sax
import json
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

# main()
# addPermission()
readDict()
#