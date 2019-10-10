indent = 1
tabs = '\t' * indent	
from binascii import hexlify as hx, unhexlify as uhx
import Print
import os

def striplines(textfile,number=1,counter=False):
	#print(textfile)
	number=int(number)
	filelist=list()
	c=0;i=0
	with open(textfile,'r', encoding='utf8') as f:
		for line in f:		
			if i>(number-1):
				fp=line.strip()
				filelist.append(fp)	
				c+=1	
			else:
				i+=1	

	with open(textfile,"w", encoding='utf8') as f:
		for ln in filelist:
			f.write(ln+'\n')
	if counter == True:
		print('...................................................')
		print('STILL '+str(c)+' FILES TO PROCESS')
		print('...................................................')
			
def counter(textfile):
	counter=0
	with open(textfile,'r', encoding='utf8') as f:
		for line in f:
			counter+=1	
	return counter

def printcurrent(textfile,number=1,counter=False):
	currentline=''
	with open(textfile,'r', encoding='utf8') as f:
		i=0
		for line in f:
			print(line)
			break
			
def read_lines_to_list(textfile,number=1,all=False):
	#print(textfile)
	number=int(number)
	filelist=list()
	i=0
	if all==False:
		with open(textfile,'r', encoding='utf8') as f:
			for line in f:		
				if i>(number-1):
					break
				else:
					fp=line.strip()
					filelist.append(fp)					
					i+=1
	else:
			for line in f:			
				fp=line.strip()	
				filelist.append(fp)		
	return 	filelist		

def parsetags(filepath):	
	fileid='unknown';fileversion='unknown';cctag='unknown';nG=0;nU=0;nD=0;
	tid1=list()
	tid2=list()
	tid1=[pos for pos, char in enumerate(filepath) if char == '[']
	tid2=[pos for pos, char in enumerate(filepath) if char == ']']
	if len(tid1)>=len(tid2):
		lentlist=len(tid1)					
	elif len(tid1)<len(tid2):
		lentlist=len(tid2)						
	for i in range(lentlist):	
		try:
			i1=tid1[i]+1
			i2=tid2[i]					
			t=filepath[i1:i2]
			#print(t)
			if len(t)==16: 
				try:
					test1=filepath[i1:i2]
					int(filepath[i1:i2], 16)
					fileid=str(filepath[i1:i2]).upper()
					if fileid !='unknown':
						if int(fileid[-3:])==800:
							cctag='UPD'
							baseid=str(fileid[:-3])+'000'
						elif int(fileid[-3:])==000:
							cctag='BASE'
							baseid=str(fileid)
						else:
							try:
								int(fileid[-3:])
								cctag='DLC'											
							except:pass
						break
				except:
					try:
						fileid=str(filepath[i1:i2]).upper()
						if str(fileid[-3:])!='800' or str(fileid[-3:])!='000':
							DLCnumb=str(fileid)
							DLCnumb="0000000000000"+DLCnumb[-3:]									
							DLCnumb=bytes.fromhex(DLCnumb)
							DLCnumb=str(int.from_bytes(DLCnumb, byteorder='big'))									
							DLCnumb=int(DLCnumb)
							cctag='DLC'
					except:continue
		except:pass	
	if cctag=='DLC':
		baseid=str(fileid)
		token=int(hx(bytes.fromhex('0'+baseid[-4:-3])),16)-int('1',16)
		token=str(hex(token))[-1]
		token=token.upper()
		baseid=baseid[:-4]+token+'000'				
	for i in range(lentlist):	
		try:
			i1=tid1[i]+1
			i2=tid2[i]
		except:pass									
		if (str(filepath[(i1)]).upper())=='V':
			try:
				test2=filepath[(i1+1):i2]
				fileversion=int(filepath[(i1+1):i2])
				if fileversion !='unknown':
					break
			except:
				continue
	if fileversion == 'unknown':
		fileversion=0
	if fileid !='unknown':
		tid1=list()
		tid2=list()
		tid1=[pos for pos, char in enumerate(filepath) if char == '(']
		tid2=[pos for pos, char in enumerate(filepath) if char == ')']
		if len(tid1)>=len(tid2):
			lentlist=len(tid1)					
		elif len(tid1)<len(tid2):
			lentlist=len(tid2)				
		for i in range(lentlist):	
			try:
				i1=tid1[i]
				i2=tid2[i]+1					
				t=filepath[i1:i2]
				#print(t)
				if 'G+' in t or 'G)' in t:
					x_= t.find('G')-1
					nG=t[x_]
					for i in range(len(t)):
						try:
							index=x_-i
							test=t[index:x_]
							int(test)
							nG=test
						except:pass	
				else:
					nG=1
				if 'U+' in t or 'U)' in t:					
					y_= t.find('U')-1
					nU=t[y_]
					for i in range(len(t)):
						try:
							index=y_-i
							test=t[index:y_]
							int(test)
							nU=test
						except:pass						
				if 'D)' in t:			
					z_= t.find('D')-1
					nD=t[z_]	
					for i in range(len(t)):
						try:
							index=z_-i
							test=t[index:z_]
							int(test)
							nD=test
						except:pass							
			except:pass		
		# if int(nG)>0 or int(nU)>0 or int(nD)>0:
			# print(fileid+' '+str(fileversion)+' '+cctag+' '+str(nG)+'G+'+str(nU)+'U+'+str(nD)+'D')			
		# else:
			# print(fileid+' '+str(fileversion)+' '+cctag)		
	return str(fileid),str(fileversion),cctag,int(nG),int(nU),int(nD),baseid
	
def folder_to_list(ifolder,extlist=['nsp'],filter=False):	
	ruta=ifolder
	filelist=list()
	try:
		fname=""
		binbin='RECYCLE.BIN'
		for ext in extlist:
			#print (ext)
			if os.path.isdir(ruta):
				for dirpath, dirnames, filenames in os.walk(ruta):
					for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
						fname=""
						if filter != False:
							if filter.lower() in filename.lower():
								fname=filename
						else:
							fname=filename
						if fname != "":
							if binbin.lower() not in filename.lower():
								filelist.append(os.path.join(dirpath, filename))
			else:
				if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
					filename = ruta
					fname=""
					if filter != False:
						if filter.lower() in filename.lower():
							fname=filename
					else:
						fname=filename
					if fname != "":
						if binbin.lower() not in filename.lower():
							filelist.append(filename)
	except BaseException as e:
		Print.error('Exception: ' + str(e))													
	return filelist