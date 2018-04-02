import re
import random

from loggers import blog
from utils import get_users
from conversation_node import DirectMessageNode

# node_structure: (bot_message, {user_response1: (next_node1, bot_repsonse1), user_response2: next_node2, ...})

def choose_pub_factory(bot, original_user, original_channel):
    #Talks to slackbot but no other bots
    users = get_users(bot.slack_client)
    for user in [u for u in users if u != original_user]:
        blog.debug(f"Username: {user.get('name')} " \
                   + f"with ID: {user.get('id')}")
        channel = bot.slack_client.api_call("conversations.open",
                                            users=[user.get('id')])
        if channel['ok']:
            channel = channel['channel']['id']
            #TODO: don't set original_user's handler
            bot.handlers[channel] = DirectMessageNode(bot, channel, ['Fancy a pint?'], {'.*': (['Cool'], None)})
        else:
            blog.warn(f"Status is not ok for user: {user.get('id')}")
    return DirectMessageNode(bot, original_channel, ["I've messaged everyone for you"], {'.*': (['Have a good time'], None)})

pub = (["Fancy a pint?",
        "Do you want to go to the pub?",
        "Are you thirsty?",
        "Want a drink?",
        "Pub time?",
       ],
       {
        '.*y(es|eah|)|of\s+course.*': (
                                       ["Great - let's get organising!",
                                        "Cool, I'll invite the others",
                                        "Finally, I've been wanting a drink all day!"
                                        ],
                                        choose_pub_factory
                                       ),
        '.*n(o|ot\s+today|ah).*': (
                                   ["We'll miss you.",
                                    "Maybe next time?",
                                    "Your loss"
                                    ],
                                    None
                                   ),
       }
       )
pub_trip_factory = lambda bot, user, channel: DirectMessageNode(bot, channel, *pub)
