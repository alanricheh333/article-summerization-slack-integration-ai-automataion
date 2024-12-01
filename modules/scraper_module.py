import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore

def fetch_article_content(link):
    """Fetches the title and main content of an article from the given link."""
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()  # Check for HTTP request errors
        
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title = soup.title.string if soup.title else 'No Title'

        # Extract main article content by targeting <p> tags within the main content
        # Adjust the strategy to pick relevant sections intelligently
        main_content = ''
        for p_tag in soup.find_all('p'):
            text = p_tag.get_text().strip()
            if len(text) > 50:  # Filter short, irrelevant paragraphs
                main_content += text + '\n'

        # Return a dictionary with the article details
        return {
            'title': title,
            'link': link,
            'content': main_content.strip() if main_content else 'No content found'
        }

    except (requests.RequestException, Exception) as e:
        print(f"Failed to fetch content from {link}: {e}")
        return None

def fetch_articles(links):
    """Takes a list of unique links, fetches articles, and returns a list of dictionaries."""
    articles = []
    for link in links:
        print(f"Fetching article from: {link}")
        article_data = fetch_article_content(link)
        if article_data:
            articles.append(article_data)
            print(f"Fetched article: {article_data['title']} from {link}")
        else:
            print(f"Skipped link due to fetching issues: {link}")
    return articles



def main(links):
    articles = fetch_articles(links)
    for article in articles:
        print(f"\nTitle: {article['title']}\nLink: {article['link']}\nContent:\n{article['content'][:300]}...\n")

    return articles


# Example usage
if __name__ == "__main__":
    test_links = [
        'https://www.vanta.com/state-of-trust?utm_campaign=state-of-trust-2024&utm_source=tldr&utm_medium=newsletter',
        'https://www.theverge.com/2024/11/7/24290703/apple-green-bubble-message-reaction-rcs-android?utm_source=tldrnewsletter'
    ]
    main(test_links)
