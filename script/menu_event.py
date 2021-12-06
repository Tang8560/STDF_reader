# -*- coding: utf-8 -*-
#==========================================================================
# Create menubar event handle
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import os
import wx
import sys
import threading
from pubsub  import pub
from pathlib import Path
#==========================================================================
# PATH
#==========================================================================
root = str(Path(__file__).parents[1])

#==========================================================================
# PUB SENDMESSAGE
#==========================================================================
MENU_FILE    = "MENU_FILE"
MENU_SAVE    = "MENU_SAVE"
MENU_QUIT    = "MENU_QUIT"
MENU_SETTING = "MENU_SETTING"
MENU_CSV     = "MENU_CSV"
MENU_MAP     = "MENU_MAP"
MENU_PARSE   = "MENU_PARSE"

UNSUB = [MENU_FILE, MENU_SAVE, MENU_SETTING, MENU_CSV, MENU_MAP, MENU_PARSE ]

#==========================================================================
# MAIN PROGRAM
#==========================================================================
class MenuEvent(object):

    def __init__(self, parent):
        self.parent = parent

    def file_event(self, event):
        """ Open file """
        try:
            filepath = wx.FileDialog(self.parent, u"Open file", wildcard="XLXS files (*.xlsx)|*.xlsx",style = wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
            if filepath.ShowModal() == wx.ID_OK:
                self.file_path = filepath.GetPath()
                print("[INFO] Open file: " + os.path.basename(self.file_path))
                filepath.Destroy()
                pub.sendMessage(MENU_FILE, file_path = self.file_path)
        except Exception as e:
            self.traceback(e)

    def save_event(self, event):
        """ Save file """
        try:
            filepath = wx.FileDialog(self.parent, u"Save file",wildcard="CSV files (*.csv)|*.csv",style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_NO_FOLLOW)
            if filepath.ShowModal() == wx.ID_OK:
                self.save_path = filepath.GetPath()
                print("[INFO] Save the file: " + os.path.basename(self.save_path))
                filepath.Destroy()
                pub.sendMessage(MENU_SAVE, save_path = self.save_path)
        except Exception as e:
            self.traceback(e)

    def quit_event(self, event):
        """ Menubar quit """
        try:
            dlg = wx.MessageDialog(None,u"Are you sure you want to close the window?",u"Confirm close",wx.YES_NO)
            if dlg.ShowModal()==wx.ID_YES:
                for i in UNSUB:
                    try: pub.unsubAll(i)
                    except: pass
                event.Skip()
                print("[INFO] Exit the program")
                pub.sendMessage(MENU_QUIT)
                self.parent.Close()
        except Exception as e:
            self.traceback(e)

    def setting_event(self, event):
        pub.sendMessage(MENU_SETTING, setting = event)

    def csv_event(self, event):
        pub.sendMessage(MENU_CSV, csv = event)

    def map_event(self, event):
        pub.sendMessage(MENU_MAP, map = event)

    def parse_event(self, event):
        try:
            filepath = wx.FileDialog(self.parent, u"Open file", wildcard="STDF files (*.stdf)|*.stdf",style = wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
            if filepath.ShowModal() == wx.ID_OK:
                self.file_path = filepath.GetPath()
                print("[INFO] Open file: " + os.path.basename(self.file_path))
                filepath.Destroy()
                pub.sendMessage(MENU_PARSE, parse_path = self.file_path)
        except Exception as e:
            self.traceback(e)

    def about_event(self, event):
        os.startfile(root+'\\script\\STDF_spec.pdf')

    def traceback(self, error):
        """ Error handling """
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,'line '+ str(traceback.tb_lineno))

