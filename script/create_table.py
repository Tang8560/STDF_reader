import wx
import pandas as pd

class DataTable(wx.grid.GridTableBase):

    def __init__(self, data):      
        wx.grid.GridTableBase.__init__(self)
        if data is None: 
            data = pd.DataFrame()
        self.data = data
        
    def GetNumberRows(self):
        return len(self.data)
    
    def GetNumberCols(self):   
        return len(self.data.columns)
    
    def GetValue(self, row, col):
        return self.data.iloc[row, col]
    
    def SetValue(self, row, col, value):
        self.data.iloc[row, col] = value

    def GetColLabelValue(self, col):
        if self.data.index.name is None:
            return str(self.data.columns[col])

    def GetRowLabelValue(self, row):
        if self.data.columns.name is None:
            return str(self.data.index[row])