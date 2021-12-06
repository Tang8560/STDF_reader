# -*- coding: utf-8 -*-
#==========================================================================
# Plot wafer map
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import os
import sys
import wx.grid
from pubsub import pub

#==========================================================================
# IMPORTS NOTEBOOK FUNCTION
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

#==========================================================================
# MAIN PROGRAM
#==========================================================================
class MapUI ( wx.Panel ): 
	
    def __init__( self, parent):
        """ map panel """
        super().__init__(parent)
        self.build_panel()

    def build_panel(self):
        self.grid_panel = wx.Panel(self,  -1)       
        self.grid_sizer = wx.BoxSizer( wx.VERTICAL )
           
        self.test_grid = wx.grid.Grid(self.grid_panel, -1, style = wx.VSCROLL )
        self.test_grid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE ) 
        self.test_grid.AutoSizeColumns()
        self.test_grid.AutoSizeRows()
        self.test_grid.DisableDragRowSize()
        self.grid_sizer.Add( self.test_grid, 1, wx.ALL|wx.EXPAND, 5 )
                   
        self.grid_panel.SetSizer( self.grid_sizer )
        self.grid_panel.Layout()
        self.grid_sizer.Fit( self.grid_panel )   
        self.Bind(wx.EVT_SIZE, self.onResize)       
        self.Layout()
        
    def onResize(self, event):
        ss = self.GetSize()
        for i in range(self.test_grid.GetNumberCols()):
            self.test_grid.SetColSize(i,ss[0]/(self.test_grid.GetNumberCols()+1))
        for j in range(self.test_grid.GetNumberRows()):
            self.test_grid.SetRowSize(j,ss[1]/(self.test_grid.GetNumberRows()+1))
        self.grid_sizer.Fit( self.grid_panel )  
        self.test_grid.SetRowLabelSize(ss[0]/(self.test_grid.GetNumberCols()+1)) 
        self.test_grid.SetColLabelSize(ss[1]/(self.test_grid.GetNumberRows()+1)) 
        self.Layout()
        self.Refresh()

    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))
                

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Test map")
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        self.panel = MapUI(self)
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
    