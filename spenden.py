#!/usr/bin/python
from Frontend import Frontend
import wx

# "fast-add" buttons in grid on the right side
fastbuttons = [
	'Schuhe',
	'Jacke',
	'Pullover',
	'Socken',
	'Unterhosen'
	]

# language maps
L = {}
L['DE'] = {
	'title':	"Spenden",
	'load':		"Laden",
	'save':		"Speichern",
	'delete':	"Entfernen",
	'browse':	"Ordner",
	'invalid_id':	"Bitte Kennung angeben!",
	'notfound':	"Nicht gefunden, Eintrag wird neu angelegt.",
	'saved':	"Eintrag gespeichert.",
	'notsaved':	"Konnte nicht gespeichert werden!",
	'del_confirm':	"Eintrag entfernen?"
	}
	
L['EN'] = {
	'title':	"Donations",
	'load':		"load",
	'save':		"save",
	'delete':	"delete",
	'browse':	"browse",
	'invalid_id':	"Please enter an ID!",
	'notfound':	"Entry not found, will be created.",
	'saved':	"Entry saved.",
	'notsaved':	"Could not save entry!",
	'del_confirm':	"Delete entry?"
	}

app = wx.App()
Frontend(None, fastbuttons, L)
app.MainLoop()
