import re
import random

from conversation_node import DirectMessageNode



congrats = (['Thats great to hear'],
            {'.*': None}
            )

comiserations = (['Im sorry to hear that'],
                 {'.*': None}
                 )

hows_my_day = (['Great, I guess. How was yours?',
                'Not bad but been better, you?',
                'Frankly, pretty rubbish. Yours better?',
                ],
               {'.*(good|great|excellent).*': congrats,
                '.*(bad|terrible|rubbish|wors.*).*': comiserations,
                'do.*worry.*': None,
                }
               )


hows_your_day = (['Hows your day'],
                 {'.*(good|great|excellent).*': congrats,
                  '.*(bad|terrible|rubbish|wors.*).*': comiserations,
                  'do.*worry.*': None,
                  }
                 )
                    
hello = (['Hi!',
          'Hello...',
          "G'day",
          'Greetings',
          'Welcome',
          ],
         {
          'h(i|ello|ey)': hows_your_day,
          '.*how.*day.*': hows_my_day,
          }
         )

greetings_factory = lambda slack_client, channel: DirectMessageNode(slack_client, channel, hello[1], hello[0])
