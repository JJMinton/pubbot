import re
import random

from loggers import blog
from utils import get_users
from conversation_node import DirectMessageNode

# node_structure: (bot_message, {user_response1: (bot_repsonse1, next_node1), user_response2: next_node2, ...})

def find_local_pubs_factory(bot, user, channel):

    return DirectMessageNode(bot, channel,
                             ["Found you a pub"],
                             {'.*': (['Enjoy the pub!'], None)})

where = (["Any ideas where?",
        "Where do you want to go?"
       ],
       {
        '.*(near|close).*': ( ["Okay - I'll suggest something.",
                               "Great.",
                              ],
                              find_local_pubs_factory
                              ),
        '.*n(o|ot\s+today|ah).*': (
                                   ["I'll suggest something nearby.",
                                    "Okay.",
                                    "Not to worry - I'll find some options."
                                    ],
                                    None
                                   ),
        '.*': (
            ["Great - let's get organising!",
             "Cool, I'll invite the others",
             "Finally, I've been wanting a drink all day!"
            ],
            None
        ),
       }
       )

location_factory = lambda bot, user, channel: DirectMessageNode(bot, channel, *where)
