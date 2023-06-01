import pandas as pd
import os

# Step 1: Import pandas and os

# Step 2: Open new CSV as a DataFrame
root_path = r"C:\Users\macmahm\Desktop\Temp\Budget MAster"
new_csv_path = os.path.join(root_path, "New/Transactions.csv")
df_new = pd.read_csv(new_csv_path, usecols=["Date", "Amount", "Category", "Merchant Name"])
df_new['Merchant Name'].fillna('uncategorised',inplace=True)

# Step 3: Categorize transactions based on the merchant name
# Add your own categorization rules here

def categorise_MN(df, a, b):
    df.loc[df['Merchant Name'] == a, 'Category'] = b
    return


def categprise_MN_contains(df, a, b):
    df.loc[df['Merchant Name'].str.contains(a), 'Category'] = b
    return


def categorise_cat(df, a, b):
    df.loc[df['Category'] == a, 'Category'] = b
    return


def rent(df):
    df.loc[df['Amount'] == -320, 'Category'] = "Rent"
    return
def specific(df,amount,cat):
    df.loc[df['Amount'] == amount, 'Category'] = cat
    return

rent(df_new)
specific(df_new,-457.55,"Suit")
specific(df_new,-269.99,"Shoes")

# Categorise based on entire merchant  category
# df_new.loc[df_new['Category']=='donations','Category'] = "opshop"
categorise_MN(df_new, 'Beem', "Friend Debt")

# Categorise based on small part of merchant name category
# df_new.loc[df_new['Merchant Name'].str.contains("hotel|Club|Greens|Imperial|Clock|The Vic|Pav"),"Category"] = "Pub"
# df_new[df_new['Merchant Name'].str.contains("Uber")] = "Uber"
categprise_MN_contains(df_new, "Hotel|Club|Greens|Imperial|Clock|The Vic|Pav|Goro", "Pub")
categprise_MN_contains(df_new, "Uber", "Uber")
categprise_MN_contains(df_new, 'Taxation', "Hecs Debt")
categprise_MN_contains(df_new, 'Fitness', "Gym")
categprise_MN_contains(df_new, 'NSW', "Public Transport")
categprise_MN_contains(df_new, 'University', "UNSW")
categprise_MN_contains(df_new, 'Tobacconist|Tobacco', "Vapes")
categprise_MN_contains(df_new, 'Cellars|Dan|Booze|Liquor', "Alcohol")

# Categorise changing category
# df_new.loc[df_new['Merchant Name']=='Beem','Category'] = "Friend Debt"
categorise_cat(df_new, 'Donations', "Shopping")
categorise_cat(df_new, 'Transfers out', "Friend Debt")
categorise_cat(df_new, 'Other income', "Friend Receivable")
categorise_cat(df_new, 'Transfers in', "Friend Receivable")
categorise_cat(df_new, 'Transport', "Petrol")

df_new = df_new.drop(["Merchant Name"],axis = 1)
df_new = df_new.drop(df_new[df_new['Category']=='Internal transfers'].index)
df_new['Date'] = pd.to_datetime(df_new['Date'],format='mixed', dayfirst= True)
df_new['Date'] = df_new['Date'].dt.strftime('%d/%m/%Y')
df_new['Date'] = pd.to_datetime(df_new['Date'],format='%d/%m/%Y', dayfirst= True)

# Step 4: Append new transactions to the second sheet of the master Excel, excluding duplicates
master_excel_path = os.path.join(root_path,"Master Data.xlsx")
sheet_name = "Data"

df_master = pd.read_excel(master_excel_path, sheet_name=sheet_name)
df_master['Date'] = pd.to_datetime(df_master['Date'],format = "%d/%m/%Y")

# Exclude duplicates based on Date, Amount, and Merchant Name
df_master_max_date = pd.to_datetime(df_master['Date'].max())
if pd.isnull(df_master_max_date):
    df_master_max_date = pd.to_datetime("01/01/2022")
# Filter df_new based on the maximum date of df_master
df_new = df_new.loc[df_new['Date'] > df_master_max_date]

# Append new transactions to the master DataFrame
df_master = pd.concat([df_master, df_new])
df_master['Date'] = df_master['Date'].dt.strftime('%d/%m/%Y')
# Step 5: Save master Excel and move the new CSV to the old Transactions folder
writer = pd.ExcelWriter(master_excel_path)
df_master.to_excel(writer, sheet_name=sheet_name, index=False)
writer.close()

