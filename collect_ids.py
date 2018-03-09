import twitter
import click
import threading
import json
from logzero import logger

from twitterkenkoooo.config import Config


@click.command()
@click.option("--config", "-c", required=True)
def main(config: str):
    conf = Config(config)
    api = twitter.Api(consumer_key=conf.consumer_key,
                      consumer_secret=conf.consumer_secret,
                      access_token_key=conf.access_token_key,
                      access_token_secret=conf.access_token_secret,
                      sleep_on_rate_limit=True)

    def f1():
        logger.info("dumping followers")
        with open(conf.followers_json, "w") as f:
            json.dump(api.GetFollowerIDs(), f)
        logger.info("followers dumping done")

    def f2():
        logger.info("dumping friends")
        with open(conf.friends_json, "w") as f:
            json.dump(api.GetFriendIDs(), f)
        logger.info("friends dumping done")

    t1 = threading.Thread(target=f1)
    t2 = threading.Thread(target=f2)
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()
