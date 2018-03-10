import click
from logzero import logger

from twitterkenkoooo.config import Config


@click.command()
@click.option("--config", "-c", required=True)
def main(config: str):
    conf = Config(config)
    api = conf.get_api(sleep_on_rate_limit=False)
    followers = conf.get_followers()
    friends = conf.get_friends()

    l_set = set(followers)
    r_set = set(friends)
    to_follow = l_set - r_set

    looking = []
    for user_id in followers:
        if user_id not in to_follow:
            continue

        looking.append(user_id)
        if len(looking) != 100:
            continue

        lookups = api.LookupFriendship(user_id=looking)
        for lookup in lookups:
            if not lookup.followed_by or lookup.following or lookup.following_requested:
                continue
            logger.info("following {}".format(lookup.screen_name))
            logger.info(lookup)
            api.CreateFriendship(screen_name=lookup.screen_name)
        looking = []


if __name__ == '__main__':
    main()
