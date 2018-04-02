from utils import get_users, get_username_from_id
from loggers import blog

from greetings import greetings_factory


class TriggerMessageNode(object):

    def __init__(self, slack_client, channel, bail_out=None):
        self._slack_client = slack_client
        self._channel = channel
        self._trigger_keywords = ["pub", "drink", "pint", "thirsty"]

        self.bail_out_option = bail_out or self

    def handle_message(self, user, user_message):
        if "hello" in user_message:
            return self.trigger_conversation(user)

        # Triggers pubbot if words in command are trigger words
        for word in self._trigger_keywords:
            if word in user_message:
                self.trigger_pub_command(user)
                return

        # TODO: add generic bail out
        self.post_message("Sorry, I don't understand you. " \
            + "To trigger pubbot use the following keywords: " \
            + ", ".join(self._trigger_keywords), self._channel)
        return self.bail_out_option

    def trigger_conversation(self, user):
        user_name = get_username_from_id(user, get_users(self._slack_client))
        if self._channel[0] != "D":
            self.post_message("<@" \
                + str(user_name)
                + ">"\
                + " I'll message you.", self._channel)
        blog.info(f"Triggered conversation with {user_name} " \
                  + f"with ID: {user}")

        # Talks to user who posted
        dmchannel = self._slack_client.api_call("conversations.open",
                                               users=[user])
        if dmchannel['ok']:
            return greetings_factory(self._slack_client,
                                     dmchannel['channel']['id'])
        else:
            blog.warn(f"Cannot trigger pubbot with user: {user}")

    def trigger_pub_command(self, user, channel):
        blog.info("Triggered pub")

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

    def post_message_to_channel(self, message, channel):
        self._slack_client.api_call("chat.postMessage",
                                    channel=channel,
                                    text=message,
                                    as_user=True)
