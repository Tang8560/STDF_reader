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
# SETTING MENU ICON SIZE
#==========================================================================
MENU_WIDTH  = 15
MENU_HEIGHT = 15

#==========================================================================
# MAIN PROGRAM
#==========================================================================
class MenuUI( object ):
    def __init__( self, parent, src_path ):
        """Create Menu"""
        self.parent = parent
        self.src_path = src_path
        self.parent.menubar = wx.MenuBar()
        self.menu_build()
        self.menu_icon()
        self.menu_item()
        self.menu_item_icon()
        self.file_menu()
        self.edit_menu()
        self.view_menu()
        self.go_menu()
        self.help_menu()
        self.parent.SetMenuBar( self.parent.menubar )

        self.event_handle()

    def event_handle(self):
        """Add Event to Menu Item"""
        evt = MenuEvent(self.parent)
        self.parent.Bind(wx.EVT_MENU, evt.file_event,    id = 100)
        self.parent.Bind(wx.EVT_MENU, evt.save_event,    id = 101)
        self.parent.Bind(wx.EVT_MENU, evt.quit_event,    id = 102)
        self.parent.Bind(wx.EVT_MENU, evt.setting_event, id = 201)
        self.parent.Bind(wx.EVT_MENU, evt.csv_event,     id = 301)
        self.parent.Bind(wx.EVT_MENU, evt.map_event,     id = 302)
        self.parent.Bind(wx.EVT_MENU, evt.parse_event,   id = 401)
        self.parent.Bind(wx.EVT_MENU, evt.about_event,   id = 501)

    def path_trans(self, path):
        """Change source file path into the same type"""
        new_path = self.src_path + "\\" + path
        new_path = new_path.replace("/","\\")
        return new_path

    def menu_build(self):
        """Create Menubar Item"""
        self.file = wx.Menu()
        self.edit = wx.Menu()
        self.view = wx.Menu()
        self.go   = wx.Menu()
        self.help = wx.Menu()

    def menu_icon(self):
        """Get Icon"""
        self.open_image    = wx.Image(self.path_trans('open.png')).Rescale(MENU_WIDTH, MENU_HEIGHT)
        self.save_image    = wx.Image(self.path_trans('save.png')).Rescale(MENU_WIDTH, MENU_HEIGHT)
        self.quit_image    = wx.Image(self.path_trans('quit.png')).Rescale(MENU_WIDTH, MENU_HEIGHT)
        self.setting_image = wx.Image(self.path_trans('setting.png')).Rescale(MENU_WIDTH, MENU_HEIGHT)
        self.csv_image     = wx.Image(self.path_trans('csv.png')).Rescale(MENU_WIDTH, MENU_HEIGHT)
        self.map_image     = wx.Image(self.path_trans('wafer.png')).Rescale(MENU_WIDTH, MENU_HEIGHT)
        self.parse_image   = wx.Image(self.path_trans('parse.png')).Rescale(MENU_WIDTH, MENU_HEIGHT)

    def menu_item(self):
        """
        Create Item
        ------------------------------------------
        'MenuItem' object has no attribute 'Bind', thus we must use id to bind the menu event.
        """
        self.open       = wx.MenuItem( self.file, 100, "&Open\tCtrl+O"   , kind = wx.ITEM_NORMAL )
        self.save       = wx.MenuItem( self.file, 101, "&Save\tCtrl+S"   , kind = wx.ITEM_NORMAL )
        self.quit       = wx.MenuItem( self.file, 102, "&Quit\tCtrl+Q"   , kind = wx.ITEM_NORMAL )
        self.setting    = wx.MenuItem( self.edit, 201, "&Setting\tF2"    , kind = wx.ITEM_NORMAL )
        self.view_csv   = wx.MenuItem( self.view, 301, "&CSV\tF3"        , kind = wx.ITEM_NORMAL )
        self.view_map   = wx.MenuItem( self.view, 302, "&Wafer Map\tF4"  , kind = wx.ITEM_NORMAL )
        self.stdf_parse = wx.MenuItem( self.go,   401, "&parse\tF5"      , kind = wx.ITEM_NORMAL )
        self.about      = wx.MenuItem( self.help, 501, "&About\tF1"      , kind = wx.ITEM_NORMAL )

    def menu_item_icon(self):
        """Add Icon to Menu Item"""
        self.open.SetBitmap(wx.Bitmap(self.open_image))
        self.save.SetBitmap(wx.Bitmap(self.save_image))
        self.quit.SetBitmap(wx.Bitmap(self.quit_image))
        self.setting.SetBitmap(wx.Bitmap(self.setting_image))
        self.view_csv.SetBitmap(wx.Bitmap(self.csv_image))
        self.view_map.SetBitmap(wx.Bitmap(self.map_image))
        self.stdf_parse.SetBitmap(wx.Bitmap(self.parse_image))
        self.about.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_MENU,(MENU_WIDTH, MENU_HEIGHT)))

    def file_menu(self):
        """File Menu Layout"""
        self.file.Append( self.open )
        self.file.Append( self.save )
        self.file.Append( self.quit )
        self.parent.menubar.Append( self.file, u" File " )

    def edit_menu(self):
        """Edit Menu Layout"""
        self.edit.Append( self.setting )
        self.parent.menubar.Append( self.edit, u" Edit " )

    def view_menu(self):
        """Run Menu Layout"""
        self.view.Append( self.view_csv )
        self.view.Append( self.view_map )
        self.parent.menubar.Append( self.view, u" View " )

    def go_menu(self):
        """Tool Menu Layout"""
        self.go.Append( self.stdf_parse )
        self.parent.menubar.Append( self.go, u" Go " )

    def help_menu(self):
        """Help Menu Layout"""
        self.help.Append( self.about )
        self.parent.menubar.Append( self.help, u" Help " )

class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="Test Menu")
        self.panel = MenuUI(self, root + "\\source\\image\\")
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
