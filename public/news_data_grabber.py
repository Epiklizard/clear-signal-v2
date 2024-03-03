import requests
import json
from datetime import datetime

# Insert your News API key here
api_key = 'qdmgg6OCMin2NfJS8MfzpdKH3aDmbD5hBDXHZKwc'

# Function to fetch news articles
def fetch_articles(api_key, date):
    url = 'https://api.thenewsapi.com/v1/news/all'

    # Define the parameters for the request
    params = {
        'api_token': api_key,
        'published_on': date,
        'language': 'en',
        'categories': 'tech'
    }

    response = requests.get(url, params=params)
    articles = response.json()
    return articles

# Function to fetch news articles across multiple pages
def fetch_all_articles(api_key, date, categories, total_pages):
    base_url = 'https://api.thenewsapi.com/v1/news/all'
    all_articles = []

    for page in range(1, total_pages + 1):  # Loop through pages
        params = {
            'api_token': api_key,
            'published_on': date,
            'language': 'en',  # Choose the language of the articles
            'categories': categories,
            'page': page,  # Current page number
            # 'search': 'Apple'
        }

        response = requests.get(base_url, params=params)

        # Check the response status
        if response.status_code == 200:
            # If successful, add articles to our list
            data = response.json()
            if 'data' in data:
                all_articles.extend(data['data'])  # Add the articles from the current page
        else:
            print(f"Error fetching page {page}: {response.status_code}")
            break  # Exit the loop if there is an error

    print('done with ', date)
    return all_articles

# Save the articles to a file
def save_articles(articles, filename):
    with open(filename, 'w') as f:
        json.dump(articles, f, indent=4)


# chosen_day = datetime(2024, 1, 1).strftime('%Y-%m-%d')
# # articles = fetch_all_articles(api_key, chosen_day, 4)
# articles = fetch_articles(api_key, chosen_day)


# save_articles(articles, f'data/article0.json')


lis = ['business', 'entertainment', 'politics', 'science', 'tech']

for categories in lis:
    for i in range(1, 30):
        # # Chosen day for article search (e.g., March 10, 2023)
        chosen_day = datetime(2024, 2, i).strftime('%Y-%m-%d')

        # Fetch the news articles
        articles = fetch_all_articles(api_key, chosen_day, categories, 4)

        # Save articles to a file
        save_articles(articles, f'data/{categories}/2024-02/day_{i}.json')