# -*- coding: utf-8 -*-
#==========================================================================
# Build report monitor
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import wx
from pubsub import pub

#==========================================================================
# MAIN PROGRAM
#==========================================================================
class ReportUI ( wx.Panel ):

    def __init__( self, parent ):
        """ Serial panel """
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        wx.Panel.__init__ ( self, parent, -1, pos = wx.DefaultPosition, size = (framew*0.142 ,-1) ,style = wx.TAB_TRAVERSAL )
        self.BuildPanel()

    def BuildPanel(self):
        self.report_txt = wx.TextCtrl( self, -1, style = wx.TE_MULTILINE)
        self.Font(self.report_txt, 12)

        serial_Sizer = wx.BoxSizer( wx.VERTICAL )
        serial_Sizer.Add( self.report_txt, 1, wx.EXPAND )
        self.SetSizer( serial_Sizer )
        self.Layout()

    def Font(self, parent, size):
        parent.SetFont( wx.Font( size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False) )
        parent.SetForegroundColour( "#FFFF")
        parent.SetBackgroundColour( "#0000" )
        return parent


class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="  Report  ")
        self.panel = ReportUI(self)
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
