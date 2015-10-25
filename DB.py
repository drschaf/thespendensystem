import os

class DB(object):
	def __init__(self, dbfolder):
		self.folder = dbfolder
		if not os.path.exists(dbfolder):
			os.makedirs(dbfolder)
			
	# get content of file with name [theID].txt or False
	def get(self, theID):
		f = "%s/%s.txt" % (self.folder, theID)
		try:
			fhandle = open(f)
			return fhandle.read()
			fhandle.close()
		except:
			return False
			
	# write content to [theID].txt
	def write(self, theID, text):
		f = "%s/%s.txt" % (self.folder, theID)
		try:
			fhandle = open(f, "w")
			fhandle.write(text)
			fhandle.close()
			return True
		except:
			return False
			
	# get a list of IDs
	def getIDs(self):
		L = []
		for F in os.listdir(self.folder):
			if F[-4:] == ".txt":
				L.append(F[0:-4])
		return L
	
	# delete a file by ID
	def delete(self, theID):
		f = "%s/%s.txt" % (self.folder, theID)
		try:
			os.remove(f)
			return True
		except:
			return False
			
	# get absolute path of DB folder
	def getPath(self):
		return os.path.abspath(self.folder)
