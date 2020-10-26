from TwitterAPI import TwitterAPI
from dotenv import load_dotenv
from urllib.parse import parse_qs
import os
import feedparser
import time
from datetime import datetime
import dateutil.parser
import json
import random

load_dotenv()


consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

api = TwitterAPI(consumer_key, consumer_secret,
                 access_token, access_token_secret)


def load_json():
    # carregando a lista de feeds do json
    global list_feeds

    with open('feeds.json') as json_file:
        list_feeds = json.load(json_file)


def update_lastsync_on_json(item, lastsync):
    # abrindo arquivo json e salvando as alterações na data de ultima sincronia

    global list_feeds
    list_feeds['feeds'][item]['lastsync'] = lastsync
    with open("feeds.json", "w+") as json_file:
        json_file.write(json.dumps(list_feeds))
        json_file.close()

    load_json()


def create_hashtags(hashtags):
    str_hashtags = ''

    if (len(hashtags) > 0):
        for hs in hashtags:
            str_hashtags += f' #{hs}'

        str_hashtags += ' '

    return str_hashtags


def create_new_tweet(entry, hashtags):
    try:
        tweet_title = entry.get('title', '')
        tweet_link = entry.get('link', '')

        new_tweet = f'{tweet_title}{create_hashtags(hashtags)}{tweet_link}'

        # debug purpose:
        tweet_published = entry.get('published', '')
        print('****')
        print(f'[{tweet_published}] {new_tweet}')
        print('****')
        #api.request('statuses/update', {'status': f'{new_tweet}'})

        return True
    except:
        return False


def get_feed_lastsync(feed):
    try:
        return dateutil.parser.parse(feed['lastsync']).replace(tzinfo=None)
    except:
        return ''


def main():
    global list_feeds
    print('running twitterbot')
    while (True):
        try:
            load_json()
            for item in range(len(list_feeds['feeds'])):
                feed = list_feeds['feeds'][item]
                hashtags = feed['hashtags']
                lastsync = get_feed_lastsync(feed)
                rss = feedparser.parse(feed['url'])
                entries = rss['entries'][:20]

                for entry in reversed(entries):
                    entry_published = entry.get('published', '')
                    published = dateutil.parser.parse(entry_published
                                                      ).replace(tzinfo=None)

                    if (type(lastsync) is not datetime):
                        update_lastsync_on_json(item, entry_published)
                        lastsync = get_feed_lastsync(feed)
                    elif (type(lastsync) is datetime and (published > lastsync)):
                        create_new_tweet(entry, hashtags)
                        update_lastsync_on_json(item, entry_published)

                    seconds = random.randrange(15, 120)
                    print(f'Próxima noticia em {seconds}s')
                    time.sleep(seconds)
        except:
                return


if (__name__ == "__main__"):
    main()
