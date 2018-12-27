import pandas as pd
from datetime import datetime
import os

def save_hdf(symbol,csv_file,sheetname = ""):
    data_df = pd.read_csv(csv_file) 
    data_df['datetime'] = data_df['datetime'].apply(lambda x : datetime.strptime(x,"%Y%m%d %H:%M:%S"))
    data_df['date'] = data_df['datetime'].apply(lambda x : x.strftime("%Y%m%d"))
    data_df['time'] = data_df['datetime'].apply(lambda x : x.strftime("%H:%M:%S"))
    data_df['vtSymbol'] = symbol
    
    date = set(data_df['date'])
    print(date)

    if data_df.size > 0:
        save_path = os.path.join("E:/vnpy_data/", "bar", symbol.replace(":", "_"))
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        for single_date in date:
            file_data = data_df[data_df["date"] == single_date]
            if file_data.size > 0:
                file_path = os.path.join(save_path, "%s.h5" % (single_date,))
                file_data.to_hdf(file_path, key="d")

if __name__ == '__main__':
    save_hdf('rb:SHF', "rb88-2010-2018.csv")