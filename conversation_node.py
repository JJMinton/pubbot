import datetime
import random
import re

from utils import get_users
from loggers import blog

# node_structure: (bot_message, {user_response1: (bot_repsonse1, next_node1), user_response2: next_node2, ...})
# where next_nodex is a factory function or a class

class DirectMessageNode(object):

    def __init__(self, bot, channel,
                 bot_message=[""], user_responses={},
                 bail_out=None):
        self.bot = bot
        self.slack_client = bot.slack_client
        self.channel = channel
        self.last_response = datetime.datetime.now()

        self.user_responses = user_responses
        self.bail_out_option = bail_out or self

        self.post_message(random.choice(bot_message))
        blog.info(f"At {bot_message} node.")

    def handle_message(self, user, user_message):
        for response in self.user_responses:
            if re.search(response, user_message, re.IGNORECASE):
                if self.user_responses[response] and isinstance(self.user_responses[response], (list, tuple)): # TODO: use group
                    self.post_message(random.choice(self.user_responses[response][0]))
                    next_node = self.user_responses[response][1]
                else:
                    next_node = self.user_responses[response]

                if callable(next_node):
                    return next_node(self.bot, user, self.channel)
                elif next_node is None:
                    return next_node
                else:
                    raise TypeError("The next node provided is neither a function, nor None")

        self.post_message("Sorry, I don't know what to say.")
        log.debug(f"Unrecognised option: response are {self.user_response.keys()}")
        return self.bail_out_option

    def post_message(self, message):
        self.slack_client.api_call("chat.postMessage",
                                   channel=self.channel,
                                   text=message,
                                   as_user=True)
