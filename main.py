# -*- coding: utf-8 -*-
#==========================================================================
# Create Panel
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

import wx
from ui.main_ui import Main


if __name__ == '__main__':
    app = wx.App()
    frame = Main(None)
    frame.Show()
    app.MainLoop()
