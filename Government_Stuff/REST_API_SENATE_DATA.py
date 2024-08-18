import requests
import json

# Your API key here
API_KEY = 'f8256c817082d96f12135eb8a2d994bedba3cf8a'

# Base URL for the LDA REST API
BASE_URL = 'https://lda.congress.gov/api/v1/'  # Confirm this URL with the API documentation

# Define headers including your API key
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Define the endpoint you want to query
endpoint = 'disclosures'  # Adjust this to the correct endpoint based on API documentation

# Define any query parameters (e.g., year, senator name, etc.)
params = {
    'year': '2023',  # Example query parameter for a specific year
    'limit': 100,    # Limit the number of results per request
    # Add more query parameters as needed
}


# Make a GET request to the API endpoint
try:
    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
    
    # Print response status code and headers for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    
    # Check if the request was successful
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
    
    # Parse the JSON response
    data = response.json()
    
    # Print the retrieved data

    print("----------------------------------")
    print(json.dumps(data, indent=4))
    
    # Save data to a file (optional)
    with open('financial_disclosures.json', 'w') as f:
        json.dump(data, f, indent=4)

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")
