from utils import get_users


class Command(object):
    def __init__(self, sc):
        self.sc = sc
        self.trigger_keywords = ["pub", "drink", "pint", "thirsty"]
        #self.commands = {
        #    "pub" : self.pub,
        #    "help" : self.help
        #}

    def handle_command(self, user, command):

        for word in self.trigger_keywords:
            if word in command:
                self.trigger()
                return ""

        return "Sorry I don't understand the command"

    def trigger(self):
        print("Triggered pub")
        for user in get_users(self.sc):
            print(f"Username: {user.get('name')} with ID: {user.get('id')}")
            channel = self.sc.api_call("conversations.open",
                                       users=[user.get('id')])
            if channel['ok']==True:
                channelid=channel['channel']['id']
                print(channelid)
                self.sc.api_call("chat.postMessage",
                                 channel=channelid,
                                 text="Fancy a pint?",
                                 as_user=True)
            else:
                print(f"Status is not ok for user: {user.get('id')}")
        return ""

    def help(self):
        response = "Currently I do xyz"

        return response
