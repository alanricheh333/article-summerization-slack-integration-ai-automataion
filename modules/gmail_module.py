import os.path
import base64
import re
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from google.auth.transport.requests import Request  # type: ignore
from googleapiclient.discovery import build  # type: ignore

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticates the user and returns the Gmail API service."""
    creds = None
    # The token.json file stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first time.
    # Try loading existing credentials
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception as e:
            print(f"Error loading token.json: {e}")
            raise FileNotFoundError("token.json not found")

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                print("Attempting to reauthenticate...")
                creds = None  # Force reauthentication
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Reauthenticate and create new credentials
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def search_emails(service, query):
    """Searches for emails based on a query and returns the matching email data."""
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("No messages found.")
        return []

    print(f"Found {len(messages)} message(s).")
    emails = []

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        full_body = get_full_email_body(msg)
        links = extract_links_from_body(full_body) if full_body else []
        email_data = {
            'id': message['id'],
            'snippet': msg['snippet'],
            'links': links
        }
        emails.append(email_data)

    return emails

def get_full_email_body(message):
    """Fetches the full body content from the email message payload."""
    payload = message['payload']
    body = None

    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
            elif part['mimeType'] == 'text/html' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
    else:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

    return body

def extract_links_from_body(body):
    """Extracts and returns a filtered list of URLs from the email body."""
    # Regex to find all URLs in the email body
    links = re.findall(r'https?://\S+', body)
    
    # List to hold filtered links
    filtered_links = []

    # Loop to filter out unwanted links
    for link in links:
        # Check if the domain contains "tldr" or matches specific unwanted domains
        if not (re.search(r'https?://[^/]*tldr[^/]*', link) or 'hub.sparklp.co' in link):
            filtered_links.append(link)
    
    return filtered_links


def main():
    # Authenticate and get the service object
    service = authenticate_gmail()

    # Example: Search for emails with a specific keyword
    query = "from:TLDR Web Dev AND label:tlDR AND newer_than:2d"
    emails = search_emails(service, query)

    # Set to store unique links
    unique_links = set()

    for email in emails:
        print(f"Email ID: {email['id']}, Snippet: {email['snippet']}")
        for link in email['links']:
            unique_links.add(link)  # Add each link to the set

    # Convert the set to a list if needed and print the unique links
    unique_links_list = list(unique_links)
    print("\nUnique Links Across All Emails:")
    for link in unique_links_list:
        print(f" - {link}")

    return unique_links_list

if __name__ == "__main__":
    main()
