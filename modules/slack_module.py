from slack_sdk import WebClient # type: ignore
from slack_sdk.errors import SlackApiError # type: ignore
from env import SLACK_BOT_TOKEN, SLACK_CHANNEL

# Initialize Slack client
slack_client = WebClient(token=SLACK_BOT_TOKEN)

def send_to_slack(article):
    """
    Sends the summary to a Slack channel with interactive buttons.
    """
    try:
        response = slack_client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=f"*Summary for Article: {article['title']}*",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{article['title']}*\n\n{article['content']}\n\nSource: <{article['link']}|{article['link']}>",
                    },
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Copy to Clipboard"},
                            "style": "primary",
                            "action_id": "copy_to_clipboard",
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Dismiss"},
                            "style": "danger",
                            "action_id": "dismiss_summary",
                        },
                    ],
                },
            ],
        )
        print(f"Message sent to Slack: {response['ts']}")
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")


def main(article):
    send_to_slack(article)


if __name__ == "__main__":
    # Example article dictionary
    article = {
        "title": "State of Trust Report | Vanta",
        "link": "https://www.vanta.com/state-of-trust?utm_campaign=state-of-trust-2024&utm_source=tldr&utm_medium=newsletter",
        "content": (
            "Find all your security and compliance content here.\n"
            "Get bite-sized definitions of the terms you need to know.\n"
            "Watch webinars and videos on trending security topics.\n"
            "Deepen your security knowledge and learn new skills.\n"
            "To uncover the latest trends shaping security and compliance, we surveyed 2,500 business and IT leaders across the US, UK, and Australia. "
            "Find out why third-party risk and AI are making it harder to build and demonstrate trust.\n"
            "More than half (55%) of organizations say that security risks have never been higher. At the same time, just 11% of a company's IT budget is dedicated "
            "to security—but leaders say it should be 17% in an ideal world.\n"
        ),
    }

    # Generate and print the summary
    send_to_slack(article)