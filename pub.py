import re
import random

from loggers import blog
from utils import get_users
from conversation_node import DirectMessageNode
from location import location_factory

# node_structure: (bot_message, {user_response1: (bot_repsonse1, next_node1), user_response2: next_node2, ...})

def choose_pub_factory(bot, original_user, original_channel):
    #Talks to slackbot but no other bots
    users = get_users(bot.slack_client)
    for user in [u for u in users if u != original_user]:
        blog.debug(f"Username: {user.get('name')} " \
                   + f"with ID: {user.get('id')}")
        channel = bot.slack_client.api_call("conversations.open",
                                            users=[user.get('id')])
        if (channel['ok']
                and 'channel' in channel
                and 'id' in channel['channel']
                and channel['channel']['id'] != original_channel):
            channel_id = channel['channel']['id']
            bot.handlers[channel_id] \
                = DirectMessageNode(bot, channel_id,
                                    ['Fancy a pint?'],
                                    {'.*': (['Cool'], None)}
                                   )
        else:
            blog.warn(f"Status is not ok for user: {user.get('id')}")
    #Print I've messaged everyone for you.
    return DirectMessageNode(bot, original_channel,
                             ["I've messaged everyone for you"],
                             {'.*':location_factory})
    #print ("Returning location factory")
    #return location_factory

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
                                    "Your loss."
                                    ],
                                    None
                                   ),
       }
       )
pub_trip_factory = lambda bot, user, channel: DirectMessageNode(bot, channel, *pub)
