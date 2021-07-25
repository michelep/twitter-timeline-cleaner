# Twitter timeline cleaner

*Keep clean your Twitter timeline*

**Why keep your Twitter timeline clean?** First of all, to reduce the amount of public personal information we leave in the Net infosphere. Then, to prevent a tweet from a few years ago that we've completely forgotten about from compromising our career or relationship. Of course, it's impossible to guarantee that someone hasn't saved our tweets, but removing them after some time helps minimize the risk that our thoughts and reactions could end up in the wrong hands or harm us.

If I convinced you, this free script can help you in the purpose.

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

