import pandas as pd

# xlsx_path = "C:\\Users\\ACER\\Desktop\\STDF_MFG\\main_Lot_1_Wafer_1_Oct_13_09h33m41s_STDF.stdf.xlsx"

def LoadXlsx(xlsx_path,sheet_name,col):
    df = pd.read_excel(xlsx_path, sheet_name, usecols=col)
    try:
        x = df["X_COORD"].to_list()
        y = df["Y_COORD"].to_list()
        data = df.values.tolist()
    except Exception as e:
        print(e)

    return df, data, (min(x),max(x),min(y),max(y))


# data = LoadXlsx(xlsx_path,"PRR","G,H,J")
# print(data[0])