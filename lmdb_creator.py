import numpy as np
import lmdb
import caffe
import metadata
import argparse
import os
import pickle

def create_record(X,y,path,save_as_float=False):
	assert(X.shape[0]==y.shape[0])

	malwareDecompiledPath="/home/lxiao/metaQNN-Android/malwareDecompress"
	malwareN=len(os.listdir(malwareDecompiledPath)) 

	benignDecompiledPath="/home/lxiao/metaQNN-Android/benignDecompress"
	benignN=len(os.listdir(benignDecompiledPath)) 

	N=X.shape[0]  #data size
	fN=metadata.perNum  #feature size
	m=1;n=1  #height and width

	map_size=X.nbytes*50  #dataset size????

	env=lmdb.open(path,map_size=map_size)


	with env.begin(write=True) as txn:
		for i in range(N):
			datum=caffe.proto.caffe_pb2.Datum()
			datum.channels=fN
			datum.height=m
			datum.width=n
			if save_as_float:
				datum.float_data.extend(X[i].astype(float).flat)
			else:
				datum.data=X[i].tobytes()
			datum.label=int(y[i])
			str_id='{:08}'.format(i)   #total 10^8

			txn.put(str_id.encode('ascii'),datum.SerializeToString())

def shuffle(X,y):
	assert X.shape[0] == y.shape[0]
	new_index=np.random.permutation(np.arange(X.shape[0]))
	return X[new_index,:,:,:],y[new_index]

def create_records(Xtr,
				   Ytr,
				   Xte,
				   Yte,      
				   root_path,
				   save_as_float=False):

	print('Labels train',np.unique(Ytr))   #find unique elements for Ytr
	print('Labels test',np.unique(Yte))

	if save_as_float:
		print('Converting to Float')
		Xtr=Xtr.astype(float)
		Ytr=Ytr.astype(float)
		Xte=Xte.astype(float)
		Yte=Yte.astype(float)

	Xtr, Ytr= shuffle(Xtr,Ytr)  #mix Xtr,Ytr
	Xte, Yte= shuffle(Xte,Yte)  #mix Xtr,Ytr

	print 'Train x shape',Xtr.shape, Xtr.dtype
	print 'Train y shape',Ytr.shape, Ytr.dtype
	print 'Test x shape',Xte.shape, Xte.dtype
	print 'Test y shape',Yte.shape, Yte.dtype

	create_record(Xtr,Ytr,os.path.join(root_path,'train_full.lmdb'),save_as_float=save_as_float)
	create_record(Xte,Yte,os.path.join(root_path,'test.lmdb'),save_as_float=save_as_float)

def load_batch(filename):
	with open(filename,'rb') as f:
		datadict=pickle.load(f)
		X=datadict["data"]
		Y=datadict["label"]
		X=np.array(X).reshape(Y.shape[0],metadata.perNum,1,1).astype(np.uint8)
		Y=np.array(Y,dtype=np.int64)
		return X,Y

def get_datasets(save_dir=None, root_path=None):
	Xtr, Ytr=load_batch(os.path.join(root_path,"train"))
	Xte, Yte=load_batch(os.path.join(root_path,"test"))
	
	return Xtr, Ytr, Xte, Yte


def main():
	parser=argparse.ArgumentParser()
	parser.add_argument('root_save_dir')  #data save directory
	parser.add_argument('-odd', '--original_data_dir')    #original data directory

	args=parser.parse_args()
	if not os.path.isdir(args.root_save_dir):
		os.makedirs(args.root_save_dir)

	if args.original_data_dir and not os.path.isdir(args.original_data_dir):
		print 'ERROR: original data dir not real directory'
		return

    # Should we save as float?
	save_as_float = False

    #Convert to absolute paths
	root_save_dir=os.path.abspath(args.root_save_dir)
	print(root_save_dir)
	root_path=os.path.abspath(args.original_data_dir) if args.original_data_dir else none

    #Data Process
	Xtr, Ytr, Xte, Yte = get_datasets(save_dir=root_save_dir,   
    								  root_path=root_path)
    
	create_records(Xtr=Xtr,
    			   Ytr=Ytr,
    			   Xte=Xte,
    			   Yte=Yte,
    			   root_path=root_save_dir,
    			   save_as_float=save_as_float)

if __name__=="__main__":
	main()





