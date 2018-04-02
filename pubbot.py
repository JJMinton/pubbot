import time
from slackclient import SlackClient

import config
from utils import get_users
from loggers import blog
from trigger_node import TriggerMessageNode

class Bot(object):
    def __init__(self):
        self.slack_client = SlackClient(config.bot_user_oauth_token)
        self.bot_name = config.bot_name
        self.bot_id = self.get_bot_id()
        self.handlers = {}

        if self.bot_id is None:
            blog.error("Could not find bot: exiting")
            exit("Error, could not find " + self.bot_name)

        self.listen()

    def get_bot_id(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = get_users(self.slack_client)
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    return user.get('id')
            raise ValueError('The token does not match self.bot_name')

    def listen(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            blog.info("Successfully connected, listening for commands")
            while True:
                events = self.slack_client.rtm_read()
                if events and len(events) > 0:
                    self.handle_events(events)
                time.sleep(1)
        else:
            blog.error("Connection failed: exiting")
            exit("Error, Connection Failed")

    def handle_events(self, events):
        for event in events:
            blog.debug("Triggered an event")
            # TODO: not from any bot
            if 'text' in event and 'user' in event and event['user']!=self.bot_id:
                if 'channel' in event and event['channel']:
                    channel = event['channel']
                    blog.debug(f"Received: {event['text']}")
                    if channel in self.handlers.keys() and self.handlers[channel]:
                        self.handlers[channel] = \
                            self.handlers[channel].handle_message(event['user'],
                                                                  event['text'])
                    else:
                        blog.info("Using default handler.")
                        self.handlers[channel] = TriggerMessageNode(self.slack_client, channel)
                        self.handlers[channel] = \
                            self.handlers[channel].handle_message(event['user'],
                                                                  event['text'])
            else:
                blog.debug("Event not a message to bot")


if __name__ == "__main__":
    Bot()
