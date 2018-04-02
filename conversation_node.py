import datetime
import random

from utils import get_users
from loggers import blog

# node_structure: (bot_message, {user_response1: (next_node1, bot_repsonse1), user_response2: next_node2, ...})

class DirectMessageNode(object):

    def __init__(self, slack_client, channel,
                 user_responses, bot_message=[""], bail_out=None):
        self._slack_client = slack_client
        self._channel = channel
        self._last_response = datetime.datetime.now()

        self.user_responses = user_responses
        self.bail_out_option = bail_out or self

        self.post_message(random.choice(bot_message))

    def handle_message(self, user, user_message):
        for response in self.user_responses:
                if not isinstance(self.user_responses[response], tuple):
                    self.user_responses[response] = (self.user_responses[response],)
                if len(self.user_responses[response]) > 1:
                    self.post_message(self.user_responses[response][1])
                return DirectMessageNode(self._slack_client,
                                         self._channel,
                                         self.user_responses[response][0][1],
                                         self.user_responses[response][0][0],
                                         self.bail_out_option)
        # TODO: add generic exit options
        self.post_message("Sorry, I don't know what to say.")
        return self.bail_out_option

    def post_message(self, message):
        self._slack_client.api_call("chat.postMessage",
                                    channel=self._channel,
                                    text=message,
                                    as_user=True)
