import re
import random

from conversation_node import DirectMessageNode

# node_structure: (bot_message, {user_response1: (next_node1, bot_repsonse1), user_response2: next_node2, ...})

pub = (["Fancy a pint?",
        "Do you want to go to the pub?",
        "Are you thirsty?",
        "Want a drink?",
        "Pub time?",
       ],
       {
        '.*y(es|eah|)|of course.*': (pub_trip,
                                     ["Great - let's get organsiing!",
                                      "Cool, I'll invite the others",
                                      "Finally, I've been wanting a drink all day!"
                                     ]
                                     )
        '.*n(o|ot today|ah).*': (no_pub_trip,
                                 ["We'll miss you.",
                                  "Maybe next time?",
                                  "Your loss"
                                 ]
                                )
       }
      )

pub_trip_factory = lambda slack_client, channel: DirectMessageNode(slack_client,
                                                                   channel,
                                                                   pub[1],
                                                                   pub[0])
