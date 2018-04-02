import datetime

from utils import get_users
from loggers import blog

# structure: (message, {response1: next_node1, response2: next_node2, ...})


class DirectMessageNode(object):

    def __init__(self, slack_client, channel, choices, message="", bail_out=None):
        self._slack_client = slack_client
        self._channel = channel
        self.respond(random.choice(message))
        self._last_response = datetime.now()

        self.choices = choices
        self.bail_out_option = bail_out or self

    def process_message(self, user, message):
        for choice in choices:
            if re.search(choice, message, re.IGNORECASE):
                if len(choices[choice]) > 2:
                    choices[choice][2](self)
                if len(choices[choice]) > 1:
                    return DirectMessageNode(self._slack_client,
                                             self._channel,
                                             choices[choice][1],
                                             choices[choice][0],
                                             self.bail_out_option)
                return
        self.respond("Sorry, I don't know what to say.")
        return self.bail_out_option

    def respond(self, message):
        self._slack_client.api_call("chat.postMessage",
                                    channel=self._channel,
                                    text=message,
                                    as_user=True)
