#!/usr/bin/env python3
#
# Twitter timeline cleaner
# v0.0.2
#
# by Michele <o-zone@zerozone.it> Pinassi
# 
# Released under GPL v3
#
# More @ https://www.zerozone.it/tecnologia-privacy-e-sicurezza/ripulire-la-propria-twitter-timeline/19195
#
# v0.0.2 - 25.07.2021
# - added "save" and "limit" options
#

from __future__ import print_function

import os
import json
import sys
import argparse

from datetime import datetime, date
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
    argparser.add_argument("--until", dest="until_date", required=True, help="delete tweets until this date (YYYY-MM-DD)")
    argparser.add_argument("--dry-run", dest="dry_run", action="store_true", default=False help="simulate (don't delete anything)")
    argparser.add_argument("--save", dest="save", action="store_true", default=False, help="Save deleted tweets in JSON")
    argparser.add_argument("--limit", dest="limit", default=False, help="define how many tweets to delete (default: all)")

    args = argparser.parse_args()

    if not ("TWITTER_CONSUMER_KEY" in os.environ and
            "TWITTER_CONSUMER_SECRET" in os.environ and
            "TWITTER_ACCESS_TOKEN" in os.environ and
            "TWITTER_ACCESS_TOKEN_SECRET" in os.environ and
            "TWITTER_NAME" in os.environ):
        sys.stderr.write("Twitter API credentials not set.\n")
        exit(1)

    print("[#] Connection to Twitter API...")

    api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],access_token_key=os.environ["TWITTER_ACCESS_TOKEN"],access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],sleep_on_rate_limit=True)

    try:
        api.VerifyCredentials()
    except twitter.TwitterError as err:
        print("[!] API error: %s. Please verify credentials and try again!"%err.message)
        exit(1)

    until_date = datetime.min if args.until_date is None else parser.parse(args.until_date, ignoretz=True)

    if args.save:
        now = datetime.now()
        filename='tweets_%s.json'%(now.strftime('%Y%b%d'))
        json_file = open(filename, 'w')
        print("[#] Saving deleted tweets to %s"%filename)

    print("[#] Fetch tweets for %s..."%os.environ["TWITTER_NAME"])

    try:
        timeline = get_tweets(api=api, screen_name=os.environ["TWITTER_NAME"])
    except twitter.TwitterError as err:
        print("Exception: %s\n" % err.message)
        exit(1)

    tweet_count=0

    for tweet in timeline:
        tweet_date = parser.parse(tweet._json["created_at"], ignoretz=True)
        tweet_id = tweet._json['id']

        if tweet_date >= until_date:
           continue

        tweet_count+=1
        if args.limit and tweet_count > args.limit:
            break

        print(tweet._json)

        if args.save:
            print("[#] Save tweet ID %d to file..."%tweet_id)
            json.dump(tweet._json,json_file)

        try:
            print("[!] Delete tweet %s" % tweet_id)
            if not args.dry_run:
                api.DestroyStatus(tweet_id)
        except twitter.TwitterError as err:
            print("Exception: %s\n" % err.message)

    print("[#] DONE! Deleted %d tweet(s) from yout timeline"%tweet_count)

    if args.save:
        json_file.close()

if __name__ == "__main__":
    main()
