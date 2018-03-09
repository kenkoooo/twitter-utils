import json

import click
import twitter

from twitterkenkoooo.config import Config
from logzero import logger


@click.command()
@click.option("--config", "-c", required=True)
def main(config: str):
    conf = Config(config)
    api = twitter.Api(consumer_key=conf.consumer_key,
                      consumer_secret=conf.consumer_secret,
                      access_token_key=conf.access_token_key,
                      access_token_secret=conf.access_token_secret,
                      sleep_on_rate_limit=True)

    with open(conf.followers_json, "r") as f:
        followers = json.load(f)
    with open(conf.friends_json, "r") as f:
        friends = json.load(f)

    l_set = set(followers)
    r_set = set(friends)
    removable = r_set - l_set

    friends.reverse()
    looking = []
    for user_id in friends:
        if user_id not in removable:
            continue
        looking.append(user_id)
        if len(looking) != 100:
            continue
        lookups = api.LookupFriendship(user_id=looking)
        for lookup in lookups:
            if lookup.followed_by or not lookup.following:
                continue
            print(lookup)
            return
        looking = []


if __name__ == '__main__':
    main()
