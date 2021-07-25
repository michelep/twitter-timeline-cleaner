# Twitter timeline cleaner
## Clean your Twitter timeline

## Prerequisites
Before running, remember to set these environment variables: 

```
export TWITTER_ACCESS_TOKEN='' 
export TWITTER_ACCESS_TOKEN_SECRET='' 
export TWITTER_CONSUMER_KEY='' 
export TWITTER_CONSUMER_SECRET='' 
export TWITTER_NAME='@your_twitter_name' 
```

and follow the instructions to claim a [Twitter developers account](https://developer.twitter.com/en/apply) and [to create an app](https://developer.twitter.com/en/apps/create), needed to fetch your Twitter timeline's tokens and keys.

## Usage

```
usage: twitter-timeline-cleaner.py [-h] --until UNTIL_DATE [--dry-run] [--save] [--limit LIMIT]

Maintain clean your Twitter timeline

optional arguments:
  -h, --help          show this help message and exit
  --until UNTIL_DATE  delete tweets until this date (YYYY-MM-DD)
  --dry-run           simulate (don't delete anything)
  --save              save deleted tweets in JSON
  --limit LIMIT       define how many tweets to delete (default: all)
```

Article in italian talking about this project: [Ripulire la propria Twitter timeline](https://www.zerozone.it/tecnologia-privacy-e-sicurezza/ripulire-la-propria-twitter-timeline/19195)

Work inspired by [delete-tweets](https://github.com/koenrh/delete-tweets) by Koen Rouwhorst
