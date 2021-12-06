# -*- coding: utf-8 -*-
#==========================================================================
# Combine all UI panel
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
import time
import threading
import pandas as pd
from pubsub     import pub
from wx.lib.agw import aui

#==========================================================================
# IMPORTS UI PANEL
#==========================================================================
root = os.getcwd()
sys.path.append(root)

from .menu_ui     import  MenuUI
from .toolbar_ui  import  ToolbarUI
from .report_ui   import  ReportUI
from .log_ui      import  LogUI
from .plot_ui     import  PlotUI
from .map_ui      import  MapUI
#==========================================================================
# IMPORTS FUNCTION
#==========================================================================

from script.create_thread import Thread
from script.parse_data    import StdfParse
from script.file_read     import FileReaders
from script.load_xlsx     import LoadXlsx
from script.create_table  import DataTable

#==========================================================================
# PARAMETER
#==========================================================================
image_path    = root + "\\source\\image\\"

#==========================================================================
# PUB SUBSCRIBE
#==========================================================================
MENU_FILE    = "MENU_FILE"
MENU_SAVE    = "MENU_SAVE"
MENU_SETTING = "MENU_SETTING"
MENU_CSV     = "MENU_CSV"
MENU_MAP     = "MENU_MAP"
MENU_PARSE   = "MENU_PARSE"

#==========================================================================
# MAIN PROGRAM
#==========================================================================
class Main (wx.Frame):

    def __init__(self, parent):
        """ Main panel """
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        wx.Frame.__init__ (self, parent, -1, title = u"STDF Reader", size=(framew*0.5, frameh))
        self.SetMinSize((framew*0.5, frameh*0.7))
        self.Startup()
        self.add_map = False
        self.add_csv = False
        pub.subscribe(self.pub_file, MENU_FILE)
        pub.subscribe(self.pub_save, MENU_SAVE)
        pub.subscribe(self.pub_setting, MENU_SETTING)
        pub.subscribe(self.pub_csv, MENU_CSV)
        pub.subscribe(self.pub_map, MENU_MAP)        
        pub.subscribe(self.pub_parse, MENU_PARSE)  

    def Startup(self):
        """ Startup the UI """
        self.Status()
        self.BuildPanel()
        self.InitUI()
        # Create UI Thread
        T_Timer = threading.Thread(target =self.Timer, args=())
        T_Timer.start()

    def BuildPanel(self):
        """ Build panel object """
        ## Create Panel Object
        self.menu_build     = MenuUI(self, image_path )
        self.toolbar_build  = ToolbarUI(self, image_path )
        self.report_build   = ReportUI(self)
        self.log_build      = LogUI(self)
        self.plot_build     = PlotUI(self)
        self.map_build      = MapUI(self)

        ## Create AUI Manager
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        self.manager = aui.AuiManager()
        self.manager.SetManagedWindow(self)
        self.toolbar_info  = aui.AuiPaneInfo().Name('Control').Top().Show().Floatable(True).Movable(False).CaptionVisible(False)
        self.report_info   = aui.AuiPaneInfo().Name(' Report ').Center().Show().Floatable(False).Movable(False).CloseButton(False)
        self.log_info      = aui.AuiPaneInfo().Name(' Log data ').Center().Show().Floatable(False).Movable(False).CloseButton(False)
        self.plot_info     = aui.AuiPaneInfo().Name('Plot').CenterPane().Show().Floatable(False).Movable(False).MinSize(-1, frameh*0.55)
        self.map_info      = aui.AuiPaneInfo().Name('Map').CenterPane().Show().Floatable(False).Movable(False).MinSize(-1, frameh*0.55)

    def InitUI(self):
        """ Main frame layout """
        self.manager.AddPane(self.toolbar_build,  self.toolbar_info)
        self.manager.AddPane(self.plot_build,     self.plot_info)
        self.manager.AddPane(self.map_build , self.map_info )
        self.manager.AddPane(self.log_build,      self.log_info)
        self.manager.AddPane(self.report_build,   self.report_info, target=self.log_info)
        self.manager.GetPane(self.map_build).Hide()
        self.manager.Update()

        ## Event
        self.Bind(wx.EVT_SIZE, self.onResize)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show()

    def Status(self):
        """ Statusbar """
        self.statusbar = self.CreateStatusBar(style = wx.STB_SIZEGRIP)
        self.statusbar.SetForegroundColour((255,255,255))
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-9,-1]) 
        self.total_seconds = 0

    def Timer(self):
        """ Stopwatch """
        while True:
            time.sleep(1)
            self.total_seconds += 1
            seconds = self.total_seconds % 60
            minutes = int((self.total_seconds / 60) % 60)
            hours   = int((self.total_seconds / 3600) % 24)
            times   = str(hours).zfill(2)+":"+str(minutes).zfill(2)+":"+str(seconds).zfill(2)
            self.statusbar.SetStatusText(times, 1)
            self.statusbar.Layout()

    def prompt_msg(self, message): 
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True) 

    def onResize(self, event):
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        self.framew = framew
        self.frameh = frameh
        self.Refresh()

    def pub_file(self, file_path):
        df, data, scale = LoadXlsx(file_path,"PRR","G,H,J")

        # Add data to report ui
        self.report_build.report_txt.AppendText(str(df))

        # Show wafer map on map ui
        dict = {}
        Cols = range(scale[0],scale[1]+1)
        Rows = range(scale[2],scale[3]+1)
        Rowlabel_list = [str(j) for j in Rows]   
        Row_value     = ["" for _ in Rows]

        for i in Cols:
            dict[i] = Row_value
        dataframe = pd.DataFrame(dict, index=Rowlabel_list)
        self.map_build.test_grid.SetTable(DataTable(dataframe), takeOwnership=True)

        # Set cell value 
        for x,y,v in data:
            # print(x,y,v, scale[0], scale[2])
            self.map_build.test_grid.SetCellValue(y-scale[2],x-scale[0], str(v))
        self.manager.Update()
        self.map_build.onResize(event=None)

    def pub_save(self, save_path):
        pass

    def pub_setting(self, setting):
        pass

    def pub_map(self, map):
        self.manager.GetPane(self.map_build).Hide()
        self.manager.GetPane(self.plot_build).Show()
        self.manager.Update()

    def pub_csv(self, csv):
        self.manager.GetPane(self.plot_build).Hide()
        self.manager.GetPane(self.map_build).Show()
        self.manager.Update()
        self.map_build.onResize(event=None)

    def pub_parse(self, parse_path):
        parse_data = threading.Thread(target =StdfParse, args=(parse_path,))
        # Use pystdf to parse (.stdf) file
        excel_parse = threading.Thread(target =FileReaders.to_excel, args=(parse_path,))

        parse_data.start()
        excel_parse.start()


if __name__ == '__main__':
    app = wx.App(0)
    frame = Main(None)
    frame.Show()
    app.MainLoop()
