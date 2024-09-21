import os
import webbrowser
from newspaper import Article
from collections import Counter
import re
from googlesearch import search
import requests
import time
from datetime import datetime

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
            webbrowser.open(url)  # Open the link in the default web browser
            time.sleep(3600)  # Wait for 1 hour before retrying (as noted in google's api documentation)
            return fetch_article_content(url)  # Retry fetching the article
        else:
            print(f"Error fetching article from {url}: {e}")
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

    return normalized_data

def find_articles(keyword, date, num_results=10):
    """Searches for articles containing the specified keyword and published on a specific date."""
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")
    keywordAdditions = [f"{keyword} financial articles published on {formatted_date}",
                        f"{keyword} recent changes published on {formatted_date}",
                        f"{keyword} predictions published on {formatted_date}"]
    search_results = []
    
    time.sleep(0.25) # just to keep google off da back

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
    
    for ticker in list_of_tickers:
        create_directory(ticker)
        print(f"Processing articles for ticker: {ticker}")
        urls = find_articles(ticker, date)
        normalized_data = process_articles(urls, positive_word_list, negative_word_list)
        all_normalized_data[ticker] = normalized_data

        with open(f'/Users/adam/Documents/GitHub/NEW-Trading-App/article_word_frequency_data/{ticker}/normalized_article_data_{date}.txt', 'w') as f:
            f.write(f"{ticker}: {normalized_data}\n")

# Example usage
list_of_tickers = get_tickers_from_file('/Users/adam/Documents/GitHub/NEW-Trading-App/list_of_tickers.txt')
specific_date = "2024-01-01"
article_processor_function(list_of_tickers, specific_date)
