from loggers import blog

def get_users(slack_client):
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        return users
    else:
        blog.info("Failed to get users")
        return []

def get_username_from_id(userid, users):
    for user in users:
       if user['id'] == userid:
           return user['name']
    blog.warn(f"No username for: {user['id']}")
    return ""

def post_message_to_channel(slack_client, channel, message):
    slack_client.api_call("chat.postMessage",
                          channel=channel,
                          text=message,
                          as_user=True)
