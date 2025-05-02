import json
import time
import feedparser
from datetime import datetime
import re

# Svenska stopwords
stop_words = set([
    "och", "i", "på", "av", "en", "ett", "som", "för", "med", "till", "från",
    "om", "det", "att", "är", "var", "sig", "de", "vi", "du", "man", "han", "hon",
    "men", "har", "inte", "kan", "ska", "nu", "också", "så", "då", "omkring", "dömd", "döms", "efter", "under"
])

def normalize_date(date_string):
    try:
        return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
    except ValueError:
        try:
            clean_date_string = date_string.split("+")[0].strip()
            return datetime.strptime(clean_date_string, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.min

def extract_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return set([word for word in words if word not in stop_words])

def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def fetch_new_articles(last_article_date):
    url = "https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/"
    feed = feedparser.parse(url)

    new_articles = []
    for entry in feed.entries:
        article_date = normalize_date(entry.published)
        if article_date > last_article_date:
            new_articles.append({
                "title": entry.title,
                "link": entry.link,
                "pubDate": entry.published,
                "description": entry.get("summary", entry.get("description", ""))
            })
    return new_articles

def match_articles_with_events(articles_data, events_data):
    matched_results = load_json('matched_results.json')
    existing_matches = {(m['article_title'], m['event_id']) for m in matched_results}
    new_matches_count = 0

    for article in articles_data:
        article_date = normalize_date(article['pubDate'])
        article_words = extract_words(article['title']) | extract_words(article['description'])

        # Hitta event som har samma datum som artikeln
        events_same_date = [
            event for event in events_data
            if normalize_date(event['datetime']).date() == article_date.date()
        ]

        for event in events_same_date:
            event_words = (
                extract_words(event['name']) |
                extract_words(event['summary']) |
                extract_words(event['type'])
            )

            common_words = article_words & event_words

            if len(common_words) >= 3:
                match_key = (article['title'], event['id'])
                if match_key not in existing_matches:
                    matched_results.append({
                        "event_id": event["id"],
                        "event_datetime": event["datetime"],
                        "event_name": event["name"],
                        "event_summary": event["summary"],
                        "event_type": event["type"],
                        "article_title": article["title"],
                        "article_description": article["description"],
                        "article_link": article["link"],
                        "common_words": list(common_words)
                    })
                    existing_matches.add(match_key)
                    new_matches_count += 1

    save_json('matched_results.json', matched_results)
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {new_matches_count} nya matchningar hittade. {len(matched_results)} totalt sparade.")

def main_loop():
    while True:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        articles_data = load_json('articles.json')
        events_data = load_json('events_data.json')

        if articles_data:
            last_article_date = max([normalize_date(a['pubDate']) for a in articles_data])
        else:
            last_article_date = datetime.min

        new_articles = fetch_new_articles(last_article_date)

        if new_articles:
            articles_data = new_articles + articles_data
            save_json('articles.json', articles_data)
            print(f"{current_time} - {len(new_articles)} nya artiklar tillagda.")
        else:
            print(f"{current_time} - Inga nya artiklar.")

        match_articles_with_events(articles_data, events_data)

        # Skriv ut antalet artiklar och datapunkter efter varje scan
        num_articles = len(articles_data)
        num_matched_results = len(load_json('matched_results.json'))

        print(f"{current_time} - Artiklar i articles.json: {num_articles}")
        print(f"{current_time} - Datapunkter i matched_results.json: {num_matched_results}")

        print(f"{current_time} - Väntar 30 sekunder...\n")
        time.sleep(30)

if __name__ == "__main__":
    main_loop()
