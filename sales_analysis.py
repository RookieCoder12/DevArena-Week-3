import pandas as pd
pd.set_option('display.max_columns', 5)

# Importing thr file
df = pd.read_csv(r"/Users/developer/Documents/Current Project/Python/DevArena /DevArena-Week-3/sales_data.csv")
print(df.head())

# # Shape of the database
print(f"\nShape of the dataframe: {df.shape}")

# # Printing the columns
print("\n",df.columns)

# # Checking the null values and the columns datatypes
print("\n\n",df.info())

# # Dropping duplicates
df.drop_duplicates(inplace=True)

print("\nExecutive Summary:")

# # Collective revenue and quantity sold for all the months
total_revenue = df["Total_Sales"].sum()
quantity_sold = df["Quantity"].sum()
print("\n\tTotal Revenue: ", total_revenue)
print("\n\tQuantity Sold: ", quantity_sold)

# # Executive Summary
product_df = df.groupby('Product').agg(
    total_sales = ('Total_Sales', 'sum')
)

product_df.sort_values(by='total_sales', ascending=False, inplace=True)
product_df.reset_index(inplace=True)

print(f"\n\tBest performing product category is: {product_df['Product'].iloc[0]} With Sales = {product_df['total_sales'].iloc[0]}")

# # M-o-M Return
df1 = df[["Date", "Product", "Total_Sales", "Customer_ID"]]
df1[["Year", "Month", "Day"]] = df1["Date"].str.split("-", expand=True)
df1.drop(["Date", "Year"], axis=1, inplace=True)

month_df = df1.groupby('Month').agg(
    monthly_sales = ('Total_Sales', 'sum'),
)

month_df.index = month_df.index.astype(int)
month_df.reset_index(inplace=True)
month_df["Month"] = month_df["Month"].astype(int)

# for i in range(1, 5):
#     month_df["M-o-M %"] = ((month_df[month_df["Month"] == i]["monthly_sales"] - month_df[month_df["Month"] == i-1]["monthly_sales"]) / month_df[month_df["Month"] == (i-1)]["monthly_sales"]) *100

month_df["M-o-M %"] = (month_df["monthly_sales"].pct_change() * 100).round(2)

print("\nMonth - on - Month Returns:")
# print(month_df[month_df["Month"] == 1]["monthly_sales"])
print("\n", month_df)

# # Customer Counts

monthly_orders_df = df1.groupby("Month").agg(
    no_orders = ('Customer_ID', 'count')
)

print("\nOrder Change:")
monthly_orders_df["Change %"] = (monthly_orders_df["no_orders"].pct_change() * 100).round(2)
print("\n", monthly_orders_df)