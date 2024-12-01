# **Automated Article Summarization and Slack Integration**

## **Overview**
This project automates the process of:
1. **Reading emails** from Gmail to extract article links.
2. **Scraping article content** from the extracted links.
3. **Generating summaries** using an LLM model (via Groq).
4. **Sending the summaries** to a Slack channel with interactive buttons for further actions:
   - **Copy to Clipboard**: Copies the summary for immediate use (e.g., posting to LinkedIn).
   - **Dismiss**: Marks the summary as dismissed.

---

## **Project Structure**

```plaintext
├── LICENSE
├── README.md
├── credentials.json (not included; see setup instructions)
├── env.py (not included; contains sensitive environment variables)
├── main.py (entry point for the project)
├── modules
│   ├── LLM_module.py (handles summarization using Groq)
│   ├── __init__.py
│   ├── gmail_module.py (fetches emails and extracts links)
│   ├── scraper_module.py (scrapes articles from links)
│   └── slack_module.py (sends messages to Slack)
├── requirements.txt (Python dependencies)
├── server
│   └── slack_event_trigger.py (handles Slack interactive actions)
└── token.json (not included; generated during Gmail API authentication)

---

## Requirements

- **Python 3.10 or later**
- **Google API credentials** for Gmail API
- **Groq API key**
- **Slack bot token and channel**
- **Internet access** for fetching articles and API communication

---

## Setup Instructions

### Clone the Repository

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

### Install Dependencies

1. Create a virtual environment and install the required dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Create the `env.py` File

1. Create an `env.py` file to store sensitive environment variables:
   ```python
   GROQ = "your_groq_api_key"
   SLACK_BOT_TOKEN = "your_slack_bot_token"
   SLACK_CHANNEL = "your_slack_channel"
   ```

2. Add the `env.py` file to `.gitignore` to avoid committing it to version control.

### Set Up Google API for Gmail

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the Gmail API:
   - Navigate to **API & Services** > **Enable APIs and Services**.
   - Search for and enable the **Gmail API**.
4. Create OAuth 2.0 credentials:
   - Go to **Credentials** > **Create Credentials** > **OAuth Client ID**.
   - Select **Desktop App** as the application type.
   - Download the `credentials.json` file and place it in the project root.
5. Run the project once to generate `token.json` for Gmail authentication:
   ```bash
   python main.py
   ```

---

## Setting Up Groq

1. Sign up at [Groq](https://www.groq.com/).
2. Navigate to the API section in your dashboard.
3. Obtain your API key.
4. Store the key in the `env.py` file under the `GROQ` variable.

---

## Setting Up Slack Bot

1. Go to the [Slack API page](https://api.slack.com/) and create a new app.
2. Choose "From scratch" and name your app.
3. Add necessary scopes:
   - Navigate to **OAuth & Permissions**.
   - Add the following Bot Token Scopes:
     - `chat:write`
     - `commands`
4. Install the app to your workspace and authorize it.
5. Copy the Bot User OAuth Token and store it in the `env.py` file under `SLACK_BOT_TOKEN`.
6. Enable interactivity:
   - Navigate to **Interactivity & Shortcuts**.
   - Enable interactivity and set the **Request URL** to your ngrok public URL, e.g., `https://<your-ngrok-url>/slack/events`.

---

## Configuring Flask Server for Slack Actions

1. Start the Flask server to handle Slack interactions:
   ```bash
   python server/slack_event_trigger.py
   ```
2. Use ngrok to expose your local server:
   ```bash
   ngrok http 5000
   ```
3. Copy the ngrok public URL and set it as the **Request URL** in Slack (under **Interactivity & Shortcuts**).

---

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```
2. The workflow involves:
   - Fetching emails using Gmail API.
   - Scraping article content from extracted links.
   - Generating summaries using Groq.
   - Sending summaries to Slack with interactive buttons.

---

## Slack Actions

### Copy to Clipboard

- Formats the summary as a LinkedIn-style post, including the title, summary, and source link.
- Copies the text to the clipboard for easy posting.

### Dismiss

- Updates the Slack message to indicate the summary has been dismissed.

---

## Key Modules

### gmail_module.py

- Authenticates Gmail API and fetches emails based on a query.
- Extracts unique article links from email bodies.

### scraper_module.py

- Fetches article content and title using BeautifulSoup.
- Filters irrelevant or short paragraphs.

### LLM_module.py

- Uses Groq LLM to generate summaries.
- Accepts article title, content, and link as input.

### slack_module.py

- Sends summaries to Slack channels.
- Includes interactive buttons for actions.

### slack_event_trigger.py

- Handles interactive actions in Slack:
  - Copy to Clipboard: Formats and copies the summary.
  - Dismiss: Updates the Slack message to indicate dismissal.

---

## Known Issues and Debugging

### Error: `invalid_blocks`

- Ensure the `blocks` payload is correctly formatted.
- Validate the payload in Slack's [Block Kit Builder](https://app.slack.com/block-kit-builder/).

### Error: `Token has been expired or revoked`

- Delete `token.json` and re-authenticate with Gmail API:
   ```bash
   python main.py
   ```

---

## Contributing

Feel free to contribute by submitting issues or pull requests. All contributions are welcome.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
