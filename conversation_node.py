import datetime
import random
import re

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
        blog.info(f"At {bot_message} node.")

    def handle_message(self, user, user_message):
        for response in self.user_responses:
            if re.search(response, user_message, re.IGNORECASE):
                if self.user_responses[response] and isinstance(self.user_responses[response][1], str):
                    self.post_message(self.user_responses[response][1])
                if self.user_responses[response] is None or self.user_responses[response][0] is None:
                    return None
                if isinstance(self.user_responses[response][1], dict):
                    response = self.user_responses[response]
                else:
                    response = self.user_responses[response][0]
                return DirectMessageNode(self._slack_client,
                                         self._channel,
                                         response[1],
                                         response[0],
                                         self.bail_out_option)
        # TODO: add generic exit options
        self.post_message("Sorry, I don't know what to say.")
        log.debug(f"Unrecognised option: response are {self.user_response.keys()}")
        return self.bail_out_option

    def post_message(self, message):
        self._slack_client.api_call("chat.postMessage",
                                    channel=self._channel,
                                    text=message,
                                    as_user=True)
