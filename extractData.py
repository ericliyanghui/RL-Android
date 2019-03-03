# -*- encoding:utf-8 -*-
import os
## decompress apk()
benignPath="/home/lxiao/metaQNN-Android/benignSamples"
malwarePath="/home/lxiao/metaQNN-Android/malwareSamples"
benignTmp="/home/lxiao/metaQNN-Android/benignDecompress"
malwareTmp="/home/lxiao/metaQNN-Android/malwareDecompress"

def decompress():
	global benignPath,malwarePath,benignTmp,malwareTmp
	for root,dirs,fnames in os.walk(benignPath):     #benign decompress
		for fname in fnames:
			decompile(fname,"benign")

	# for root,dirs,fnames in os.walk(malwarePath):    #malware decompress
	# 	for fname in fnames:
	# 		decompile(fname,"malware")


def decompile(fname,type):
	global benignPath,malwarePath,benignTmp,malwareTmp
	if(type=="benign"):
		fullPath=os.path.join(benignPath,fname)
		decompressPath=os.path.join(benignTmp,fname)
		apkIt="apktool d "+fullPath+" -f -o "+decompressPath
		# print(apkIt)       
		os.system(apkIt)    #not all file can be decoded
	elif(type=="malware"):
		fullPath=os.path.join(malwarePath,fname)
		decompressPath=os.path.join(malwareTmp,fname)
		apkIt="apktool d "+fullPath+" -f -o "+decompressPath
		# print(apkIt)     
		os.system(apkIt)   
	else:
		raise Exception("Invalid type")

if __name__=="__main__":
	decompress()