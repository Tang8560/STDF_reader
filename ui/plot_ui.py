# -*- coding: utf-8 -*-
#==========================================================================
# Plot wafer map
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

import wx
from wafer_map import gen_fake_data
from wafer_map import wm_core

class PlotUI( wx.Panel ):

    def __init__(self, parent, xyd = None, wafer_info = None):
        """ Check panel """
        wx.Panel.__init__(self, parent, -1, style=wx.SIMPLE_BORDER)
        if (xyd and wafer_info):
            self.xyd = xyd
            self.wafer_info = wafer_info
        else:
            wafer_info, xyd = gen_fake_data.generate_fake_data()
            self.xyd = xyd
            self.wafer_info = wafer_info       
        self.BuildPanel()

    
    def BuildPanel(self):
        """
        Create the wafer map
        """
        self.plot = wm_core.WaferMapPanel(self, self.xyd, self.wafer_info, show_die_gridlines=True,)
        plot_Sizer = wx.BoxSizer( wx.VERTICAL )
        plot_Sizer.Add( self.plot, 1, wx.EXPAND )
        self.SetSizer( plot_Sizer )
        self.Layout()
         

class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="  Plot  ")
        self.panel = PlotUI(self)
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
