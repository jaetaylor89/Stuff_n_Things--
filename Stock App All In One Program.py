# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 18:14:29 2021

@author: Jae
"""

import tkinter
from datetime import datetime
from stock_class import Stock, DailyData
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import matplotlib.pyplot as plt
import json
import pandas as pd
import stock_class
from datetime import datetime
from stock_class import Stock, DailyData
from Account_Class import  Traditional, Robo

class Stock:
    def __init__(self, symbol, name, shares):
        self.symbol = symbol
        self.name = name
        self.shares = shares
        self.DataList = [] #List of DailyData class
      
   # Add stock data
    def add_data(self, stock_data):
        self.DataList.append(stock_data)
    
         
    #Add DailyData Class
class DailyData:
    def __init__(self, date, close, volume):
        self.date = date
        self.close = close #Closing volume for stock trade
        self.volume = volume # Daily volume
        
 ########################################################################
        
class Retirement_Account:
    def __init__(self, balance, number):
        self.balance = balance
        self.number = number
        
  #Create Traditional Account      
class Traditional(Retirement_Account):
    def __init__(self, balance, number):
        Retirement_Account.__init__(self, balance, number)
        self.Stock_List = []
    

    def add_stock (self, stock_data):
            self.Stock_List.append(stock_data)
            self.Stock_List.append(stock_data)
        
    #Create Robo Account    
class Robo(Retirement_Account):
    def __init__(self, balance, number, years):
        Retirement_Account.__init__(self, balance, number)
        self.years = years
        
  #Investment Return      
    def investment_return(self):
        return self.years * self.balance * 1.05
    
    
    #######################################################################
    
    
def add_stock(stock_list):      
    option = ""
    while option != "0":
        print("Add stock")
        symbol = input("Enter symbol: ").upper()
        name = input("Enter company name: ")
        shares = float(input("Enter shares: "))
        new_stock = Stock(symbol,name,shares)
        stock_list.append(new_stock)
        option = input("Press to add new stock or 0 to quit: ")
        
        
        
# Delete Stock
def delete_stock(stock_list):    
    print("Delete Stock")
    print("Stock List: [", end= "")
    for stock in stock_list:
        print(stock.symbol, " ", end= "")
    print("]")
    symbol = input("Which stock would you like to delete?: ").upper()
    found = False
    i = 0
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            stock_list.pop(i)
        i = i + 1
    if found == True:
        print("Deleted ", symbol)
    else:
        print("Symbol not found")
    _ = input("Press enter to continue") 
    
    
    
# List Stocks Being Traked
def list_stocks(stock_list):
    print("Stock list")
    print("SYMBOL\t\tNAME\t\tSHARES")
    print("========================================")
    for stock in stock_list:
    	print(stock.symbol, " " *(14-len(stock.symbol)), stock.name, " " *(14-len(stock.name)), stock.shares)   
    print()
    _ = input("Press enter to continue")
    
    
    
# Add Daily Stock data
def add_stock_data(stock_list):
    print("Add Daily Stock Data ----")
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol," ",end="")
    print("]")
    symbol = input("Which stock do you want to use?:").upper()
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            current_stock = stock
    if found == True:
        print("Ready to add data for: ",symbol)
        print("Enter Data Separated by Commas - Do Not Use Spaces")
        print("Enter a Blank Line to Quit")
        print("Enter Date,Prince,Volume")
        print("Example: 8/28/20,54.45,20440")
        data = input("Enter date,Price,Volume:")
        while data != "":
            date, price, volume = data.split(",")
            daily_data = DailyData(date, float(price), float(volume))
            
            current_stock.add_data(daily_data)
            data = input("Enter Date,Price,Volume: ")
        print("Date Entry Complete")
    else:
        print("Symbol Not Found ***")
    _ = input("Press Enter to Continue ***")
    


# Investment Type, Via Account Type
def investment_type(stock_list):
    print("Investment Account ---")
    balance = float(input("What is your initial balance: "))
    number = input("Enter your account number: ")
    acct = input("Select Traditional (t) or Robo (r) account: ")
    if acct.lower() == "r":
        years = float(input("Enter years until retirement:"))
        robo_acct = Robo(balance, number, years)
        print("Current Investment Return ", robo_acct.investment_return())
        print("\n\n")
    elif acct.lower() =="t":
        trad_acct = Traditional(balance, number)
        temp_list = []
        print("Choose Stocks From List Below: ")
        while True:
            print("Stock List: [",end ="")
            for stock in stock_list:
                print(stock.symbol," ",end="")
            print("]")
            symbol = input("Which stock would you like to purchase, 0 to quit: ").upper()
            if symbol =="0":
                break
            shares = float(input("Select Purchase Quantity: "))
            found = False
            for stock in stock_list:
                if stock.symbol == symbol:
                    found = True
                    current_stock = stock
            if found == True:
                current_stock.shares += shares
                temp_list.append(current_stock)
                print("Bought ", shares, "of", symbol)
            else:
                print("Symbol Not Found ***")
        trad_acct.add_stock(temp_list)
        
        
        
# Function to create stock chart
def display_stock_chart(stock_list, symbol):
    date = []
    price = []
    volume = []
    company = []
    for stock in stock_list:
        
        if stock.symbol == symbol:
            company = stock.name
            for DailyData in stock.DataList:
                date.append(DailyData.date)
                price.append(DailyData.close)      
                volume.append(DailyData.volume)
    plt.plot(date,price)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(company)
    plt.show() 
    
    

#Display Chart
def display_chart(stock_list):
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol," ",end="")
    print("]")
    symbol = input("Select the Stock You Would Like to Use: ").upper()
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            current_stock = stock
    if found == True:
        display_stock_chart(stock_list, current_stock.symbol)
    else:
        print("Symbol Not Found")
        _ = input("Press Enter to Continue")
 



# Object Decoder & Encoder
def data_encoder(obj):
    data_dict = dict(date=obj.date, close = obj.close, volume = obj.volume)
    return data_dict

def obj_encoder(obj):
        dlist = []
        for o in obj.DataList:
            d = data_encoder(o)
            dlist.append(d)
        stock_dict = dict(symbol=obj.symbol, name = obj.name, shares = obj.shares, DataList = dlist)
        return stock_dict
    
    

def obj_decoder(obj):
        symbol = obj["symbol"]
        name = obj["name"]
        shares = obj["shares"]
        DL = obj["DataList"]
        objStock = Stock(symbol, name, shares)
        for o in DL:
            d = o['date']
            c = o['close']
            v = o['volume']
            dd = DailyData(d,c,v)
            objStock.add_data(dd)
        return objStock
    


# File Processing
def file_processing(stock_list):
    json_dict = {}
    choice = ""
    while choice == "":    
        choice = input("Select Save Data (S), Load Data (D), Import Data (I), Exit (E): ")
        if choice == "S":
            # Encode Stock Data as Python Dictionary
            json_list = [obj_encoder(stock) for stock in stock_list]
            json_dict["Stock"] = json_list
            # Save Stock to stock_data.json
            try:
                with open("stock_data.json","w") as f:
                    json.dump (json_dict, f, indent = 4)
                print("\nData Saved to stock_data.json--")
            except IOError:
                print("File Not Created")
        elif choice =="D":
            try:
                with open("stock_data.json","r") as f:
                    str_file = f.read()
                    str_file = str_file.replace("\'",  "\"")
                    stock_obj = json.loads(str_file)
                    for s in stock_obj["Stock"]:
                        temp = obj_decoder(s)
                        stock_list.append(temp)
                        # Add to the stock_list
                print("\nData Loaded From stock_list.json")
            except IOError:
                print("file Not Found")
                break
        elif choice == "I":
            print("\nAdd Historical Data to a Stock in the Stock List--")
            symbol = input("Enter ticker symbol: ").upper()
            filename = input("Enter the File Name: ")
            import_stock_csv(stock_list, symbol, filename)              
            display_report(stock_list, symbol)
            
                

# Get Price and Volume History from Yahoo! Finance Using CSV Impot                
def import_stock_csv(stock_list,symbol,filename):
    for stock in stock_list:
        if stock.symbol == symbol:
            with open(filename, newline='') as stockdata:
                datareader = csv.reader(stockdata,delimiter=',')
                next(datareader)
                for row in datareader:
                    daily_data = DailyData(str(row[0]),float(row[4]),float(row[6]))
                    stock.add_data(daily_data)


        
# Display Roport for Stock (imported data)
def display_report(stock_list, symbol):
    currentDate=datetime.now()
    print("Stock Report ---")
    for stock in stock_list:
        if stock.symbol == symbol:
            print("Report for: ",stock.symbol,stock.name)
            print("Shares: ", stock.shares)
            count = 0
            price_total = 0.00
            volume_total = 0
            lowPrice = 999999.99
            highPrice = 0.00
            lowVolume = 999999999999
            highVolume = 0
            startDate = datetime.strptime("12/31/2099","%m/%d/%Y")
            endDate = datetime.strptime("1/1/1900","%m/%d/%Y")
            for daily_data in stock.DataList: 
                currentDate= datetime.strptime(daily_data.date,"%Y-%m-%d")
                count = count + 1
                price_total = price_total + daily_data.close
                volume_total = volume_total + daily_data.volume
                if daily_data.close < lowPrice:
                    lowPrice = daily_data.close
                if daily_data.close > highPrice:
                    highPrice = daily_data.close
                if daily_data.volume < lowVolume:
                    lowVolume = daily_data.volume
                if daily_data.volume > highVolume:
                    highVolume = daily_data.volume
                if currentDate < startDate:
                    startDate = currentDate
                    startPrice = daily_data.close
                if currentDate > endDate:
                    endDate = currentDate
                    endPrice = daily_data.close
                priceChange = endPrice-startPrice
                print(daily_data.date,daily_data.close,daily_data.volume)
            if count > 0:
                print("Summary ---",startDate,"to",endDate)
                print("Low Price:", "${:,.2f}".format(lowPrice))
                print("High Price:", "${:,.2f}".format(highPrice))
                print("Average Price:", "${:,.2f}".format(price_total/count))
                print("Low Volume:", lowVolume)
                print("High Volume:", highVolume)
                print("Average Volume:", "${:,.2f}".format(volume_total/count))
                print("Starting Price:", "${:,.2f}".format(startPrice))
                print("Ending Price:", "${:,.2f}".format(endPrice))
                print("Change in Price:", "${:,.2f}".format(priceChange))
                print("Profit/Loss","${:,.2f}".format(priceChange * stock.shares))
            else:
                print("*** No daily history.")
            print("\n\n\n")
    print("--- Report Complete ---")
    _ = input("Press Enter to Continue")
    


def update_shares(stock_list):
    option = ""
    while option != "0":
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option: ")
        while option not in ["1", "2", "0"]:
            print("*** Invalid Option - Try Again ***")
            print("Update Shares ---")
            print("1 - Buy Shares")
            print("2 - Sell Shares")
            print("0 - Exit Update Shares")
            option = input("Enter Menu Option: ")
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)
        elif option == "0":
            print("Returning to Main Menu")
            
            
            
# Buy Stocks (add to shares) 
def buy_stock(stock_list):
    print("Buy Shares ---")
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol," ",end="")
    print("]")
    symbol = input("Select Stock for Purchase: ").upper()
    shares = float(input("Enter Stock Quantity: "))
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            stock.buy(shares)
    if found == True:
        print("Successfully Added ",shares,"of",symbol)
    else: 
        print("Symbol Not Found ***")
    _ = input("Press Enter to Continue ***")
    
    
    
    # Sell Stock (subtract from shares)
def sell_stock(stock_list):
    print("Sell Shares ---")
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol," ",end="")
    print("]")
    symbol = input("Select the Stock You Would Like to Sell: ").upper()
    shares = float(input("Enter Stock Quantity:"))
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            stock.sell(shares)
    if found == True:
        print("Sold ",shares,"of",symbol)
    else: 
        print("Symbol Not Found ***")
    _ = input("Press Enter to Continue ***")
            
    
    
# Main Menu
def main_menu(stock_list):    
    option = ""    
    while True:        
        print("Stock Analyzer ---")        
        print("1 - Add Stock")        
        print("2 - Delete Stock")        
        print("3 - List stocks")        
        print("4 - Add Daily Stock Data (Date, Price, Volume)")        
        print("5 - Show Chart")        
        print("6 - Investor Type")        
        print("7 - Save/Load Data")        
        print("0 - Exit Program")        
    
        option = input("Enter Menu Option: ")        
        if option =="0":            
            print("Goodbye")            
            break
            
        if option == "1":            
            add_stock(stock_list)
        elif option == "2":
            delete_stock(stock_list)
        elif option == "3":   
            list_stocks(stock_list)
        elif option == "4":           
            add_stock_data(stock_list)
        elif option == "5":            
            display_chart(stock_list)
        elif option == "6":            
            investment_type(stock_list)
        elif option == "7":            
            file_processing(stock_list)
        else: 
            print("Goodbye")
                
        # Begin program
def main():
    stock_list = []
    main_menu(stock_list)
                
        # Program Starts Here
if __name__ == "__main__": # execute only if run as a stand-alone script    
    main()
    
    
 ######################################################################################3   
    
    
class StockApp:
    def __init__(self):
        self.stock_list = []

        
        
        # Create Window
        self.root = Tk()
        self.root.title("Stock Manager")
      
        # Add Menu
        self.menubar = Menu(self.root)

        self.filemenu = Menu(self.menubar, tearoff=0)

        
        self.webmenu = Menu(self.menubar, tearoff=0)
        self.webmenu.add_command(label = "Import CSV from Yahoo! Finance...", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web",menu=self.webmenu)

        self.chartmenu = Menu(self.menubar,tearoff=0)
        self.chartmenu.add_command(label="Display Stock Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart",menu=self.chartmenu)


        self.root.config(menu=self.menubar)

        # Add heading information
        self.headingLabel = Label(self.root,text="No Stock Selected")
        self.headingLabel.grid(column=0,row=0,columnspan=3,padx = 5, pady = 10)
        

        # Add stock list
        self.stockLabel = Label(self.root,text="Stocks")
        self.stockLabel.grid(column=0,row=1,padx = 5, pady = 10,sticky=(N))

        self.stockList = Listbox(self.root)
        self.stockList.grid(column=0,row=2,padx = 5, pady = 5,sticky=(N,S))
        self.stockList.bind('<<ListboxSelect>>',self.update_data)
        
        
        # Add Tabs
        self.notebook = ttk.Notebook(self.root,padding="5 5 5 5")
       
        self.notebook.grid(column=2,row=2,sticky=(N,W,E,S))
        self.mainFrame = ttk.Frame(self.notebook)
        self.stockDataFrame = ttk.Frame(self.notebook)
        self.reportFrame = ttk.Frame(self.notebook)
        self.chartFrame = ttk.Frame(self.notebook)
        self.notebook.add(self.mainFrame,text='Manage')
        self.notebook.add(self.stockDataFrame,text='History')
        self.notebook.add(self.reportFrame,text = 'Report')
        

        # Set Up Main Tab
        self.addStockGroup = LabelFrame(self.mainFrame,text="Add Stock",padx=5,pady=5)
        self.addStockGroup.grid(column=0,row=0,padx=5,pady=5,sticky=(W,E))
     
        self.addSymbolLabel = Label(self.addStockGroup,text = "Symbol")
        self.addSymbolLabel.grid(column=0,row=0,padx = 5, pady = 5,sticky=(W))
        self.addSymbolEntry = Entry(self.addStockGroup)
        self.addSymbolEntry.grid(column=1,row=0,padx=5,pady=5)

        self.addNameLabel = Label(self.addStockGroup,text = "Name")
        self.addNameLabel.grid(column=0,row=1,padx = 5, pady = 5,sticky=(W))
        self.addNameEntry = Entry(self.addStockGroup)
        self.addNameEntry.grid(column=1,row=1,padx=5,pady=5)

        self.addSharesLabel = Label(self.addStockGroup,text = "Shares")
        self.addSharesLabel.grid(column=0,row=2,padx = 5, pady = 5,sticky=(W))
        self.addSharesEntry = Entry(self.addStockGroup)
        self.addSharesEntry.grid(column=1,row=2,padx=5,pady=5)

        self.addStockButton = Button(self.addStockGroup,text = "New Stock",command=self.add_stock)
        self.addStockButton.grid(column=0,row=3,columnspan = 2, padx = 5, pady = 5)


        self.deleteGroup = LabelFrame(self.mainFrame,text="Delete Stock",padx=5,pady=5)
        self.deleteGroup.grid(column=0,row=2,padx=5,pady=5,sticky=(W,E))

        self.deleteStockButton = Button(self.deleteGroup,text="Delete Selected Stock",command=self.delete_stock)
        self.deleteStockButton.grid(column=0,row=0,padx=5,pady=5)



        # Setup History Tab
        self.dailyDataList = Text(self.stockDataFrame,width=40)
        self.dailyDataList.grid(column=0,row=0,padx = 5, pady = 5)
        
        


        # Setup Report Tab
        self.stockReport = Text(self.reportFrame,width=40)
        self.stockReport.grid(column=0,row=0,padx=5,pady=5)

        self.root.mainloop()

 

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                self.dailyDataList.insert(END,"- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END,"=================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END,row)
                    currentDate= datetime.strptime(daily_data.date,"%Y-%m-%d")
                #display report
                count = 0
                price_total = 0.00
                volume_total = 0
                lowPrice = 999999.99
                highPrice = 0.00
                lowVolume = 999999999999
                highVolume = 0
    
                for daily_data in stock.DataList:
                    count = count + 1
                    price_total = price_total + daily_data.close
                    volume_total = volume_total + daily_data.volume
                    if daily_data.close < lowPrice:
                        lowPrice = daily_data.close
                    if daily_data.close > highPrice:
                        highPrice = daily_data.close
                    if daily_data.volume < lowVolume:
                        lowVolume = daily_data.volume
                    if daily_data.volume > highVolume:
                        highVolume = daily_data.volume
    
                    priceChange = lowPrice-highPrice
                    
                if count > 0:
                    self.stockReport.insert(END,"Summary Data--\n\n")
                    self.stockReport.insert(END,"Low Price: " + "${:,.2f}".format(lowPrice) + "\n")
                    self.stockReport.insert(END,"High Price: " + "${:,.2f}".format(highPrice) + "\n")
                    self.stockReport.insert(END,"Average Price: " + "${:,.2f}".format(price_total/count) + "\n\n")
                    self.stockReport.insert(END,"Low Volume: " + str(lowVolume) + "\n")
                    self.stockReport.insert(END,"High Volume: " + str(highVolume) + "\n")
                    self.stockReport.insert(END,"Average Volume: " + "${:,.2f}".format(volume_total/count) + "\n\n")
                    self.stockReport.insert(END,"Change in Price: " + "${:,.2f}".format(priceChange) + "\n")
                    self.stockReport.insert(END,"Profit/Loss: " + "${:,.2f}".format(priceChange * stock.shares) + "\n")
                else:
                    self.stockReport.insert(END,"*** No daily history.") 
    
    # Add new stock to track.
    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get(), self.addNameEntry.get(), float(self.addSharesEntry.get()))
        self.stock_list.append(new_stock)
        self.stockList.insert(END, self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0, END)
        self.addNameEntry.delete(0, END)
        self.addCharesEntry.delete(0, END) 


    # Remove stock and all history from being tracked.
    def delete_stock(self):
        symbol = self.stockLabel.get(self.stockList.curselection())
        i = 0
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stock_list.poop(i)
            i = i+1
        self.display_stock_data()
        self.stockList.delete(0, END)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)
        messagebox.showinfo("Stock Dleted", symbol, "Removed") 



      # Get price and volume history from Yahoo! Finance using CSV import.
    def import_stock_csv(self,stock_list,symbol,filename):
        for stock in stock_list:
                if stock.symbol == symbol:
                    with open(filename, newline='') as stockdata:
                        datareader = csv.reader(stockdata,delimiter=',')
                        next(datareader)
                        for row in datareader:
                            daily_data = DailyData(str(row[0]),float(row[4]),float(row[6]))
                            stock.add_data(daily_data)   

    # Import CSV stock history file.
    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            self.import_stock_csv(self.stock_list,symbol,filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + "Import Complete")   
    
    # Display stock price chart.
    def display_chart(self):
        symbol = self.stockList.get(self.stockList.curselection())   
        date = []
        price = []
        volume = []
        company = ""
        for stock in self.stock_list:
            if stock.symbol == symbol:
                company = stock.name
                for dailyData in stock.DataList:
                    date.append(dailyData.date)
                    price.append(dailyData.close)
                    volume.append(dailyData.volume)
                plt.plot(date,price)
                plt.xlabel('Date')
                plt.ylabel('Price')
                plt.title(company)
                plt.show() 



        
    
    

def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()