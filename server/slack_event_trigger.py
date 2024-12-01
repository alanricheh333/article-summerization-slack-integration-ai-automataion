#user_id = "U06BXH7HGNR"

from flask import Flask, request, jsonify # type: ignore
from slack_sdk import WebClient # type: ignore
from slack_sdk.errors import SlackApiError # type: ignore
import json
import pyperclip # type: ignore
from env import SLACK_BOT_TOKEN

app = Flask(__name__)

# Slack client initialization
slack_client = WebClient(token=SLACK_BOT_TOKEN)


@app.route("/slack/events", methods=["POST"])
def slack_events():
	"""
	Handles Slack interactive message events.
	"""
	print("errooooo")
	payload = json.loads(request.form["payload"])

	# Extract interaction details
	action_id = payload["actions"][0]["action_id"]
	user_id = payload["user"]["id"]
	channel_id = payload["channel"]["id"]
	message_ts = payload["message"]["ts"]

	if action_id == "copy_to_clipboard":
		# Notify the user (simulate copying to clipboard)
		# Extract the title, summary, and source from the payload
		blocks = payload["message"]["blocks"]
	
		# Extract title from the first block
		title = blocks[0]["text"]["text"].split("\n\n")[0].strip("*")
	
		# Extract the summary from the first block
		summary_text = blocks[0]["text"]["text"].split("\n\n")[1]
	
		# Extract the source/link
		try:
			# Find the section containing the source link
			raw_source_text = blocks[0]["text"]["text"].split("\n\n")[-1]
	
			# Locate the link in the source text
			link_start = raw_source_text.find("<")
			link_end = raw_source_text.find("|")
	
			if link_start != -1 and link_end != -1:
				source_link = raw_source_text[link_start + 1: link_end]
			else:
				source_link = "No source link found"
	
		except Exception as e:
			source_link = "Error extracting source link"
			print(f"Error: {e}")
		try:
			# Format the text for LinkedIn
			post_text = f"{title}\n\n{summary_text}\n\nSource: {source_link}"
			
			pyperclip.copy(post_text)
			print(payload)
			print("Text copied to clipboard.")
			slack_client.chat_postEphemeral(
				channel=channel_id,
				user=user_id,
				text="The summary was copied to your clipboard! (Simulated).",
			)
		except SlackApiError as e:
			print(f"Error sending ephemeral message: {e.response['error']}")
		return jsonify({"text": "Copy to Clipboard action processed."})

	elif action_id == "dismiss_summary":
		# Update the message to indicate it was dismissed
		try:
			slack_client.chat_update(
				channel=channel_id,
				ts=message_ts,
				text="This summary has been dismissed by the user.",
				blocks=[],  # Clear blocks to simplify the message
			)
		except SlackApiError as e:
			print(f"Error updating message: {e.response['error']}")
		return jsonify({"text": "Dismiss action processed."})

	return jsonify({"status": "ok"})


if __name__ == "__main__":
	app.run(port=5000)
