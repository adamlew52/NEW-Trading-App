import os
import webbrowser
from newspaper import Article
from collections import Counter
import re
from googlesearch import search
import requests
import time
from datetime import datetime, timedelta
from newspaper.article import ArticleException

num_results_DESIGNATOR = 1


def load_wordlist(file_path):
    """Loads a word list from a given text file."""
    with open(file_path, 'r') as file:
        return {word.strip().lower() for word in file if word.strip()}

def fetch_article_content(url):
    """Fetches the content of an article from a given URL."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:  # Too Many Requests
            print(f"CAPTCHA or too many requests error for {url}. Opening in browser.")
            print(webbrowser.get())
            webbrowser.open(url)  # Open the link in the default web browser
            time.sleep(3600)  # Wait for 1 hour before retrying
            return fetch_article_content(url)  # Retry fetching the article
        elif e.response.status_code == 403:  # Forbidden
            print(f"Access denied for {url}. Skipping this URL.")
            return None
        elif e.response.status_code == 401:  # Unauthorized
            print(f"Authorization required for {url}. Skipping this URL.")
            return None
        else:
            print(f"Error fetching article from {url}: {e}")
            return None
    except ArticleException as e:
        print(f"Failed to download the article from {url}: {e}")
        return None

def count_word_frequencies(article_text, word_list):
    """Counts word frequencies in the article text."""
    words = re.findall(r'\b\w+\b', article_text.lower())
    return Counter(word for word in words if word in word_list)

def save_to_txt(data, output_file):
    """Writes the normalized data to a text file."""
    with open(output_file, 'a') as f:
        for entry in data:
            f.write(f"{entry}\n")

def normalize_data(pos_count, neg_count):
    total_count = pos_count + neg_count
    if total_count == 0:
        return 0  # No articles processed
    return round((pos_count - neg_count) / total_count * 2 - 1, 4)  # Normalize to [-1, 1]

def process_articles(urls, positive_word_list, negative_word_list):
    """Processes articles and normalizes positive and negative counts."""
    normalized_data = []
    for url in urls:
        article_content = fetch_article_content(url)
        if article_content:
            word_frequencies_pos = count_word_frequencies(article_content, positive_word_list)
            word_frequencies_neg = count_word_frequencies(article_content, negative_word_list)

            pos_count = sum(word_frequencies_pos.values())
            neg_count = sum(word_frequencies_neg.values())
            normalized_value = normalize_data(pos_count, neg_count)

            normalized_data.append(normalized_value)

            with open(f"/Users/adam/Documents/GitHub/NEW-Trading-App/article_word_frequencies.txt", 'a') as a:
                a.write(f"{url}: \n\tpos:{pos_count}\n\tneg:{neg_count}\n")
                a.write("----------------------------------------------------------------------\n")

        time.sleep(1)  # Sleep 1 second between article fetches to avoid rate limiting

    return normalized_data

def find_articles(keyword, date, num_results_DESIGNATOR): #CHANGEME--------------------------------------------------------------------
    """Searches for articles containing the specified keyword and published on a specific date."""
    num_results = num_results_DESIGNATOR
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")
    keywordAdditions = [
        f"{keyword} financial articles published on {formatted_date}",
        f"{keyword} recent changes published on {formatted_date}",
        f"{keyword} predictions published on {formatted_date}"
    ]
    
    search_results = []
    
    time.sleep(0.5)  # Just to keep Google off da back

    for search_query in keywordAdditions:
        print(f"Searching for articles containing: '{search_query}'")
        search_results.extend(search(search_query, num_results))
        time.sleep(1)  # Wait 1 second between searches to avoid rate limiting
    
    return search_results[:num_results]  # Limit to num_results

def get_tickers_from_file(file_path):
    """Loads tickers from a specified text file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def create_directory(ticker_name):
    """Creates a directory with the given name."""
    dir_name = f"/Users/adam/Documents/GitHub/NEW-Trading-App/article_word_frequency_data/{ticker_name}"
    try:
        os.makedirs(dir_name, exist_ok=True)  # Creates the directory if it doesn't exist
        print(f"Directory '{dir_name}' created successfully.")
    except Exception as e:
        print(f"Error creating directory '{dir_name}': {e}")

def article_processor_function(list_of_tickers, date):
    """Processes articles for each ticker and saves the normalized data."""
    negative_word_list = load_wordlist('/Users/adam/Documents/GitHub/NEW-Trading-App/Keywords/Negative.txt')
    positive_word_list = load_wordlist('/Users/adam/Documents/GitHub/NEW-Trading-App/Keywords/Positive.txt')
    
    all_normalized_data = {}
    daily_scores = []  # To store the overall scores for the day

    for ticker in list_of_tickers:
        create_directory(ticker)
        print(f"Processing articles for ticker: {ticker}")
        urls = find_articles(ticker, date, num_results_DESIGNATOR)
        normalized_data = process_articles(urls, positive_word_list, negative_word_list)
        
        # Calculate the average normalized score for the day
        average_score = sum(normalized_data) / len(normalized_data) if normalized_data else 0
        daily_scores.append(average_score)  # Add to daily scores

        # Prepend the average score to the normalized data
        normalized_data_with_average = [average_score] + normalized_data
        
        all_normalized_data[ticker] = normalized_data_with_average  # Store with average as first entry

        # Write the ticker's data to file
        with open(f'/Users/adam/Documents/GitHub/NEW-Trading-App/article_word_frequency_data/{ticker}/normalized_article_data_{date}.txt', 'a') as f:
            f.write(f"{ticker}\t|{date}\t: {normalized_data_with_average}\n")
    
    # Print the overall average score for the day across all tickers
    overall_average_score = sum(daily_scores) / len(daily_scores) if daily_scores else 0
    print(f"Overall average score for {date}: {overall_average_score}")


def iterate_date(current_date):
    # Split the date into day, month, year
    result = re.split(r'[_-]', current_date)
    day = int(result[2])
    month = int(result[1])
    year = int(result[0])
    
    # Number of days in each month (index 1 = January, index 12 = December)
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Check if it's a leap year
    def is_leap_year(year):
        return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

    # Adjust for leap years
    if is_leap_year(year):
        days_in_month[1] = 29  # February has 29 days in leap years
    
    # Increment the day
    if day < days_in_month[month - 1]:
        day += 1
    else:
        day = 1
        # Increment the month
        if month < 12:
            month += 1
        else:
            month = 1
            year += 1
    
    # Format the new date as YYYY-MM-DD
    new_date = f"{year:04d}-{month:02d}-{day:02d}"
    
    return new_date

# Function to iterate from start_date to today
def iterate_until_today(start_date):
    current_date = start_date
    today = datetime.today().strftime('%Y-%m-%d')  # Today's date in YYYY-MM-DD format
    
    # Store each date
    dates = []
    
    # Loop until current_date reaches today
    while current_date != today:
        dates.append(current_date)  # Save the current date
        current_date = iterate_date(current_date)  # Increment the date
        with open("/Users/adam/Documents/GitHub/NEW-Trading-App/tracking_date_iteration.txt", 'a') as date_track:
            date_track.write(f"{current_date}\n")
    
    dates.append(today)  # Add today's date
    return dates








# ----------------------------------------------------------------------------------------------------------------------------------------------

# Example usage:
# Load tickers from the file
list_of_tickers = get_tickers_from_file('/Users/adam/Documents/GitHub/NEW-Trading-App/list_of_tickers.txt')

# Set the start date for the iteration
start_date = "2001-01-01"

# Get all dates from start_date until today
all_dates = iterate_until_today(start_date)

# Iterate over each date and process the articles
for date in all_dates:
    article_processor_function(list_of_tickers, date)  # Process articles for each date
    print(f"Processing stuff for: {date}")
    
    # Add a delay to prevent too many requests (adjust as needed)
    time.sleep(2)  # 2-second delay between requests