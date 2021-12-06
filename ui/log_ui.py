# -*- coding: utf-8 -*-
#==========================================================================
# Build log monitor
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================


#==========================================================================
# IMPORTS
#==========================================================================
import wx
import sys
from pubsub import pub

#==========================================================================
# REDIRCT COMMAND
#==========================================================================

class RedirectText(object):

    def __init__(self,aWxTextCtrl):
        """ Redirect command prompt to the log panel """
        self.out = aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class LogUI ( wx.Panel ):

    def __init__( self, parent ):
        """ Log panel """
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, style = wx.TAB_TRAVERSAL )
        log_Sizer = wx.BoxSizer( wx.HORIZONTAL )

        self.prompt_txt = wx.TextCtrl( self, -1, u"", style = wx.TE_MULTILINE)
        self.Font(self.prompt_txt, 12 )

        log_Sizer.Add( self.prompt_txt, 1, wx.EXPAND )

        self.SetSizer( log_Sizer )
        self.Layout()
        redir = RedirectText(self.prompt_txt)
        sys.stdout = redir

    def Font(self, parent, size):
        parent.SetFont( wx.Font( size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False) )
        parent.SetForegroundColour( "#FFFF")
        parent.SetBackgroundColour( "#0000" )
        return parent

class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="  Log  ")
        self.panel = LogUI(self)
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()


