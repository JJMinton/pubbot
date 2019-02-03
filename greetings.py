import re
import random

from conversation_node import DirectMessageNode
from pub import pub_trip_factory

# node_structure: (bot_message, {user_response1: (next_node1, bot_repsonse1), user_response2: next_node2, ...})


congrats = (['Thats great to hear'],
            {'.*': pub_trip_factory}
            )
congrats_nf = lambda bot, user, channel: DirectMessageNode(bot, channel, *congrats)

comiserations = (['Im sorry to hear that'],
                 {'.*': (["I've run out of conversation, bye."], None)}
                 )
comiserations_nf = lambda bot, user, channel: DirectMessageNode(bot, channel, *comiserations)

hows_my_day = (['Great, I guess. How was yours?',
                'Not bad but been better, you?',
                'Frankly, pretty rubbish. Yours better?',
                ],
               {'.*(yes|good|great|excellent).*': congrats_nf,
                '.*(no|bad|terrible|rubbish|wors.*).*': comiserations_nf,
                'do.*worry.*': None,
                }
               )
hows_my_day_nf = lambda bot, user, channel: DirectMessageNode(bot, channel, *hows_my_day)

hows_your_day = (['Hows your day?'],
                 {'.*(good|great|excellent).*': congrats_nf,
                  '.*(bad|terrible|rubbish|wors.*).*': comiserations_nf,
                  'do.*worry.*': None,
                  }
                 )
hows_your_day_nf = lambda bot, user, channel: DirectMessageNode(bot, channel, *hows_your_day)

hello = (['Hi!',
          'Hello...',
          "G'day",
          'Greetings',
          'Welcome',
          ],
         {
          'h(i|ello|ey)': hows_your_day_nf,
          '.*how.*day.*': hows_my_day_nf,
          }
         )
greetings_factory = lambda bot, user, channel: DirectMessageNode(bot, channel, *hello)
