import time
from slackclient import SlackClient

import config
from utils import get_users
from loggers import blog
from command import Command

class Bot(object):
    def __init__(self):
        self.slack_client = SlackClient(config.bot_user_oauth_token)
        self.bot_name = config.bot_name
        self.bot_id = self.get_bot_id()

        if self.bot_id is None:
            blog.error("Could not find bot: exiting")
            exit("Error, could not find " + self.bot_name)

        self.listen()

    # Gets the ID of the bot
    def get_bot_id(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = get_users(self.slack_client)
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    return "<@" + user.get('id') + ">"
            raise ValueError('The token does not match self.bot_name')

    # Listens for events being parsed
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

    # Checks to see if pubbot message has been sent
    def handle_events(self, events):
        for event in events:
            blog.debug("Triggered an event")
            #Check if its a direct message to the bot
            #or its @pubbot
            #If true pass to trigger node
            if event and 'text' in event and self.bot_id in event['text']:
                command = Command(self.slack_client)
                command.handle_command(event['user'],
                                       event['text'].split(self.bot_id)[1].strip().lower(),
                                       event['channel'])
            else:
                blog.info("Event not a message to bot")


if __name__ == "__main__":
    Bot()
