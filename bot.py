import time
import event
import os
from slackclient import SlackClient

import config

class Bot(object):
    def __init__(self):
        self.slack_client = SlackClient(config.bot_user_oauth_token)
        self.bot_name = config.bot_name
        self.bot_id = self.get_bot_id()

        if self.bot_id is None:
            exit("Error, could not find " + self.bot_name)

        self.event = event.Event(self)
        self.listen()

    def get_bot_id(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    return "<@" + user.get('id') + ">"
            raise ValueError('The token does not match self.bot_name')

    def listen(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print ("Successfully connected, listening for commands")
            while True:
                self.event.wait_for_event()
                time.sleep(1)
        else:
            exit("Error, Connection Failed")


def get_users():
    # TODO: Filter out bots
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        return users
    else:
        print("Failed to get users")
        print(api_call.keys())
        return []
