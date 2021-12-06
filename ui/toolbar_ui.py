# -*- coding: utf-8 -*-
#==========================================================================
# Create menubar
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
import wx.lib.agw.aui as aui
from pathlib import Path

#==========================================================================
# PATH
#==========================================================================
root = str(Path(__file__).parents[1])

#==========================================================================
# IMPORTS MENU FUNCTION
#==========================================================================
try:
    from script.menu_event import MenuEvent
except:
    from script.menu_event import MenuEvent

#==========================================================================
# SETTING TOOLBAR ICON SIZE
#==========================================================================
TOOLBAR_WIDTH  = 20
TOOLBAR_HEIGHT = 20

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class ToolbarUI(aui.AuiToolBar):
    def __init__(self, parent, src_path ):
        """ Toolbar panel """
        super().__init__(parent, -1, wx.DefaultPosition, wx.DefaultSize)   # agwStyle=aui.AUI_TB_TEXT  (show label)
                                                                           # self.SetToolTextOrientation(1) (label orientation)
        self.parent = parent
        self.src_path = src_path
        self.toolbar_icon()
        self.toolbar_item()
        self.DoGetBestSize()

        self.event_handle()

    def event_handle(self):
        """Add Event to Menu Item"""
        evt = MenuEvent(self.parent)
        self.parent.Bind(wx.EVT_MENU, evt.file_event,    id = 100)
        self.parent.Bind(wx.EVT_MENU, evt.save_event,    id = 101)
        self.parent.Bind(wx.EVT_MENU, evt.setting_event, id = 201)
        self.parent.Bind(wx.EVT_MENU, evt.map_event,     id = 302)
        self.parent.Bind(wx.EVT_MENU, evt.parse_event,   id = 401)

    def path_trans(self, path):
        """Change source file path into the same type"""
        new_path = self.src_path + "\\" + path
        new_path = new_path.replace("/","\\")
        return new_path

    def toolbar_icon(self):
        """Get Icon"""
        self.open_image    = wx.Image(self.path_trans('open.png')).Rescale(TOOLBAR_WIDTH, TOOLBAR_HEIGHT)
        self.save_image    = wx.Image(self.path_trans('save.png')).Rescale(TOOLBAR_WIDTH, TOOLBAR_HEIGHT)
        self.quit_image    = wx.Image(self.path_trans('quit.png')).Rescale(TOOLBAR_WIDTH, TOOLBAR_HEIGHT)
        self.setting_image = wx.Image(self.path_trans('setting.png')).Rescale(TOOLBAR_WIDTH, TOOLBAR_HEIGHT)
        self.map_image     = wx.Image(self.path_trans('wafer.png')).Rescale(TOOLBAR_WIDTH, TOOLBAR_HEIGHT)
        self.parse_image   = wx.Image(self.path_trans('parse.png')).Rescale(TOOLBAR_WIDTH, TOOLBAR_HEIGHT)

    def toolbar_item(self):
        """ Create Item """
        self.AddSimpleTool( 100, u"open", wx.Bitmap(self.open_image, wx.BITMAP_TYPE_ANY) )
        self.AddSimpleTool( 101, u"save", wx.Bitmap(self.save_image, wx.BITMAP_TYPE_ANY) )
        self.AddSimpleTool( 201, u"setting", wx.Bitmap(self.setting_image, wx.BITMAP_TYPE_ANY) )
        self.AddSimpleTool( 302, u"map", wx.Bitmap(self.map_image, wx.BITMAP_TYPE_ANY) )
        self.AddSimpleTool( 401, u"parse", wx.Bitmap(self.parse_image, wx.BITMAP_TYPE_ANY) )
        self.SetToolBitmapSize(wx.Size(128,128))
        self.Realize()

class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="Test Toolbar")
        self.panel = ToolbarUI(self, root + "\\source\\image\\")
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
