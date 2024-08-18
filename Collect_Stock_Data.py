import yfinance as yf
import pandas_datareader as pdr
import datetime
from alpha_vantage.timeseries import TimeSeries
import time
import os
import pandas as pd
from datetime import datetime, timedelta




def yFinanceTrial(ticker_symbol): #user-friendly and does not require an API key.
    # Define the ticker symbol
    #ticker_symbol = 'AAPL'

    # Get the data
    ticker_data = yf.Ticker(ticker_symbol)

    # Get historical market data
    #ticker_df = ticker_data.history(period='1mo', start='2023-07-01', end='2024-08-01')

    ticker = ticker_data.history(period="1d", interval="1m", auto_adjust=False)
    print(ticker)

    # Display the data
    #print(ticker_df)

    # Get basic information
    info = ticker.info

    # Access specific data
    current_price = info['currentPrice']
    market_cap = info['marketCap']
    sector = info['sector']

    #print(f"Current Price: {current_price}")
    #print(f"Market Cap: {market_cap}")
    #print(f"Sector: {sector}")
    consolidate_data = sector, current_price, market_cap
    print(consolidate_data)
    return str(consolidate_data)

def pandas_datareadertrial(): #
    # Define the ticker symbol
    ticker_symbol = 'AAPL'

    # Define the date range
    start_date = datetime.datetime(2023, 7, 1)
    end_date = datetime.datetime(2024, 8, 1)

    # Fetch the data from Yahoo Finance
    stock_data = pdr.get_data_enigma(ticker_symbol, start=start_date, end=end_date)

    # Display the data
    print(stock_data)

def TimeSeriesTrial(): #requires an API key but provides more extensive data
    # Define your API key
    api_key = 'your_api_key_here'

    # Create a TimeSeries object
    ts = TimeSeries(key=api_key, output_format='pandas')

    # Get daily data for a specific stock
    data, meta_data = ts.get_daily(symbol='AAPL', outputsize='full')

    # Display the data
    print(data)

def Showoff(max):
    i = 0
    while i <= max:
        # Print the current value of the counter
        yFinanceTrial()
        # Increment the counter
        i += 1
        try:
            time.sleep(1)
        except Exception as e:
            # Print a custom message along with the exception
            print(f"An error occurred: {e}")

def write_df_to_csv(df, file_path, index=False):
    """
    Writes the given DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame to write to CSV.
    file_path (str): The path to the CSV file to create.
    index (bool): Whether to write the DataFrame index to the file. Defaults to False.
    """
    df.to_csv(file_path, index=index)

class Store_Data:
    def Append(df, file_loc):
        df.to_csv(file_loc, mode='a', index=False, header=False)

        with open(file_loc, 'a') as csv_store:
            df.write()
            current_time_utc = time.gmtime()
            formatted_time_utc = time.strftime("%Y-%m-%d %H:%M:%S", current_time_utc)
            line_mark =  f"----------------------------------------{formatted_time_utc}----------------------------------------\n"
            
            try:
                csv_store.write(line_mark)
            except Exception as e:
                print(f"~~~~~~~~~~~~~~~~~~~~~~`the problem is {e}")

    def Write(df, file_loc):
        #df.to_csv(file_loc, columns=['Column1', 'Column2'], index=False)
        #df.to_csv(file_loc, sep='\t', index=False)

        df.to_csv(file_loc, header=True, index=False)  # Include header
        #df.to_csv(file_loc, header=False, index=False)  # Exclude header

        df.to_csv(file_loc, index=True)   # Include index
        #df.to_csv(file_loc, index=False)  # Exclude index

        df.to_csv(df, mode='a', index=False, header=False)

        #df.to_csv('output.csv', na_rep='NA', index=False)  # Replace NaN with 'NA'

        # lambda modifications
        # Example: Format date columns
        #df['DateColumn'] = df['DateColumn'].dt.strftime('%Y-%m-%d')

        # Example: Format numerical columns
        #df['Amount'] = df['Amount'].apply(lambda x: f"${x:,.2f}")

        #df.to_csv(file_loc, index=False)
        
        #df.to_csv(file_loc, index=False)

def comparetimes():
    # Define the ticker symbol
    ticker_symbol = 'AAPL'  # Replace with your desired ticker

    # Fetch intraday data at 1-minute intervals for the last day
    data = yf.download(ticker_symbol, period='1d', interval='1m')

    # Get the last row of data (most recent minute)
    last_minute_data = data.tail(1)

    # Print the most recent minute of data
    print("Last Minute Data:\n", last_minute_data)

    # Print the current date and time for reference
    print("Current Date and Time:", datetime.now())

def MinuteDataTrial():
    # Define the ticker symbol and interval
    ticker_symbol = 'AAPL'  # Replace with the ticker you want
    interval = '1m'  # 1-minute interval
    period = '1d'  # Full day of data

    # Fetch the data
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)

    # Get the last row of data (most recent minute)
    #last_minute_data = data.tail(1)

    # Print the most recent minute of data
    
    print(data)
    #print(last_minute_data)

def WriteToCSV(line_parsed, file_loc):  
    with open(file_loc, 'a') as csv_store:
        current_time_utc = time.gmtime()
        formatted_time_utc = time.strftime("%Y-%m-%d %H:%M:%S", current_time_utc)
        try:
            line_parsed = line_parsed + formatted_time_utc
        except Exception as e:
            print(f"~~~~~~~~~~~~~~~~~~~~~~`the problem is {e}")

        try:
            csv_store.write(str(line_parsed))
        except Exception as e:
            print(f"||~~~~~~~~~~~~~~~~~~~~~~`the problem is {e}")
        
def Tick_List_Collection():
    location = '/Users/adam/Documents/GitHub/NEW-Trading-App/list_of_tickers.txt'
    # Open the file in read mode
    with open(location, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Process the line (e.g., print it)
            #time.sleep(5)
            try: 
                line_parsed = line.strip()
                #print(f"\n---------------Data for {line_parsed}---------------\n\n{yFinanceTrial(str(line_parsed))}")
                #WriteToCSV((f"\t|\t{line_parsed}\t|\t"+ yFinanceTrial(str(line_parsed)) + "\n"), "/Users/adam/Documents/GitHub/NEW-Trading-App/Practice_Stock_Data_Storage")
                Historical_data(line_parsed)
            except Exception as e:
                # Print a custom message along with the exception
                print(f"An error occurred: {e}")
        #WriteToCSV(f"--------------------------------------\n","/Users/adam/Documents/GitHub/NEW-Trading-App/Practice_Stock_Data_Storage")
            
#Tick_List_Collection()
def Collect_Hella_Info():
    day_length = 86400

    i = 0
    while i <= 360:
            # Print the current value of the counter
            Tick_List_Collection()
            # Increment the counter
            i += 1
            try:
                time.sleep(10)
            except Exception as e:
                # Print a custom message along with the exception
                print(f"An error occurred: {e}")

def Historical_data(ticker_symbol):
    ticker_data = yf.Ticker(ticker_symbol)

    # Get historical market data
    #ticker_df = ticker_data.history(period='1mo', start='2023-07-01', end='2024-08-01')

    ticker = ticker_data.history(period="5d", interval="1m", auto_adjust=False)

    line_parsed = ticker
    try: 
        file_loc = f"{os.getcwd()}/Storage_Location/{ticker_symbol}_Historical_Data.csv"
    except Exception as e:
        print(f"An error occurred: {e}")

    Store_Data.Write(line_parsed, file_loc)

class MBM:

    def Minute_by_Minute(ticker, period, interval):
        """
        Fetch minute-by-minute stock data for a given ticker.

        :param ticker: Stock ticker symbol (e.g., 'AAPL')
        :param period: The period for which data should be retrieved (default '1m')
        :param interval: The interval of the data (default '1m' for one minute)
        :return: Pandas DataFrame with stock data
        """
        #time.sleep(60)
        #stock_data = yf.download(ticker, period=period, interval=interval)
        stock_data = yf.download(ticker, period, interval)
        last_row = stock_data.tail(1)

        print(f"most recent data: {last_row}")

        stock_data.index = stock_data.index.tz_localize(None)

        ticker_symbols = []
        location = '/Users/adam/Documents/GitHub/NEW-Trading-App/list_of_tickers.txt'
        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        for ticker_symbol in ticker_symbols:
            with open(location, 'r') as file:
                
            # Iterate through each line in the file
                for line in file:
                    # Process the line (e.g., print it)
                    #time.sleep(5)
                    line = line.strip()
                    ticker_symbols.append(line) # Add more ticker symbols as needed
            filename = f"/Users/adam/Documents/GitHub/NEW-Trading-App/Storage_Location/MBM/{ticker_symbol}_minute_data.csv"
            Store_Data.Append(line, filename)
        return stock_data
    
    #if __name__ == "__main__":
    def runMBM():
        # List of stock ticker symbols
        ticker_symbols = []
        location = '/Users/adam/Documents/GitHub/NEW-Trading-App/list_of_tickers.txt'
        # Open the file in read mode
        with open(location, 'r') as file:
            
        # Iterate through each line in the file
            for line in file:
                # Process the line (e.g., print it)
                #time.sleep(5)
                line = line.strip()
                ticker_symbols.append(line) # Add more ticker symbols as needed

        print(ticker_symbols)

        # Define the duration to run the program (e.g., 4 hours)
        end_time = datetime.now() + timedelta(hours=4)

        # Start the loop
        while datetime.now() < end_time:
            for ticker_symbol in ticker_symbols:
                try:
                    # Fetch minute-by-minute data for the stock
                    data = Minute_by_Minute(ticker_symbol, '1d', '1m')
                    
                    # Save the data to a CSV file (append mode)
                    current_time = datetime.now().strftime("%Y%m%d_%H%M")
                    print(f"current time: {current_time}")
                    filename = f"/Users/adam/Documents/GitHub/NEW-Trading-App/Storage_Location/MBM/{ticker_symbol}_minute_data.csv"
                    
                    
                    #last_row = data.tail(1).to_dict('records')[0]
                    last_row = data.head(1)
                    #first_row = data.head(1) #this is the next problem, we need to get data from the current day, check the day orientation
                    print(f"last row: {last_row}")

                    with open(filename, 'a') as f:
                        f.write(str(last_row)) #i think that this part might be the probelm, try writing it as a 
                        #f.write(f"----------------------------------------{current_time}----------------------------------------")

                    #data.to_csv(filename, mode='a', header=not pd.read_csv(filename).empty if filename else True)
                    Store_Data.Append(last_row, filename)
                    
                    #Store_Data.Append("-----------------------------------", filename)
                    
                    print(f"Collected data for {ticker_symbol} at {current_time}")
                    
                except Exception as e:
                    print(f"Error collecting data for {ticker_symbol}: {e}")

            # Wait for a minute before collecting the next batch of data
            time.sleep(60)

def MinuteDataTrial():
    # Define the ticker symbol and interval
    ticker_symbol = 'AAPL'  # Replace with the ticker you want
    interval = '1m'  # 1-minute interval
    period = '1d'  # Full day of data

    # Fetch the data
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)

    # Get the last row of data (most recent minute)
    last_minute_data = data.tail(1)

    # Print the most recent minute of data
    print(last_minute_data)

#Tick_List_Collection() # 5 days worth of minute by minute data
#Collect_Hella_Info()
#Historical_data("TSLA")
#MBM.Minute_by_Minute()
#comparetimes()
#MinuteDataTrial()
    
MinuteDataTrial()