#!/usr/bin/env python3
#
### Twitter timeline cleaner ###
#
# by Michele <o-zone@zerozone.it> Pinassi
# 
# https://www.zerozone.it/tecnologia-privacy-e-sicurezza/ripulire-la-propria-twitter-timeline/19195
#
from __future__ import print_function

import os
import json
import sys
import argparse

from datetime import datetime
from dateutil import parser

import twitter

def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline

def main():
    argparser = argparse.ArgumentParser(description="Maintain clean your Twitter timeline")
    argparser.add_argument("--until", dest="until_date", required=True, help="Delete tweets until this date (YYYY-MM-DD)")
    argparser.add_argument("--dry-run", dest="dry_run", action="store_true", default=False)

    args = argparser.parse_args()

    if not ("TWITTER_CONSUMER_KEY" in os.environ and
            "TWITTER_CONSUMER_SECRET" in os.environ and
            "TWITTER_ACCESS_TOKEN" in os.environ and
            "TWITTER_ACCESS_TOKEN_SECRET" in os.environ and
            "TWITTER_NAME" in os.environ):
        sys.stderr.write("Twitter API credentials not set.\n")
        exit(1)

    api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],access_token_key=os.environ["TWITTER_ACCESS_TOKEN"],access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],sleep_on_rate_limit=True)

    until_date = datetime.min if args.until_date is None else parser.parse(args.until_date, ignoretz=True)

    timeline = get_tweets(api=api, screen_name=os.environ["TWITTER_NAME"])

    for tweet in timeline:

        print(tweet._json)

        tweet_date = parser.parse(tweet._json["created_at"], ignoretz=True)
        tweet_id = tweet._json['id']

        if tweet_date >= until_date:
           continue

        try:
            print("delete tweet %s" % tweet_id)
            if not args.dry_run:
                api.DestroyStatus(tweet_id)
        except twitter.TwitterError as err:
            print("Exception: %s\n" % err.message)


if __name__ == "__main__":
    main()
