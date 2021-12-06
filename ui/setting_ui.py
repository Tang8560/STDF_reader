# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © Quanta Computer Inc. 
#--------------------------------------------------------------------------
# Project : MFG_v3
# File    : setting_ui.py 
#--------------------------------------------------------------------------
# Create setting Panel
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import os
import wx
from pubsub import pub
#==========================================================================
# PUB SENDMESSAGE
#==========================================================================
expand = "expand"
report = "report"
#==========================================================================
# PARAMETER
#==========================================================================
button_width  = 60
button_height = 30
fontSize      = 12
#==========================================================================
# BUTTON EVENT
#==========================================================================
class Toggle(wx.BitmapButton):
     
    def __init__(self, parent, function):
        wx.BitmapButton.__init__(self, parent, -1, style = wx.BORDER_NONE)
        self.SetBackgroundColour( "#FFFF" )
        root = os.getcwd()
        self.function = function
        openbtn  = root + "/source/button/open.png"
        closebtn = root + "/source/button/close.png"
        
        openbtn_img  = wx.Image(openbtn).Rescale(button_width, button_height)
        closebtn_img = wx.Image(closebtn).Rescale(button_width, button_height)
        self.open    = wx.Bitmap(openbtn_img , wx.BITMAP_TYPE_ANY)
        self.close   = wx.Bitmap(closebtn_img , wx.BITMAP_TYPE_ANY)  

        self.state = False
        self.SetBitmapLabel(self.close)
        self.Bind(wx.EVT_BUTTON,self.OnClick)   
        
    def OnClick(self, event):
        if self.state==True:
            self.function(self.state)
            self.state = False
            self.SetBitmapLabel(self.close)
        else:
            self.function(self.state)
            self.state = True
            self.SetBitmapLabel(self.open)
        self.Refresh()

#==========================================================================
# MAIN PROGRAM
#==========================================================================
class SettingUI( wx.Panel ): 
    def __init__( self, parent):
        wx.Panel.__init__ ( self, parent, -1, pos = wx.DefaultPosition, style = wx.TAB_TRAVERSAL )
        self.parent = parent
        self.SetBackgroundColour( "#FFFF" )
        self.BuildPanel() 
   
    def BuildPanel(self):
        self.expand      = wx.StaticText( self, -1, u"Expand All" ) 
        self.report      = wx.StaticText( self, -1, u"Report Fail/All" ) 
        self.expand_btn  = Toggle( self, self.onExpand )
        self.report_btn  = Toggle( self, self.onReport )
        self.gauge       = wx.Gauge( self, -1, 100, wx.DefaultPosition, (-1, button_height), wx.GA_HORIZONTAL )
        self.process     = wx.StaticText( self, -1, u"0% (0/92)" )
        self.button_font(self.expand , fontSize)
        self.button_font(self.report, fontSize)
        self.process_font(self.process, fontSize )

        setting_Sizer = wx.BoxSizer( wx.HORIZONTAL ) 
        setting_Sizer.Add(self.expand,     0, wx.ALL|wx.ALIGN_CENTER, 10 )
        setting_Sizer.Add(self.expand_btn, 0, wx.ALL|wx.ALIGN_CENTER, 10 )
        setting_Sizer.Add(self.report,     0, wx.ALL|wx.ALIGN_CENTER, 10 )
        setting_Sizer.Add(self.report_btn, 0, wx.ALL|wx.ALIGN_CENTER, 10 )
        setting_Sizer.Add(self.gauge,      1, wx.ALL|wx.ALIGN_CENTER, 10 )
        setting_Sizer.Add(self.process,    0, wx.ALL|wx.ALIGN_CENTER, 10 )

        self.SetSizer( setting_Sizer )
        self.Layout()  

    def button_font(self, parent, size): 
        parent.SetFont( wx.Font( size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Calibri" ) )
        return parent 

    def process_font(self, parent, size): 
        parent.SetFont( wx.Font( size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ) )
        parent.SetForegroundColour((0,0,255))
        parent.SetBackgroundColour( "#FFFF" )
        return parent

    def onExpand(self, state):
        pub.sendMessage(expand, value = not state)   
  
    def onReport(self, state):
        pub.sendMessage(report, value = not state)   


class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="Setting Panel")
        self.panel = SettingUI(self)
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()