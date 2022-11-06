#Imports
import pandas as pd
from datetime import datetime
import requests
import json
import sqlite3
from sqlite3 import Error
import calendar
import pendulum
import math

#Password encryptor
from passlib.hash import pbkdf2_sha256

#database file
db_file = 'myob.db'

#global date variables
current_year = datetime.now().year
current_month = datetime.now().month
current_day = datetime.now().day
yesterday_day = current_day - 1
before_yesterday_day = current_day - 2
last_day_month = calendar.monthrange(current_year, current_month)[1]

month_num = f"{current_month:02d}"
day_num = f"{current_day:02d}"
yesterday_day_num = f"{yesterday_day:02d}"
before_yesterday_day_num = f"{before_yesterday_day:02d}"

start_date = "%s-%s-%s"%(current_year, month_num, '01')
start_year_date = "%s-%s-%s"%(current_year, '01', '01')
last_date = "%s-%s-%s"%(current_year, month_num, last_day_month)
orders_current_date = "%s-%s-%s"%(current_year, current_month, current_day)
orders_enddate = pd.to_datetime(orders_current_date) + pd.DateOffset(days=30)
today = "%s-%s-%s"%(current_year, month_num, day_num)
yesterday = "%s-%s-%s"%(current_year, month_num, yesterday_day_num)
before_yesterday = "%s-%s-%s"%(current_year, month_num, before_yesterday_day_num)

#Class Brands
class Brands:

    def __init__(self, company):
        self.company = company
        if self.company == 'tegral':
            #tegral MYOB details
            company_id = "1c79926b-3034-409d-af3f-1f6719ab711d"
            company_url = "https://arl2.api.myob.com/accountright"
            self.url_invoice = "%s/%s/Sale/Invoice/Item?$filter=Date ge datetime'%s' and Date le datetime'%s'"%(company_url, company_id, start_date, last_date)
            self.url_invoice_product = "%s/%s/Sale/Invoice/Item?$top=1000&$skip=1000&$filter=Date ge datetime'%s' and Date le datetime'%s'"%(company_url, company_id, start_year_date, last_date)
            #self.url_invoice_product = "%s/%s/Sale/Invoice/Item?$filter=Date ge datetime'%s' and Date le datetime'%s'"%(company_url, company_id, start_date, last_date)
            self.url_orders = "%s/%s/Sale/Order/Item?$filter=Date ge datetime'%s' and Date le datetime'%s' and Status eq 'Open'"%(company_url, company_id, start_date, orders_enddate.date())

            #token and secret keys
            self.api_key = "b8cc48f8-1e5d-44c6-9a57-aa0815aaed23"
            self.client_secret = "07W7kC6s9HDCUmHOgQ0GwyRw"
            self.site_token = 'poU7!IAAAANNbTR9SoyqcYi0sT7xghbwRJaw14myiHr4EKcISp41wwQAAAAEJxh8eHy402-BakGA54SPuqPXImv0cRkjRqgqtrmWPw-WaXIfTaQHSSDE2BH_x4F12T-TIf2y6zqP8M8seNc3XG3DCTX8DTrZfPnd7MryEhG41HNHnzKP_VdlN9YWsR2PhoGhMGZRrCzIDRD_kEeQmNe79JSaSAiZ7tNTaEa7g-X1Cy1BU9-pNmwXWUrGRzkXMmPxV-NINFRgtY3BgJdKzXh9yAhUN6h11sWJSJgnNHnoKlV3oT8iTCYoSeAAgPaw'
            
        else:
            #purific MYOB details
            company_id = "b0b1c4e1-4e92-4f49-b659-fa6d63f97565"
            company_url = "https://arl2.api.myob.com/accountright"
            self.url_invoice = "%s/%s/Sale/Invoice/Item?$filter=Date ge datetime'%s' and Date le datetime'%s'"%(company_url, company_id, start_date, last_date)
            self.url_orders = "%s/%s/Sale/Order/Item?$filter=Date ge datetime'%s' and Date le datetime'%s' and Status eq 'Open'"%(company_url, company_id, start_date, orders_enddate.date())

            #token and secret keys
            self.api_key = "72f41902-284d-403c-8cdc-654d5fda216d"
            self.client_secret = "ugSr6rek1akLoqbI8Q22F6jF"
            self.site_token = 'lvnc!IAAAAArQBLEMnNsuvqUvNLojZMW59hjy2TE-9g3GtysaUzc7wQAAAAGqxUo9Drb0FS5xZ6hsL5LAac3bi6E8uXLWzFE2RTnzjsmfIVb_IjOvtwgSklNvOoWa4U2_tU62GHaJLwAqgFZmemxVf2GzOmWZSY9I9h39zSlZrCzkF-S2R3d8rHdydaugR6aTmDbaj6JKMok92lnUFWXqYiaYERkWAsH2I7cj8iT-GLInQpOKKrOULr4dKM_QH9c012O5WX5T5U6IO5xJK_XQDYwjZG8gZ941BmtU8Jonph-w86nlpsJAP4s9u8s'

    #Create database and table
    def create_myob_db(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)

            # Create A Cursor
            c = conn.cursor()

            # Create A Table myob_invoice
            c.execute("""CREATE TABLE if not exists %s_myob_invoice(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_sales INTEGER,
                order_date timestamp,
                sample INTEGER)
                """%(self.company))

            # Create A Table myob_computed_invoice
            c.execute("""CREATE TABLE if not exists %s_myob_computed_invoice(
                ID INTEGER PRIMARY KEY,
                invoice_sales INTEGER,
                order_date timestamp)
                """%(self.company))

            # Create A Table myob_invoice_meta
            c.execute("""CREATE TABLE if not exists %s_myob_invoice_meta(
                ID INTEGER PRIMARY KEY,
                sales INTEGER)
                """%(self.company)) 

            # Create A Table myob_orders
            c.execute("""CREATE TABLE if not exists %s_myob_orders(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_sales INTEGER,
                order_date timestamp)
                """%(self.company))   

            # Create A Table myob_computed_orders
            c.execute("""CREATE TABLE if not exists %s_myob_computed_orders(
                ID INTEGER PRIMARY KEY,
                order_sales INTEGER,
                order_date timestamp)
                """%(self.company))

            # Create A Table myob_pipeline
            c.execute("""CREATE TABLE if not exists %s_myob_pipeline(
                ID INTEGER PRIMARY KEY,
                order_sales INTEGER,
                start_date timestamp,
                end_date timestamp)
                """%(self.company))

            # Create A Table tegral month target
            c.execute("""CREATE TABLE if not exists %s_month_target(
                ID INTEGER PRIMARY KEY,
                sales INTEGER,
                month_number TEXT)
                """%(self.company))

            # Create A Table tegral invoice year target
            c.execute("""CREATE TABLE if not exists %s_invoice_year_target(
                ID INTEGER PRIMARY KEY,
                invoice_sales INTEGER,
                order_date timestamp)
                """%(self.company))

            # Create A Table tegral year target meta
            c.execute("""CREATE TABLE if not exists %s_year_target_meta(
                ID INTEGER PRIMARY KEY,
                sales INTEGER)
                """%(self.company)) 

            # Create A Table tegral refresh flag
            c.execute("""CREATE TABLE if not exists %s_refresh_flag(
                ID INTEGER PRIMARY KEY,
                flag_date TEXT)
                """%(self.company)) 


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)
    
    #Update refresh flag
    def update_refresh_flag(self):
        try:
            td = pendulum.now('Australia/Sydney')
            td.to_day_datetime_string()
            formatted_str = td.format('dddd Do [of] MMMM YYYY HH:mm:ss A')
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            #c.execute("INSERT INTO %s_refresh_flag (flag_date) VALUES (?)"%(self.company),(datetime.now()))  
            c.execute("UPDATE %s_refresh_flag SET flag_date = '%s' WHERE ID=1"%(self.company, formatted_str))         

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #get refresh flags
    def get_refresh_flag(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT flag_date FROM %s_refresh_flag WHERE ID = '%s'"%(self.company, 1))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[0]
            else:
                return 0 

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #get product refresh flags
    def get_product_refresh_flag(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT flag_date FROM %s_product_refresh_flag WHERE ID = '%s'"%(self.company, 1))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[0]
            else:
                return 0 

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Insert MYOB sales data to DB
    def insert_myob_invoice_sales(self, order_id, invoice_sales, order_date, sample_flag):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            c.execute("INSERT INTO %s_myob_invoice (order_id, invoice_sales, order_date, sample) VALUES (?, ?, ?, ?)"%(self.company), (order_id, invoice_sales, order_date, sample_flag))          

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Update MYOB sales data to DB using order_id
    def update_myob_invoice_sales(self, order_id, invoice_sales, sample_flag):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("UPDATE %s_myob_invoice SET invoice_sales = '%s', sample = '%s' WHERE order_id = '%s'"%(self.company, invoice_sales, sample_flag, order_id))

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #get sale meta DB
    def get_myob_invoice_sale_meta(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_myob_invoice_meta WHERE ID = '%s'"%(self.company, 1))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[1]
            else:
                return 0 

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #update sale meta DB FLAGS
    def update_myob_invoice_sale_meta(self, sales):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("UPDATE %s_myob_invoice_meta SET sales = '%s' WHERE ID = '%s'"%(self.company, sales, 1))

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #reset sales meta db
    def reset_myob_invoice_sales_meta(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
            if self.get_myob_invoice_sale_meta() == 0:
                # Add A Record sales meta
                c.execute("INSERT INTO %s_myob_invoice_meta (sales) VALUES (?)"%(self.company),('0')) 
            else:
                # update a record in sales meta
                c.execute("UPDATE %s_myob_invoice_meta SET sales = '%s' WHERE ID = '%s'"%(self.company, 0,1))

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    def get_myob_invoice_sale_by_date(self, prev_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT order_date, SUM(invoice_sales) FROM %s_myob_invoice WHERE order_date = '%s'  GROUP BY order_date LIMIT 1"%(self.company, prev_date))
            records = c.fetchall()
            result = 0
            # Loop thru records
            # Loop thru records
            if records:
                for record in records:
                    if not record[1] == None:
                        result = record[1]

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
            return result
        except Error as e:
            print(e)

    #Check if myob id in DB exists
    def check_myob_invoice_id_exists(self, order_id, invoice_sales, order_date_rem, sample_flag):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT order_id FROM %s_myob_invoice WHERE order_id = '%s'"%(self.company, order_id))
            records = c.fetchall()

            # Loop thru records
            if records:
                self.update_myob_invoice_sales(order_id, invoice_sales, sample_flag)
            else:
                self.insert_myob_invoice_sales(order_id, invoice_sales, order_date_rem, sample_flag)

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Insert Computed sales in DB
    def insert_myob_invoice_computed_sale(self, invoice_sales, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            c.execute("INSERT INTO %s_myob_computed_invoice (invoice_sales, order_date) VALUES (?, ?)"%(self.company), (invoice_sales, order_date))          

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Update Computed sales in DB
    def update_myob_invoice_computed_sale(self, invoice_sales, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Update A Record   
            c.execute("UPDATE %s_myob_computed_invoice SET invoice_sales = '%s' WHERE order_date = '%s'"%(self.company, invoice_sales, order_date))    

            # Add a little message
            print('Done Editing')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Check if myob id in DB exists
    def check_myob_invoice_computed_exists(self, combine_sale_final, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_myob_computed_invoice WHERE order_date = '%s'"%(self.company, order_date))
            records = c.fetchall()

            # Loop thru records
            if records:
                print('exists')
                self.update_myob_invoice_computed_sale(combine_sale_final, order_date)
            else:
                print('not exists')
                #insert computed final sale in DB
                self.insert_myob_invoice_computed_sale(combine_sale_final, order_date)

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get data from DB based on month day
    def get_myob_sale_month_invoice(self): 

        for num in range(1, last_day_month + 1):
            if num > 9: 
                final_num = num
            else:
                final_num = "0%s"%num   
            
            start_date = "%s-%s-%s"%(current_year, month_num, final_num)
        
            meta_sale = self.get_myob_invoice_sale_meta()
            original_sale = self.get_myob_invoice_sale_by_date(start_date)

            #compute current sale plus previous sale date
            combine_sale = original_sale + meta_sale  

            #divide to tax
            combine_sale_final = combine_sale // 1.1

            #check MYOB computed exists based on date
            self.check_myob_invoice_computed_exists(combine_sale_final, start_date)
            
            #update sale meta DB
            self.update_myob_invoice_sale_meta(combine_sale)

    #Get MYOB Token
    def get_myob_token(self):
        try:
            token_url = "https://secure.myob.com/oauth2/v1/authorize/"

            payload = "client_id=%s&client_secret=%s&grant_type=refresh_token&refresh_token=%s"%(self.api_key, self.client_secret, self.site_token)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", token_url, headers=headers, data=payload)
            json_response = response.json()
            return json_response['access_token']
        except:
            return 0
    #get myob invoice data and insert
    def get_myob_data_invoice(self):

        refresh_token = "Bearer %s"%self.get_myob_token()
        payload={}

        headers = {
            'x-myobapi-key': self.api_key,
            'x-myobapi-version': 'v2',
            'Accept-Encoding': 'gzip,deflate',
            'Authorization': refresh_token
        }

        # Inspect some attributes of the `requests` repository
        try:
            response = requests.request("GET", self.url_invoice, headers=headers, data=payload, timeout=10)
            json_response = response.json()

            items = json_response['Items']
            if items:
                for item in items:
                    order_id = item["Number"]
                    order_status = item["Status"]
                    invoice_sales = item["TotalAmount"]
                    order_date = item["Date"]
                    order_lines = item["Lines"]
                    sample = order_lines[0]["Job"]
                    if sample is None:
                        sample_flag = 0
                    else:
                        sample_flag = 1    
                    datem = datetime.strptime(order_date, "%Y-%m-%dT%H:%M:%S")
                    order_date_rem = f"{datem.year}-{datem.month:02d}-{datem.day:02d}"
                    self.check_myob_invoice_id_exists(order_id, invoice_sales, order_date_rem, sample_flag)
            else:
                pass
        except requests.Timeout as errtim:
            print ("Timeout Error: ", errtim)
        except requests.ConnectionError as errcon:
            print ("Connection Error: ", errcon)

    #Insert MYOB orders data to DB
    def insert_myob_orders_sales(self, order_id, order_sales, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            c.execute("INSERT INTO %s_myob_orders (order_id, order_sales, order_date) VALUES (?, ?, ?)"%(self.company), (order_id, order_sales, order_date))          

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Delete MYOB orders data to DB
    def delete_myob_orders_sales(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Delete Record
            c.execute("DELETE FROM %s_myob_orders"%(self.company))         


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)


    #Get MYOB data from api orders
    def get_myob_data_orders(self):

        refresh_token = "Bearer %s"%self.get_myob_token()
        payload={}

        headers = {
            'x-myobapi-key': self.api_key,
            'x-myobapi-version': 'v2',
            'Accept-Encoding': 'gzip,deflate',
            'Authorization': refresh_token
        }
        try:
            response = requests.Session().request("GET", self.url_orders, headers=headers, data=payload, timeout=10)

            # Inspect some attributes of the `requests` repository
            json_response = response.json()
            items = json_response['Items']
            if items:
                self.delete_myob_orders_sales()
                for item in items:
                    order_id = item["Number"]
                    order_status = item["Status"]
                    order_sales = item["TotalAmount"]
                    #order_sales_ex = order_sales // 1.1
                    order_date = item["Date"]
                    order_lines = item["Lines"]
                    order_date_rem = order_date.replace("T00:00:00", "") 
                    self.insert_myob_orders_sales(order_id, order_sales, order_date_rem)
            else:
                pass
                      
        except requests.Timeout as errtim:
            print ("Timeout Error: ", errtim)
        except requests.ConnectionError as errcon:
            print ("Connection Error: ", errcon)       

    #Insert Computed orders in DB
    def insert_myob_order_computed_sale(self, order_sales, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            c.execute("INSERT INTO %s_myob_computed_orders (order_sales, order_date) VALUES (?, ?)"%(self.company), (order_sales, order_date))          

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Delete MYOB orders data to DB
    def delete_myob_computed_orders_sales(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Delete Record
            c.execute("DELETE FROM %s_myob_computed_orders"%(self.company))         

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get order sale data from db
    def get_myob_order_sale_from_db(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT order_date, SUM(order_sales) FROM %s_myob_orders GROUP BY order_date"%(self.company))
            records = c.fetchall()

            # Loop thru records
            if records:
                self.delete_myob_computed_orders_sales()
                for record in records:
                    order_date = record[0]
                    order_sales = 0
                    if not record[1] == None:
                        order_sales = record[1]
                    self.insert_myob_order_computed_sale(order_sales, order_date)
            else:
                return 0

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get Invoice Sales Data Yesterday
    def get_myob_invoice_data_yesterday(self):

        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_myob_computed_invoice WHERE order_date BETWEEN '%s' AND '%s'"%(self.company, yesterday, yesterday))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[1]

            else:
                return 0


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            return 0

    #Get Invoice Sales Data Yesterday
    def get_myob_invoice_data_before_yesterday(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_myob_computed_invoice WHERE order_date BETWEEN '%s' AND '%s'"%(self.company, before_yesterday, before_yesterday))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[1]

            else:
                return 0


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get Invoice Sales Data today
    def get_myob_invoice_data_today(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_myob_computed_invoice WHERE order_date BETWEEN '%s' AND '%s'"%(self.company, today, today))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    #order_date = record[2]
                    return record[1]

            else:
                return 0


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get Invoice Sales Yesterday
    def get_myob_invoice_yesterday(self):
        return self.get_myob_invoice_data_today() - self.get_myob_invoice_data_yesterday()

    #Get Order Sales for whole month
    def get_myob_orders_computed_whole_month(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT SUM(order_sales) FROM %s_myob_computed_orders WHERE order_date BETWEEN '%s' AND '%s'"%(self.company, start_date, last_date))
            records = c.fetchall()
            result = 0
            # Loop thru records
            if records:
                for record in records:
                    if not record[0] == None:
                        result = record[0]

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()

            return result
        except Error as e:
            print(e)

    #Get computed Pipeline
    def get_myob_orders_computed_pipeline(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT SUM(order_sales) FROM %s_myob_computed_orders WHERE order_date BETWEEN '%s' AND '%s'"%( self.company, start_date, last_date ))
            records = c.fetchall()
            result = 0
            # Loop thru records
            if records:
                for record in records:
                    if not record[0] == None:
                        result = record[0]

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()

            return result

        except Error as e:
            print(e)

    #Get Month Potential
    def get_myob_month_potential(self):
        return self.get_myob_invoice_data_today() + self.get_myob_orders_computed_whole_month()

    #Get myob invoice sample sent
    def get_myob_invoice_sample_sent(self):
        
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT SUM(sample) FROM %s_myob_invoice WHERE order_date BETWEEN '%s' AND '%s'"%(self.company, start_date, last_date))
            records = c.fetchall()
            result = 0
            # Loop thru records
            if records:
                for record in records:
                    if not record[0] == None:
                        result = record[0]
            
            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
            return result
        except Error as e:
            print(e)

    #Get myob invoice sample sent
    def get_computed_pipeline_orders(self, start_date, end_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT SUM(order_sales) FROM %s_myob_computed_orders WHERE order_date BETWEEN '%s' AND '%s'"%(self.company, start_date, end_date))
            records = c.fetchall()
            result = 0
            # Loop thru records
            if records:
                for record in records:
                    if not record[0] == None:
                        result = record[0]

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
            return result
        except Error as e:
            print(e)

    #Insert PIPELINE data to DB
    def insert_pipeline(self, pipeline_total, start_date, end_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            c.execute("INSERT INTO %s_myob_pipeline (order_sales, start_date, end_date) VALUES (?, ?, ?)"%(self.company), (pipeline_total, start_date, end_date))          

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Delete MYOB PIPELINE DB data
    def delete_pipeline(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Delete Record
            c.execute("DELETE FROM %s_myob_pipeline"%(self.company))         


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get Pipeline sale based on whole month
    def get_myob_pipeline_month(self): 
        self.delete_pipeline()
        for num in range(1, last_day_month + 1):
            if num > 9: 
                final_num = num
            else:
                final_num = "0%s"%num   
            
            start_date_loop = "%s-%s-%s"%(current_year, month_num, final_num)
            end_date = pd.to_datetime(start_date_loop) + pd.DateOffset(days=30)    
            pipeline_total = self.get_computed_pipeline_orders(start_date, end_date.date()) // 1.1 
            if pipeline_total:
                self.insert_pipeline(pipeline_total, start_date_loop, end_date.date())

    #Get Email Contacts count from Vision 6
    def get_email_contact_count(self):
        try:
            url = "http://54.253.46.156/vision6/"
            r = requests.get(url)
            return r.text
        except:
            return 0
    
    #get and connect to js graph
    def get_data(self, type):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            if type == 'sales':
                c.execute("SELECT * FROM %s_myob_computed_invoice WHERE order_date BETWEEN '%s' AND '%s'"%(self.company, start_date, last_date))
            elif type == 'pipeline':
                c.execute("SELECT * FROM %s_myob_pipeline WHERE start_date BETWEEN '%s' AND '%s'"%(self.company, start_date, last_date))
            elif type == 'yeartarget':
                c.execute("SELECT * FROM %s_invoice_year_target WHERE order_date BETWEEN '%s' AND '%s'"%(self.company, start_date, last_date))
            records = c.fetchall()

            # Loop thru records
            if records:
                return records
            else:
                return 0
        except Error as e:
            print(e)


    #Get month target data
    def get_month_target_data(self, month_num):

        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_month_target WHERE month_number=%s"%(self.company, month_num))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[1]

            else:
                return 0


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #get year invoice target meta
    def get_invoice_year_meta(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_year_target_meta WHERE ID = '%s'"%(self.company, 1))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[1]
            else:
                return 0 

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #update year invoice target meta
    def update_invoice_year_meta(self, sales):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("UPDATE %s_year_target_meta SET sales = '%s' WHERE ID = '%s'"%(self.company, sales, 1))

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #reset year target meta db
    def reset_invoice_year_meta(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
            if self.get_invoice_year_meta() == 0:
                # Add A Record sales meta
                c.execute("INSERT INTO %s_year_target_meta (sales) VALUES (?)"%(self.company), ('0')) 
            else:
                # update a record in sales meta
                c.execute("UPDATE %s_year_target_meta SET sales = '%s' WHERE ID = '%s'"%(self.company, 0, 1))

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Insert invoice_year_target in DB
    def insert_invoice_year_target(self, invoice_sales, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            c.execute("INSERT INTO %s_invoice_year_target (invoice_sales, order_date) VALUES (?, ?)"%(self.company), (invoice_sales, order_date))          

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Update invoice_year_target in DB
    def update_invoice_year_target(self, invoice_sales, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Update A Record   
            c.execute("UPDATE %s_invoice_year_target SET invoice_sales = '%s' WHERE order_date = '%s'"%(self.company, invoice_sales, order_date))    

            # Add a little message
            print('Done Editing')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Check if invoice_year_target in DB exists
    def check_invoice_year_target_exists(self, combine_sale_final, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_invoice_year_target WHERE order_date = '%s'"%(self.company, order_date))
            records = c.fetchall()

            # Loop thru records
            if records:
                self.update_invoice_year_target(round(combine_sale_final), order_date)
            else:
                #insert computed final sale in DB
                self.insert_invoice_year_target(round(combine_sale_final), order_date)

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get and Update data from DB based on year target
    def get_invoice_year_target(self): 
        #reset invoice meta
        self.reset_invoice_year_meta()
        for num in range(1, last_day_month + 1):
            if num > 9: 
                final_num = num
            else:
                final_num = "0%s"%num   
            
            start_date = "%s-%s-%s"%(current_year, month_num, final_num)
            month_target = self.get_month_target_data(current_month)
            day_1 = month_target / 30
            
            meta = self.get_invoice_year_meta()

            #compute current sale plus previous sale date
            combine_sale = day_1 + meta  

            #divide to tax
            #combine_sale_final = combine_sale // 1.1

            print('Date: ', start_date)   
            print('Computed sales: ', combine_sale) 
            print('\n')
            self.check_invoice_year_target_exists(combine_sale, start_date)
            self.update_invoice_year_meta(combine_sale)

    #Get Invoice Sales Data Yesterday
    def count_orders(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT COUNT(*) FROM %s_myob_orders WHERE order_date BETWEEN '%s' AND '%s'"%(self.company, start_date, last_date))
            return c.fetchone()[0]
        except Error as e:
            print(e)

    #Insert product monthly data
    def insert_product(self, order_id, product_id, product_total, product_date, product_category):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
  
            # Add A Record
            c.execute("INSERT INTO %s_product (order_id, product_id, product_total, product_date, product_category) VALUES (?, ?, ?, ?, ?)"%(self.company), (order_id, product_id, product_total, product_date, product_category))    

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)
    
    #Delete MYOB PIPELINE DB data
    def delete_product_monthly(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Delete Record
            c.execute("DELETE FROM %s_product"%(self.company))         


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #get product categories
    def get_product_categories(self, product_id_monthly):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_product_categories"%(self.company))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    cat_name = record[1]
                    product_ids = record[2]
                    product_ids_chunks = product_ids.split(',')
                    for product_id in  product_ids_chunks:
                        if product_id_monthly == product_id:
                            return cat_name
            else:
                return 0

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #get month target for product
    def get_month_target_sales(self, product_category, order_month_num):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT fy_actual, new_growth, growth_portions FROM %s_product_categories WHERE product_category='%s'"%(self.company, product_category))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    fy_actual =  record[0]
                    new_growth =  record[1]
                    growth_portions =  record[2]
                    return round(fy_actual / 12 + new_growth / growth_portions * order_month_num)
            else:
                return 0

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #get year target for product
    def get_year_target_sales(self, product_category):
        sum = 0
        for num in range(1, 13):
            sum += self.get_month_target_sales(product_category, num)
        return sum

    #get product monthly based on cat
    def get_product_monthly_base_cat(self, type):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
            
            # Grab records from database
            if type == 'total': 
                c.execute("SELECT month_sales FROM %s_product_categories"%(self.company))
            elif type == 'month_target': 
                c.execute("SELECT month_target FROM %s_product_categories"%(self.company)) 
            else:
                c.execute("SELECT product_category FROM %s_product_categories"%(self.company))
            records = c.fetchall()
            
            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
            
            # Loop thru records
            result = 0 
            if records:
                result = records
            
            return result
        except Error as e:
            print(e)

    #get product monthly based on cat
    def get_product_yearly_base_cat(self, type):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
            
            # Grab records from database
            if type == 'total': 
                c.execute("SELECT yearly_sales FROM %s_product_categories"%(self.company))
            elif type == 'year_target': 
                c.execute("SELECT year_target FROM %s_product_categories"%(self.company)) 
            else:
                c.execute("SELECT product_category FROM %s_product_categories"%(self.company))
            records = c.fetchall()
            
            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
            
            # Loop thru records
            result = 0 
            if records:
                result = records
            
            return result
        except Error as e:
            print(e)

    #Create database and table
    def create_myob_product_db(self):
        # Create Database Or Connect To One
        conn = sqlite3.connect(db_file)

        # Create A Cursor
        c = conn.cursor()

        # Create A Table tegral product
        c.execute("""CREATE TABLE if not exists %s_product(
            ID INTEGER PRIMARY KEY,
            order_id TEXT,
            product_id TEXT,
            product_total TEXT,
            product_date timestamp,
            product_category TEXT)
            """%(self.company)) 

        # Create A Table tegral product categories
        c.execute("""CREATE TABLE if not exists %s_product_categories(
            ID INTEGER PRIMARY KEY,
            product_category TEXT,
            product_ids TEXT,
            fy_actual INTEGER,
            new_growth INTEGER,
            growth_portions INTEGER,
            month_target INTEGER,
            year_target INTEGER,
            month_sales INTEGER,
            yearly_sales INTEGER)
            """%(self.company)) 

         # Create A Table tegral product refresh flag
        c.execute("""CREATE TABLE if not exists %s_product_refresh_flag(
            ID INTEGER PRIMARY KEY,
            flag_date TEXT)
            """%(self.company)) 

        # Commit our changes
        conn.commit()

        # Close our connection
        conn.close()

    #Check if product id and order id exists
    def check_product_id_order_id_exists(self, order_id, product_id):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_product WHERE order_id = '%s' AND product_id='%s'"%(self.company, order_id, product_id))
            records = c.fetchall()
            result = 0
            # Loop thru records
            if records:
                result = 1
            else:
                result = 0

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
            
            return result
        except Error as e:
            print(e)

    #reset product categories
    def reset_product_category(self ):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
            c.execute("UPDATE %s_product_categories SET month_target = '%s', year_target = '%s', month_sales = '%s', yearly_sales = '%s'"%(self.company, 0, 0, 0, 0))

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #update product categories
    def update_product_category(self, product_category, target_month_sales, target_year_sales ):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
            c.execute("UPDATE %s_product_categories SET month_target = '%s', year_target = '%s' WHERE product_category = '%s'"%(self.company, target_month_sales, target_year_sales, product_category))

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #update product categories
    def update_product_category_sales(self, sales, product_category, type ):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
            if type == 'yearly':
                c.execute("UPDATE %s_product_categories SET yearly_sales = '%s' WHERE product_category = '%s'"%(self.company, sales, product_category))
            else:
                c.execute("UPDATE %s_product_categories SET month_sales = '%s' WHERE product_category = '%s'"%(self.company, sales, product_category))
            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Check product and update category data
    def get_product_update_category(self, type):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
            if type == 'yearly':
                # Grab records from database
                c.execute("SELECT SUM(product_total),product_category FROM %s_product GROUP BY product_category"%(self.company))
            else:
                # Grab records from database
                c.execute("SELECT SUM(product_total),product_category FROM %s_product WHERE product_date BETWEEN '%s' AND '%s' GROUP BY product_category"%(self.company, start_date, last_date))
            
            records = c.fetchall()
            # Loop thru records
            if records:
                for record in records:
                    sales =  record[0]
                    product_category =  record[1]
                    self.update_product_category_sales( sales, product_category, type )
                    #print(type)
                    #print(product_category)
                    #print(sales)
            else:
                pass
            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
            
        except Error as e:
            print(e)

    #Get MYOB data products from api invoice
    def get_myob_data_products_monthly(self):

        refresh_token = "Bearer %s"%self.get_myob_token()
        payload={}

        headers = {
            'x-myobapi-key': self.api_key,
            'x-myobapi-version': 'v2',
            'Accept-Encoding': 'gzip,deflate',
            'Authorization': refresh_token
        }

        # Inspect some attributes of the `requests` repository
        try:
            self.delete_product_monthly()
            response = requests.request("GET", self.url_invoice_product, headers=headers, data=payload, timeout=10)
            json_response = response.json()

            items = json_response['Items']
            if items:
                self.reset_product_category()
                for item in items:
                    order_id = item.get("Number")
                    order_date = item.get("Date")
                    order_lines = item.get("Lines")  
                    datem = datetime.strptime(order_date, "%Y-%m-%dT%H:%M:%S")
                    product_full_date = f"{datem.year}-{datem.month:02d}-{datem.day:02d}"
                    print(order_id)
                    print(product_full_date)
                    for line in order_lines:
                        product_total = line.get("Total")
                        product_id = line.get("Item",{}).get("Number")
                        if not self.check_product_id_order_id_exists(order_id, product_id):
                            if self.get_product_categories(product_id):
                                product_category = self.get_product_categories(product_id)
                            else:
                                product_category = 'Others'
                            target_month_sales = self.get_month_target_sales(product_category, current_month)
                            target_year_sales = self.get_year_target_sales(product_category)
                            if product_id and product_total > 0: 
                                self.insert_product(order_id, product_id, round(product_total), product_full_date, product_category)
                                self.update_product_category(product_category, target_month_sales, target_year_sales)
                self.get_product_update_category('yearly')
                self.get_product_update_category('monthly')
            else:
                pass
        except requests.Timeout as errtim:
            print ("Timeout Error: ", errtim)
        except requests.ConnectionError as errcon:
            print ("Connection Error: ", errcon)
        
    #Insert product categories, month and year target
    def insert_product_categories(self, cat_name, product_ids, fy_actual, new_growth, growth_portions):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            c.execute("INSERT INTO %s_product_categories (product_category, product_ids, fy_actual, new_growth, growth_portions) VALUES (?, ?, ?, ?, ?)"%(self.company), (cat_name, product_ids, fy_actual, new_growth, growth_portions))    
            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Insert product categories, month and year target
    def update_product_categories(self, category_id, cat_name, product_ids, fy_actual, new_growth, growth_portions):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Update A Record  
            c.execute("UPDATE %s_product_categories SET product_category = '%s', product_ids = '%s', fy_actual = '%s', new_growth = '%s', growth_portions = '%s' WHERE ID = '%s'"%(self.company, cat_name, product_ids, fy_actual, new_growth, growth_portions, category_id)) 
            
            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Update Monthly target for calculation
    def update_monthly_target(self, sales, num):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Update A Record  
            c.execute("UPDATE %s_month_target SET sales = '%s' WHERE month_number = '%s'"%(self.company, sales, num)) 
            
            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #check product categories exists
    def check_product_category_exists(self, product_category):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT product_category FROM %s_product_categories WHERE product_category='%s'"%(self.company, product_category))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[0]
            else:
                return 0

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)
    
    #get categories list
    def get_product_category_list(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_product_categories"%(self.company))
            records = c.fetchall()

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()

            # Loop thru records
            if records:
                return records
            else:
                return 0

            
        except Error as e:
            print(e)

    #get default product fields
    def get_default_product_fields(self, field, category_id ):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT %s FROM %s_product_categories WHERE ID='%s'"%(field, self.company, category_id))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[0]
            else:
                return 0


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()

        except Error as e:
            print(e)
    
    #get default month sales fields
    def get_default_month_fields(self, month_number ):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT sales FROM %s_month_target WHERE month_number='%s'"%(self.company, month_number))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[0]
            else:
                return 0


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()

        except Error as e:
            print(e)

    #Delete product categories from DB
    def delete_product_categories(self, cat_id):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Delete Record
            c.execute("DELETE FROM %s_product_categories WHERE ID='%s'"%(self.company, cat_id))         
            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Update refresh flag
    def update_refresh_product_flag(self):
        try:
            td = pendulum.now('Australia/Sydney')
            td.to_day_datetime_string()
            formatted_str = td.format('dddd Do [of] MMMM YYYY HH:mm:ss A')
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record 
            c.execute("UPDATE %s_product_refresh_flag SET flag_date = '%s' WHERE ID=1"%(self.company, formatted_str))         

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Refresh all data from MYOB
    def refresh(self):
        #create db
        self.create_myob_db()
        
        #Get MYOB data invoice from api
        self.get_myob_data_invoice()
        #reset sales meta db DONT FORGET TO ADD THIS !IMPORTANT
        self.reset_myob_invoice_sales_meta()
        
        #Get data from DB based on month day
        self.get_myob_sale_month_invoice()
        
        #Get MYOB data orders/pipeline from api
        self.get_myob_data_orders()
        
        #Get MYOB data orders/pipeline from database
        self.get_myob_order_sale_from_db()

        #generate pipeline data for the graph
        self.get_myob_pipeline_month()

        #get Invoice Year Target
        self.get_invoice_year_target()

        #refresh flags
        self.update_refresh_flag()

    #Refresh product datas
    def refresh_product(self):
        self.get_myob_data_products_monthly()
        self.update_refresh_product_flag()

#ALL Combined FUNCTIONALITY
class CombinedBrands:
    #Create database and table
    def create_table_db(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)

            # Create A Cursor
            c = conn.cursor()

            # Create A Table myob_computed_invoice
            c.execute("""CREATE TABLE if not exists combined_myob_computed_invoice(
                ID INTEGER PRIMARY KEY,
                invoice_sales INTEGER,
                order_date timestamp)
                """)

            # Create A Table myob_pipeline
            c.execute("""CREATE TABLE if not exists combined_myob_pipeline(
                ID INTEGER PRIMARY KEY,
                order_sales INTEGER,
                start_date timestamp)
                """)
            
            # Create A Table combined invoice year target
            c.execute("""CREATE TABLE if not exists combined_invoice_year_target(
                ID INTEGER PRIMARY KEY,
                invoice_sales INTEGER,
                order_date timestamp)
                """)

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Insert Combined Computed Invoice
    def insert_combined_invoice(self, order_sales, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            c.execute("INSERT INTO combined_myob_computed_invoice (invoice_sales, order_date) VALUES (?, ?)", (order_sales, order_date))          

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get Combined Computed Invoice
    def get_computed_invoice_pr(self, today):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM purific_myob_computed_invoice WHERE order_date BETWEEN '%s' AND '%s'"%(today, today))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    invoice_sales = record[1]
                    return invoice_sales

            else:
                return 0


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Delete Combined Invoice Data
    def delete_combined_invoice(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Delete Record
            c.execute("DELETE FROM combined_myob_computed_invoice")         


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get Combined Computed Invoice
    def get_combined_computed_invoice(self):
        self.delete_combined_invoice()
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM tegral_myob_computed_invoice")
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    invoice_sales = record[1]
                    order_date = record[2]
                    pr_invoice_sales = self.get_computed_invoice_pr(order_date)
                    total = pr_invoice_sales + invoice_sales
                    self.insert_combined_invoice(total, order_date)

            else:
                pass
        except Error as e:
            print(e)

    #Get Combined Computed Invoice
    def get_computed_pipeline_pr(self, today):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM purific_myob_pipeline WHERE start_date BETWEEN '%s' AND '%s'"%(today, today))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    invoice_sales = record[1]
                    return invoice_sales

            else:
                return 0


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Insert Combined Computed Pipeline
    def insert_combined_pipeline(self, order_sales, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            c.execute("INSERT INTO combined_myob_pipeline (order_sales, start_date) VALUES (?, ?)", (order_sales, order_date))          

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Delete Combined Pipeline Data
    def delete_combined_pipeline(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Delete Record
            c.execute("DELETE FROM combined_myob_pipeline")         


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get Combined Computed Invoice
    def get_combined_computed_pipeline(self):
        try:
            self.delete_combined_pipeline()
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM tegral_myob_pipeline")
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    pipeline_sales = record[1]
                    order_date = record[2]
                    pr_pipeline_sales = self.get_computed_pipeline_pr(order_date)
                    total = pr_pipeline_sales + pipeline_sales
                    #print(total)
                    self.insert_combined_pipeline(total, order_date)

            else:
                pass


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get Purific / Tegral Year Target
    def get_tg_pr_year_target(self, table, today, output='sales'):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM %s_invoice_year_target WHERE order_date BETWEEN '%s' AND '%s'"%(table, today, today))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    if output == 'sales':
                        return record[1]
                    else:    
                        return record[2]
            else:
                return 0


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()    
        except Error as e:
            print(e)

    #Insert invoice_year_target
    def insert_invoice_year_target(self, order_sales, order_date):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Add A Record
            c.execute("INSERT INTO combined_invoice_year_target (invoice_sales, order_date) VALUES (?, ?)", (order_sales, order_date))          

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Delete invoice_year_target
    def delete_invoice_year_target(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Delete Record
            c.execute("DELETE FROM combined_invoice_year_target")         


            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get and Update data from DB based on year target
    def get_invoice_year_target(self): 
        self.delete_invoice_year_target()
        for num in range(1, last_day_month + 1):
            if num > 9: 
                final_num = num
            else:
                final_num = "0%s"%num   
            
            start_date = "%s-%s-%s"%(current_year, month_num, final_num)
            tg_sales = self.get_tg_pr_year_target('tegral', start_date, 'sales')
            pr_sales = self.get_tg_pr_year_target('purific', start_date, 'sales')
            combined_sales = tg_sales + pr_sales
            self.insert_invoice_year_target(combined_sales, start_date)
            print('Date: ', start_date)   
            print('Combined sales: ', combined_sales) 
    def get_data(self, type):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            if type == 'sales':
                c.execute("SELECT * FROM combined_myob_computed_invoice WHERE order_date BETWEEN '%s' AND '%s'"%(start_date, last_date))
            elif type == 'pipeline':
                c.execute("SELECT * FROM combined_myob_pipeline WHERE start_date BETWEEN '%s' AND '%s'"%(start_date, last_date))
            elif type == 'yeartarget':
                c.execute("SELECT * FROM combined_invoice_year_target WHERE order_date BETWEEN '%s' AND '%s'"%(start_date, last_date))
            return c.fetchall()
        except Error as e:
            print(e)

    #Refresh DB
    def refresh(self):
        #get and insert combined invoice
        self.get_combined_computed_invoice()

        #get and insert combined pipeline
        self.get_combined_computed_pipeline()
        
        #Get and Update data from DB based on year target
        self.get_invoice_year_target()

class Forms:
       #Create database and table
    def create_db_table(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)

            # Create A Cursor
            c = conn.cursor()

            # Create A Table myob_invoice
            c.execute("""CREATE TABLE if not exists users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username varchar(50) NOT NULL,
                password varchar(255) NOT NULL,
                email varchar(255) NOT NULL)
                """)

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()   
        except Error as e:
            print(e)

    def check_username(self, username):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT username FROM users WHERE username='%s'"%(username))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    return record[0]
            else:
                return 0

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    def check_password(self, username, password):
        try:
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT password FROM users WHERE username='%s'"%(username))
            records = c.fetchall()

            # Loop thru records
            if records:
                for record in records:
                    if pbkdf2_sha256.verify(password, record[0]):
                        return record[0]
                    
            else:
                return 0

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    def change_password(self, username, password):
        try:
            hashed = pbkdf2_sha256.hash(password)

            conn = sqlite3.connect(db_file)

            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
             # Grab records from database
            c.execute("UPDATE users SET password = '%s' WHERE username = '%s'"%(hashed, username))

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

class Pipedrive:
    #Pipedrive Token
    pipedrive_token = "5dd8a978276443f93d971f5bf17436190a16f484"

    #get monday for this week
    pipe_today = pendulum.now()
    pipe_today_week_start = pipe_today.start_of('week')
    pipe_today_week_end = pipe_today.end_of('week')
    pipe_monday = pipe_today_week_start.to_datetime_string()
    pipe_sunday = pipe_today_week_end.to_datetime_string()
    
    #Create database and table
    def create_db(self):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)

            # Create A Cursor
            c = conn.cursor()

            # Create A pipedrive call logs
            c.execute("""CREATE TABLE if not exists pipedrive_call_logs(
                ID INTEGER PRIMARY KEY,
                call_id TEXT,
                done TEXT,
                type TEXT,
                add_time timestamp,
                marked_as_done_time timestamp,
                subject TEXT,
                org_name TEXT,
                person_name TEXT,
                owner_name TEXT,
                type_name TEXT)
                """) 
            
            # Create A pipedrive callers status
            c.execute("""CREATE TABLE if not exists pipedrive_callers(
                ID INTEGER PRIMARY KEY,
                caller_id INTEGER,
                caller_name TEXT,
                success_status INTEGER,
                attempt_status INTEGER,
                voicemail_status INTEGER)
                """) 

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #Get pipedrive Count
    def get_pipedrive_count(self, filter_id):
        try:
            url_pipe = "https://api.pipedrive.com/v1/persons?filter_id=%s&get_summary=1&api_token=%s"%(filter_id, self.pipedrive_token)

            payload={}
            headers = {
            'Accept': 'application/json'
            }

            response = requests.request("GET", url_pipe, headers=headers, data=payload)
            json_response = response.json()
            added_data = json_response['additional_data']
            return added_data['summary']['total_count']
        except:
            return 0
    
    #insert call logs
    def insert_call_logs(self, call_id, done, type, add_time, marked_as_done_time, subject, org_name, person_name, owner_name, type_name):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
  
            # Add A Record
            c.execute("INSERT INTO pipedrive_call_logs (call_id, done, type, add_time, marked_as_done_time, subject, org_name, person_name, owner_name, type_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(call_id, done, type, add_time, marked_as_done_time, subject, org_name, person_name, owner_name, type_name))    

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)
    
    #update call logs
    def update_call_logs(self, call_id, done, type, add_time, marked_as_done_time, subject, org_name, person_name, owner_name, type_name):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()    
             # Update A Record   
            c.execute("UPDATE pipedrive_call_logs SET done = '%s', type = '%s', add_time = '%s', marked_as_done_time = '%s', subject = '%s', org_name = '%s', person_name = '%s', owner_name = '%s', type_name = '%s' WHERE call_id = '%s'"%(done, type, add_time, marked_as_done_time, subject, org_name, person_name, owner_name, type_name, call_id)) 
            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)
    
    #check if call id exists
    def check_call_id_exists(self, call_id, done, type, add_time, marked_as_done_time, subject, org_name, person_name, owner_name, type_name):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM pipedrive_call_logs WHERE call_id='%s'"%(call_id))
            records = c.fetchall()

            # Loop thru records
            if records:
                self.update_call_logs(call_id, done, type, add_time, marked_as_done_time, subject, org_name, person_name, owner_name, type_name)
            else:
                self.insert_call_logs(call_id, done, type, add_time, marked_as_done_time, subject, org_name, person_name, owner_name, type_name)

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)
    
    #get call logs successfull
    def get_call_logs_success_call(self, type):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
            
            # Grab records from database
            c.execute(f"SELECT count(type_name) FROM pipedrive_call_logs WHERE type_name='{type}' AND marked_as_done_time < '{self.pipe_sunday}' GROUP BY owner_name ORDER BY owner_name DESC")
            records = c.fetchall()
            # Loop thru records
            if records:
                return records
                #for record in records:
                    #print(record[0])
            else:
                return 0
        except Error as e:
            print(e)

    #get call logs graph
    def get_caller_graph(self, field_name):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
            c.execute(f"SELECT {field_name} FROM pipedrive_callers")
            records = c.fetchall()
            # Loop thru records
            if records:
                return records
            else:
                return 0
        except Error as e:
            print(e)

    #insert callers
    def insert_callers(self, caller_id, caller_name):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()
  
            # Add A Record
            c.execute("INSERT INTO pipedrive_callers (caller_id, caller_name, success_status, attempt_status, voicemail_status) VALUES (?, ?, ?, ?, ?)",(caller_id, caller_name, 0, 0, 0))    

            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #update callers
    def update_callers(self, caller_id, caller_name):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()    
             # Update A Record   
            c.execute("UPDATE pipedrive_callers SET caller_id = '%s', caller_name = '%s', success_status = '%s', attempt_status = '%s', voicemail_status = '%s' WHERE caller_id = '%s' "%( caller_id, caller_name, 0, 0, 0, caller_id)) 
            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)
    
    #check if caller exists
    def check_caller_exists(self, caller_id, caller_name):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()

            # Grab records from database
            c.execute("SELECT * FROM pipedrive_callers WHERE caller_id='%s'"%(caller_id))
            records = c.fetchall()

            # Loop thru records
            if records:
                self.update_callers(caller_id, caller_name)
            else:
                self.insert_callers(caller_id, caller_name)

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)

    #get all callers
    def get_callers(self):
        try:
            payload={}
            headers = {
            'Accept': 'application/json'
            }

            url_logs = f"https://api.pipedrive.com/v1/users?api_token={self.pipedrive_token}"
            response = requests.request("GET", url_logs, headers=headers, data=payload)

            json_response = response.json()
            items = json_response['data']
            if items:
                for item in items:
                    caller_id = item.get("id")
                    caller_name = item.get("name")
                    status = item.get("active_flag")
                    if status == 1: 
                        #pass
                        self.check_caller_exists(caller_id, caller_name)
                    print(caller_id)
                    print(caller_name)
            else:
                pass
        except requests.Timeout as errtim:
            print ("Timeout Error: ", errtim)
        except requests.ConnectionError as errcon:
            print ("Connection Error: ", errcon)
    
    #update callers
    def update_callers_increment(self, caller_id, status_type):
        try:
            # Create Database Or Connect To One
            conn = sqlite3.connect(db_file)
            # Create A Cursor
            c = conn.cursor()    
            # Update A Record   
            if status_type == 'success': 
                c.execute("UPDATE pipedrive_callers SET success_status = success_status + 1 WHERE caller_id = '%s' "%(caller_id)) 
            elif status_type == 'attempt': 
                c.execute("UPDATE pipedrive_callers SET attempt_status = attempt_status + 1 WHERE caller_id = '%s' "%(caller_id)) 
            else:
                c.execute("UPDATE pipedrive_callers SET voicemail_status = voicemail_status + 1 WHERE caller_id = '%s' "%(caller_id)) 
            # Add a little message
            print('Done adding')

            # Commit our changes
            conn.commit()

            # Close our connection
            conn.close()
        except Error as e:
            print(e)       

    #get call logs
    def get_call_logs(self):
        try:
            payload={}
            headers = {
            'Accept': 'application/json'
            }
            url_logs = f"https://api.pipedrive.com/v1/recents?items=activity&start=0&limit=500&since_timestamp={self.pipe_monday}&api_token={self.pipedrive_token}"
            response = requests.request("GET", url_logs, headers=headers, data=payload)
            json_response = response.json()
            items = json_response['data']
            if items:
                for item in items:
                    call_id = item.get("data").get("id")
                    done = item.get("data").get("done")
                    type = item.get("data").get("type")
                    add_time = item.get("data").get("add_time")
                    marked_as_done_time = item.get("data").get("marked_as_done_time")
                    subject = item.get("data").get("subject")
                    org_name = item.get("data").get("org_name")
                    person_name = item.get("data").get("person_name")
                    owner_name = item.get("data").get("owner_name")
                    type_name = item.get("data").get("type_name")
                    caller_id = item.get("data").get("user_id")
                    if marked_as_done_time:
                        self.check_call_id_exists(call_id, done, type, add_time, marked_as_done_time, subject, org_name, person_name, owner_name, type_name)
                        if type_name == 'Successful Call':
                            self.update_callers_increment(caller_id, 'success')
                        elif type_name == 'Attempted Call':
                            self.update_callers_increment(caller_id, 'attempt')
                        elif type_name == 'VoiceMail':
                            self.update_callers_increment(caller_id, 'voicemail')
                    print(org_name)
            else:
                pass
        except requests.Timeout as errtim:
            print ("Timeout Error: ", errtim)
        except requests.ConnectionError as errcon:
            print ("Connection Error: ", errcon)

    #refresher
    def refresh(self):
        self.get_callers()
        self.get_call_logs()

#TESTER AREA
#password = pbkdf2_sha256.hash("password")
#password2 = pbkdf2_sha256.hash("password")

#print(password)
##print(password2)

#print(pbkdf2_sha256.verify("password", password))
#model_tegral = Brands('tegral')
#model_tegral.get_product_update_category('yearly')
#model_tegral.get_product_update_category('monthly')
#model_tegral.get_myob_data_products_monthly()
#print(last_date)
#model_purific = Brands('purific')
#print(model_purific.get_myob_orders_computed_whole_month())

#print(model_tegral.get_year_target_sales('Angles - 1050mm'))
#model_tegral.get_myob_data_products_monthly()
#model_tegral.get_month_target_sales(self, 'LOAD ')
#model_tegral.get_product_monthly_base_cat('category')
#model_tegral.get_product_categories()

#form = Forms()
#print(form.check_password('jerome25','jeromejerome2015'))

#print(current_month)

#pipe = Pipedrive()
#pipe.get_call_tester()
#pipe.get_callers()
#pipe.create_db()
#pipe.get_call_logs()
#pipe.get_call_logs_success_call()

#pipe.get_call_logs_callers()


#print(yesterday)











