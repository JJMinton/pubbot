from utils import get_users, get_username_from_id, post_message_to_channel
from loggers import blog

from conversation_node import DirectMessageNode
from greetings import greetings_factory
from pub import pub_trip_factory



def trigger_conversation(bot, user, channel):
    if channel[0] == "D":
        return greetings_factory(bot, user, channel)
    else:
        user_name = get_username_from_id(user, get_users(bot.slack_client))
        post_message_to_channel(bot.slack_client, channel,
                                f"<@ {user_name}> I'll message you.")
        # Talks to user who posted
        dmchannel = bot.slack_client.api_call("conversations.open",
                                              users=[user])
        blog.info(f"Triggered conversation with {user_name} " \
                  + f"with ID: {user}")
        if dmchannel['ok']:
            bot.handlers[channel] = greetings_factory(bot, user, dmchannel['channel']['id'])
            return None
        else:
            blog.warn(f"Cannot trigger pubbot with user: {user}")
         

def trigger_pub(bot, user, channel):
    if channel[0] == "D":
        return pub_trip_factory(bot, user, channel)
    else:
        users = get_users(bot.slack_client)
        user_name = get_username_from_id(user, users)
        blog.info(f"{user_name} triggered pub")

        post_message_to_channel(bot.slack_client, channel, 
            f"<@{get_username_from_id(user, users)}> "
            "Let's move to diect messages to organise "
            "this pub trip.")

        dmchannel = bot.slack_client.api_call("conversations.open",
                                              users=[user])
        if dmchannel['ok']:
            dmchannel = dmchannel['channel']['id']
            bot.handlers[dmchannel] = pub_trip_factory(bot, user, dmchannel)
            return None
        else:
            blog.warn(f"Cannot trigger pubbot with user: {user}")


trigger_keywords = ["pub", "pint", "thirst", "drink"]
trigger_node_factory = lambda bot, channel: DirectMessageNode(bot, channel, user_responses={
                                                "hello": trigger_conversation,
                                                ".*("+"|".join(trigger_keywords)+").*": trigger_pub,
                                                ".*": (["Sorry, I don't understand you. "
                                                       "To trigger pubbot use the following keywords: "
                                                       +", ".join(trigger_keywords)], None)
                                                })
