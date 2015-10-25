import wx
import subprocess
from DB import DB
from math import ceil

class Frontend(wx.Frame):
	def __init__(self, parent, fastbuttons, Ls, language='DE'):

		self.db = DB('DB')
		self.fastbuttonlabels = fastbuttons
		self.Ls = Ls
		self.currentID = ""
		self.textobjects = {}

		super(Frontend, self).__init__(parent, size=(800,600))
		self.Centre()

		panel = wx.Panel(self)

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(14)

		# "all-in-one-box"
		vbox = wx.BoxSizer(wx.VERTICAL)

		# ID box: ID label, text input, buttons
		idbox = wx.BoxSizer(wx.HORIZONTAL)
		
		self.idinput = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
		self.idinput.SetFont(font)
		self.idinput.Bind(wx.EVT_TEXT_ENTER, self.search)
		self.idinput.Bind(wx.EVT_SET_FOCUS, self.textfocus)
		idbox.Add(self.idinput, proportion=1)

		restore = wx.Button(panel, label="<", size=(30,-1))
		restore.SetFont(font)
		restore.Bind(wx.EVT_BUTTON, self.restore)
		idbox.Add(restore)
		
		idsearch = wx.Button(panel)
		idsearch.SetFont(font)
		idsearch.Bind(wx.EVT_BUTTON, self.search)
		idbox.Add(idsearch)
		self.textobjects['load'] = idsearch
				
		vbox.Add(idbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
			border=10)

		# TEXT box: "Text" label, text area, grid for "fast-add" buttons
		textbox = wx.BoxSizer(wx.VERTICAL)

		inputsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.textinput = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
		self.textinput.SetFont(font)
		inputsizer.Add(self.textinput, proportion=1, flag=wx.EXPAND)
		
		# grid for "fast-add" buttons
		# 3 columns, ceil(n/3) rows, +2 for spacer and save/del/browse
		gridCols = 3
		gridRows = 2+int(ceil(float(len(self.fastbuttonlabels))/gridCols))
		buttongrid = wx.GridSizer(gridRows, gridCols)
		self.fastbuttons = []
		i=0
		for x in xrange(gridCols):
			for y in xrange(gridRows-2):
				try:
					l = self.fastbuttonlabels[i]
					b = wx.Button(panel, label=l, size=(120,70));
					b.Bind(wx.EVT_BUTTON, self.fastButtonAction)
					b.SetFont(font)
					self.fastbuttons.append(b)
					buttongrid.Add(b)
				except:
					# fill with spacers if n%3 > 0
					buttongrid.Add((-1,-1))		
				i += 1		
				
		for x in xrange(gridCols):
			buttongrid.Add((-1,-1))

		savebtn = wx.Button(panel, size=(120,70))
		savebtn.Bind(wx.EVT_BUTTON, self.save)
		savebtn.SetBackgroundColour("#CCFFCC")
		savebtn.SetFont(font)
		buttongrid.Add(savebtn, flag=wx.LEFT | wx.RIGHT)
		self.textobjects['save'] = savebtn

		rembtn = wx.Button(panel, size=(120,70))
		rembtn.Bind(wx.EVT_BUTTON, self.remove)
		rembtn.SetBackgroundColour("#FFCCCC")
		rembtn.SetFont(font)
		buttongrid.Add(rembtn, flag=wx.LEFT | wx.RIGHT)
		self.textobjects['delete'] = rembtn

		dbbtn = wx.Button(panel, size=(120,70))
		dbbtn.Bind(wx.EVT_BUTTON, self.openDBfolder)
		dbbtn.SetBackgroundColour("#FFEECC")
		dbbtn.SetFont(font)
		buttongrid.Add(dbbtn, flag=wx.LEFT | wx.RIGHT)
		self.textobjects['browse'] = dbbtn

		inputsizer.Add(buttongrid, proportion=0, flag=wx.RIGHT)		
		textbox.Add(inputsizer, proportion=1, flag=wx.EXPAND)
		
		vbox.Add(textbox, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)
		
		# LANGUAGE box: language buttons
		langbox = wx.BoxSizer(wx.HORIZONTAL)
		self.langbuttons = []
		for key in Ls:
			b = wx.Button(panel, label=key, size=(40,40))
			b.SetFont(font)
			b.Bind(wx.EVT_BUTTON, self._setLanguage)
			langbox.Add(b)
		
		vbox.Add(langbox, proportion=0, flag=wx.LEFT, border=10)
		vbox.Add((-1,10));

		panel.SetSizer(vbox)

		self.setLanguage(language)
		self.idinput.SetFocus()
		self.Show()


	# set button labels
	def setLanguage(self, lan):
		self.L = self.Ls[lan]
		self.SetTitle(self.L['title'])
		for i in self.L:
			try:
				self.textobjects[i].SetLabel(self.L[i])
			except KeyError:
				# for language keywords without matching object (like
				# dialog texts)
				pass

	#  --- button handlers ---

	# language buttons
	def _setLanguage(self, E):
		newlan = E.EventObject.GetLabelText()
		self.setLanguage(newlan)
		self.idinput.SetFocus()

	# load button
	def search(self, E):
		oldID = self.currentID
		if not oldID == "":
			text = self.textinput.GetValue()
			self.db.write(oldID, text)

		theID = self.idinput.GetValue()
		if theID == "":
			wx.MessageBox(self.L['invalid_id'], "", wx.OK | wx.ICON_EXCLAMATION)
			self.idinput.SetValue(self.currentID)
			self.idinput.SetFocus()
			return False
			
		t = self.db.get(theID)
		if t == False:
			wx.MessageBox(self.L['notfound'], theID, wx.OK | wx.ICON_EXCLAMATION)
			self.textinput.SetValue("")
		else:
			self.textinput.SetValue(t)
		
		self.currentID = theID
		self.idinput.SetFocus()
		self.idinput.SelectAll()
		
	# restore button
	def restore(self, E):
		self.idinput.SetValue(self.currentID)
		self.idinput.SetFocus()
								
	# called when idinputbox is focussed
	def textfocus(self, E):
		self.textinput.SelectAll()
		
	# save button
	def save(self, E):
		theID = self.currentID
		if theID == "":
			self.idinput.SetFocus()
			return False
			
		text = self.textinput.GetValue()
		
		if self.db.write(theID, text):
			wx.MessageBox(self.L['saved'], theID, wx.OK | wx.ICON_INFORMATION)
		else:
			wx.MessageBox(self.L['notsaved'], theID, wx.OK | wx.ERROR)
		
		self.idinput.SetFocus()
		
	# "fast-add" buttons
	def fastButtonAction(self, E):
		t = E.EventObject.GetLabelText()
		self.textinput.AppendText(t+"\n")
		
		self.idinput.SetFocus()

	# remove button
	def remove(self, E):
		theID = self.currentID
		if theID == "":
			self.idinput.SetFocus()
			return False

		if wx.YES == wx.MessageBox(self.L['del_confirm'], theID, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION):
			self.db.delete(theID)
			self.textinput.SetValue("")
			self.idinput.SetValue("")
			self.currentID = ""

		self.idinput.SetFocus()

	# browse button
	def openDBfolder(self, E):
		subprocess.Popen(['xdg-open', self.db.getPath()])
		self.idinput.SetFocus()
