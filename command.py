from utils import get_users, get_username_from_id
from loggers import blog


class Command(object):
    def __init__(self, slack_client):
        self.slack_client = slack_client
        self.trigger_keywords = ["hello", "pub", "drink", "pint", "thirsty"]

    def handle_command(self, user, command, channel):
        # Triggers pubbot if words in command are trigger words
        for word in self.trigger_keywords:
            if word in command:
                self.trigger(user, channel)
                return

        # If message doesn't contain key words
        response =  "Sorry I don't understand the command.  Keywords are: "
        for word in self.trigger_keywords:
            response += word + ", "
        self.slack_client.api_call("chat.postMessage",
                                   channel=channel,
                                   text=response,
                                   as_user=True)
        return

    def trigger(self, user, channel):
        blog.debug("Triggered pub")

        users = get_users(self.slack_client)
        if channel[0] != "D":
            response = "<@" + str(get_username_from_id(user, users))\
                       + "> Let's move to diect messages to organise this pub trip."
            self.slack_client.api_call("chat.postMessage",
                                       channel=channel,
                                       text=response,
                                       as_user=True)

        #Talks to slackbot but no other bots
        for user in users:
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
