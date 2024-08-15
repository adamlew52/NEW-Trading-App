import yfinance as yf
import pandas_datareader as pdr
import datetime
from alpha_vantage.timeseries import TimeSeries
import time
import os
import pandas as pd



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

#yFinanceTrial('AAPL')
#pandas_datareadertrial()
#TimeSeriesTrial()

def write_df_to_csv(df, file_path, index=False):
    """
    Writes the given DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame to write to CSV.
    file_path (str): The path to the CSV file to create.
    index (bool): Whether to write the DataFrame index to the file. Defaults to False.
    """
    df.to_csv(file_path, index=index)


def Write_Historical_DataFrame_to_CSV(df, file_loc):
    #df.to_csv(file_loc, columns=['Column1', 'Column2'], index=False)
    #df.to_csv(file_loc, sep='\t', index=False)


    df.to_csv(file_loc, header=True, index=False)  # Include header
    #df.to_csv(file_loc, header=False, index=False)  # Exclude header

    df.to_csv(file_loc, index=True)   # Include index
    #df.to_csv(file_loc, index=False)  # Exclude index

    #df.to_csv('output.csv', na_rep='NA', index=False)  # Replace NaN with 'NA'

    # lambda modifications
    # Example: Format date columns
    #df['DateColumn'] = df['DateColumn'].dt.strftime('%Y-%m-%d')

    # Example: Format numerical columns
    #df['Amount'] = df['Amount'].apply(lambda x: f"${x:,.2f}")

    #df.to_csv(file_loc, index=False)
    
    #df.to_csv(file_loc, index=False)


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

    Write_Historical_DataFrame_to_CSV(line_parsed, file_loc)

Tick_List_Collection() # 5 days worth of minute by minute data
#Collect_Hella_Info()
#Historical_data("TSLA")