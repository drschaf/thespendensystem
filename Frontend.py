import wx
import subprocess
from DB import DB
from math import ceil

class Frontend(wx.Frame):
	def __init__(self, parent, fastbuttons, L):
		super(Frontend, self).__init__(parent, title=L['title'], size=(800,600))
		self.Centre()

		self.db = DB('DB')
		self.fastbuttonlabels = fastbuttons
		self.L = L
		self.currentID = ""

		panel = wx.Panel(self)

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(14)

		vbox = wx.BoxSizer(wx.VERTICAL)

		idbox = wx.BoxSizer(wx.HORIZONTAL)
		idtext = wx.StaticText(panel, label='ID:')
		idtext.Bind(wx.EVT_TEXT_ENTER, self.search)
		idtext.Bind(wx.EVT_SET_FOCUS, self.textfocus)
		idtext.SetFont(font)
		idbox.Add(idtext, flag=wx.RIGHT, border=8)
		
		self.idinput = wx.TextCtrl(panel)
		self.idinput.SetFont(font)
		idbox.Add(self.idinput, proportion=1)
		
		idsearch = wx.Button(panel, label=L['load'])
		idsearch.SetFont(font)
		idsearch.Bind(wx.EVT_BUTTON, self.search)
		idbox.Add(idsearch)
		
		vbox.Add(idbox, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

		textbox = wx.BoxSizer(wx.VERTICAL)
		texttext = wx.StaticText(panel, label='Text:')
		texttext.SetFont(font)
		textbox.Add(texttext)

		inputsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.textinput = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
		self.textinput.SetFont(font)
		inputsizer.Add(self.textinput, proportion=1, flag=wx.EXPAND)
		
		gridCols = 3
		gridRows = 2+int(ceil(float(len(self.fastbuttonlabels))/gridCols))
		buttongrid = wx.GridSizer(gridRows, gridCols)
		self.fastbuttons = []
		i=0
		for x in xrange(gridCols):
			for y in xrange(gridRows-2):
				try:
					l = self.fastbuttonlabels[i]
					b = wx.Button(panel, label=l, size=(100,50));
					b.Bind(wx.EVT_BUTTON, self.fastButtonAction)
					b.SetFont(font)
					self.fastbuttons.append(b)
					buttongrid.Add(b)
					
				except:
					buttongrid.Add((-1,-1))				
				
				i += 1
				
		for x in xrange(gridCols):
			buttongrid.Add((-1,5))

		savebtn = wx.Button(panel, label=L['save'], size=(100,50))
		savebtn.Bind(wx.EVT_BUTTON, self.save)
		savebtn.SetBackgroundColour("#CCFFCC")
		buttongrid.Add(savebtn, flag=wx.LEFT | wx.RIGHT)

		rembtn = wx.Button(panel, label=L['delete'], size=(100,50))
		rembtn.Bind(wx.EVT_BUTTON, self.remove)
		rembtn.SetBackgroundColour("#FFCCCC")
		buttongrid.Add(rembtn, flag=wx.LEFT | wx.RIGHT)

		dbbtn = wx.Button(panel, label=L['browse'], size=(100,50))
		dbbtn.Bind(wx.EVT_BUTTON, self.openDBfolder)
		dbbtn.SetBackgroundColour("#FFEECC")
		buttongrid.Add(dbbtn, flag=wx.LEFT | wx.RIGHT)

		inputsizer.Add(buttongrid, proportion=0, flag=wx.RIGHT)		
		textbox.Add(inputsizer, proportion=1, flag=wx.EXPAND)
		
		vbox.Add(textbox, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)
		
		vbox.Add((-1,10));

		panel.SetSizer(vbox)

		self.idinput.SetFocus()
		self.Show()


	#  --- button handlers ---

	# load button
	def search(self, E):
		oldID = self.currentID
		if not oldID == "":
			text = self.textinput.GetValue()
			self.db.write(oldID, text)

		theID = self.idinput.GetValue()
		if theID == "":
			wx.MessageBox(self.L['invalid_id'], "", wx.OK | wx.ICON_EXCLAMATION)
			return False
			
		t = self.db.get(theID)
		if t == False:
			wx.MessageBox(self.L['notfound'], theID, wx.OK | wx.ICON_EXCLAMATION)
			self.textinput.SetValue("")
		else:
			self.textinput.SetValue(t)
		
		self.currentID = theID
		self.idinput.SetFocus()
				
				
	# called when idinputbox is focussed
	def textfocus(self, E):
		self.textinput.SelectAll()
		
	# save button
	def save(self, E):
		theID = self.currentID
		if theID == False:
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
		if theID == False:
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
