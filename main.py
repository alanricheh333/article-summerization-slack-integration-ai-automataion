from modules.gmail_module import main as google_email_main
from modules.scraper_module import main as scraper_main
from modules.LLM_module import main as llm_main
from modules.slack_module import main as slack_main
import time

if __name__ == "__main__":

    links = google_email_main()
    articles = scraper_main(links)

    for article in articles:
        llm_main(article)
        time.sleep(3)
        slack_main(article)
