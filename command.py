from utils import get_users
from loggers import blog


class Command(object):
    def __init__(self, slack_client):
        self.slack_client = slack_client
        self.trigger_keywords = ["hello", "pub", "drink", "pint", "thirsty"]
        #self.commands = {
        #    "pub" : self.pub,
        #    "help" : self.help
        #}

    def handle_command(self, user, command, channel):

        for word in self.trigger_keywords:
            if word in command:
                self.trigger(channel)
                return

        response =  "Sorry I don't understand the command"
        self.slack_client.api_call("chat.postMessage",
                                   channel=channel,
                                   text=response,
                                   as_user=True)
        return

    def trigger(self, channel):
        blog.debug("Triggered pub")

        if channel[0] != "D":
            print("message not in direct message")

        #Talks to slackbot but no other bots
        for user in get_users(self.slack_client):
            blog.debug(f"Username: {user.get('name')} with ID: {user.get('id')}")
            channel = self.slack_client.api_call("conversations.open",
                                                 users=[user.get('id')])
            if channel['ok']==True:
                channelid=channel['channel']['id']
                self.slack_client.api_call("chat.postMessage",
                                           channel=channelid,
                                           text="Fancy a pint?",
                                           as_user=True)
            else:
                blog.warn(f"Status is not ok for user: {user.get('id')}")
        return ""

    def help(self):
        response = "Currently I do xyz"

        return response
