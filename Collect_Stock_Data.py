import yfinance as yf
import pandas_datareader as pdr
import datetime
from alpha_vantage.timeseries import TimeSeries
import time


def yFinanceTrial(): #user-friendly and does not require an API key.
    # Define the ticker symbol
    ticker_symbol = 'AAPL'

    # Get the data
    ticker_data = yf.Ticker(ticker_symbol)

    # Get historical market data
    ticker_df = ticker_data.history(period='1mo', start='2023-07-01', end='2024-08-01')

    # Display the data
    #print(ticker_df)

    # Get the data
    ticker = yf.Ticker(ticker_symbol)

    # Get basic information
    info = ticker.info

    # Access specific data
    current_price = info['currentPrice']
    market_cap = info['marketCap']
    sector = info['sector']

    #print(f"Current Price: {current_price}")
    #print(f"Market Cap: {market_cap}")
    #print(f"Sector: {sector}")
    return sector,current_price,market_cap,

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
        yFinanceTrial('AAPL')
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

#def WriteToCSV(line_parsed, file_loc):
#    with open(file_loc, 'a') as csv_store:
#        current_time_utc = time.gmtime()
#        formatted_time_utc = time.strftime("%Y-%m-%d %H:%M:%S", current_time_utc)
#        line_parsed = line_parsed + formatted_time_utc
#
#        csv_store.write(line_parsed)



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
                print(f"\n---------------Data for {line_parsed}---------------\n\n{yFinanceTrial()}")
                #WriteToCSV(line_parsed, "/Users/adam/Documents/GitHub/NEW-Trading-App/Practice_Stock_Data_Storage")
            except Exception as e:
                # Print a custom message along with the exception
                print(f"An error occurred: {e}")


#def WriteToCSV():
#    print("writing data to csv..."
#Showoff(100)
            
Tick_List_Collection()