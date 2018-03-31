def get_users(sc):
    # TODO: Filter out bots
    api_call = sc.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        return users
    else:
        print("Failed to get users")
        return []
