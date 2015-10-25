#!/usr/bin/python
from Frontend import Frontend
import wx

fastbuttons = ['Schuhe', 'Jacke', 'Pullover', 'Socken', 'Unterhosen']
L = {
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

app = wx.App()
Frontend(None, fastbuttons, L)
app.MainLoop()
