from ast import Return
import os
from numpy import mat
import pandas as pd

class Olist:
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        csv_path = os.path.join(os.path.dirname(__file__), "..", "raw_data", "csv")
        file_names = [file for file in os.listdir(csv_path) if file.endswith('csv')]
        key_names = [name.replace('_dataset.csv','').replace('.csv','').replace('olist_','') for name in file_names]
        data = {key:pd.read_csv(os.path.join(csv_path, value)) for key, value in zip(key_names, file_names)}
        return data
    
    def get_matching_table(self):
        """
        This function returns a matching table between
        columns [ "order_id", "review_id", "customer_id", "product_id", "seller_id"]
        """
        
        data = self.get_data()
        
        #select on;y the colums of interest
        orders = data["orders"][["customer_id", "order_id"]]
        reviews = data["orders_reviews"][["order_id", "review_id"]]
        items = data["orders_items"][["order_id", "product_id", "seller_id"]]
        
        # Merge DataFrame
        matching_table = orders.merge(reviews, on="order_id", how ="outer")\
            .merge(items, on="order_id", how="outer")
            
        # Remove duplicates from matching table
        matching_table = matching_table.drop_duplicates()
        
        return matching_table
        