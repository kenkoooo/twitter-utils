import json

import logzero


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
