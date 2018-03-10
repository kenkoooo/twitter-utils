import click
from logzero import logger

from twitterkenkoooo.config import Config


@click.command()
@click.option("--config", "-c", required=True)
def main(config: str):
    conf = Config(config)
    api = conf.get_api()
    followers = conf.get_followers()
    friends = conf.get_friends()

    l_set = set(followers)
    r_set = set(friends)
    removable = r_set - l_set

    looking = []
    removed = False
    for user_id in friends:
        if removed:
            break

        if user_id not in removable:
            continue

        looking.append(user_id)
        if len(looking) != 100:
            continue

        lookups = api.LookupFriendship(user_id=looking)
        for lookup in lookups:
            if lookup.followed_by or not lookup.following:
                continue
            logger.info("removing {}".format(lookup.screen_name))
            api.DestroyFriendship(screen_name=lookup.screen_name)
            removed = True
        looking = []


if __name__ == '__main__':
    main()
