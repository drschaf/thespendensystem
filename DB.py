import os

class DB(object):
	def __init__(self, dbfolder):
		self.folder = dbfolder
		if not os.path.exists(dbfolder):
			os.makedirs(dbfolder)
		
	def get(self, theID):
		f = "%s/%s.txt" % (self.folder, theID)
		try:
			fhandle = open(f)
			return fhandle.read()
			fhandle.close()
		except:
			return False
			
	def write(self, theID, text):
		f = "%s/%s.txt" % (self.folder, theID)
		try:
			fhandle = open(f, "w")
			fhandle.write(text)
			fhandle.close()
			return True
		except:
			return False
			
	def getIDs(self):
		L = []
		for F in os.listdir(self.folder):
			if F[-4:] == ".txt":
				L.append(F[0:-4])
		return L
		
	def delete(self, theID):
		f = "%s/%s.txt" % (self.folder, theID)
		try:
			os.remove(f)
			return True
		except:
			return False
			
	def getPath(self):
		return os.path.abspath(self.folder)
