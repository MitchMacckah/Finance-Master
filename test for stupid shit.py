import pandas as pd
import os
root_path = r"C:\Users\macmahm\Desktop\Temp\Budget MAster"
master_excel_path = os.path.join(root_path,"Master Data.xlsx")
sheet_name = "Data"

df_master = pd.read_excel(master_excel_path, sheet_name=sheet_name)


df_master['Date'] = pd.to_datetime(df_master['Date'],format = "%d/%m/%Y")


# Exclude duplicates based on Date, Amount, and Merchant Name
df_master_max_date = df_master['Date'].max()


# Filter df_new based on the maximum date of df_master
# df_new = df_new.loc[df_new['Date'] > df_master_max_date]
