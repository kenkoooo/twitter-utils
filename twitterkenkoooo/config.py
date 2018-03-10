import json
from typing import List

import logzero
import twitter


class Config:
    def __init__(self, config_file: str):
        with open(config_file, "r") as f:
            config = json.load(f)
            self.consumer_key = config["consumer_key"]
            self.consumer_secret = config["consumer_secret"]
            self.access_token_key = config["access_token_key"]
            self.access_token_secret = config["access_token_secret"]
            self.followers_json = config["followers_json"]
            self.friends_json = config["friends_json"]
            logzero.logfile(config["log"])

    def get_api(self, sleep_on_rate_limit=True):
        return twitter.Api(consumer_key=self.consumer_key,
                           consumer_secret=self.consumer_secret,
                           access_token_key=self.access_token_key,
                           access_token_secret=self.access_token_secret,
                           sleep_on_rate_limit=sleep_on_rate_limit)

    def get_followers(self) -> List[int]:
        with open(self.followers_json, "r") as f:
            followers = json.load(f)
            followers.reverse()
        return followers

    def get_friends(self) -> List[int]:
        with open(self.friends_json, "r") as f:
            friends = json.load(f)
            friends.reverse()
        return friends
