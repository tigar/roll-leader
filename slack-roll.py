import os, slackclient, time
import random

# delay in seconds before checking for new events 
SOCKET_DELAY = 1
# slackbot environment variables
ROLL_SLACK_NAME = os.environ.get('ROLL_SLACK_NAME')
ROLL_SLACK_TOKEN = os.environ.get('ROLL_SLACK_TOKEN')
ROLL_SLACK_ID = os.environ.get('ROLL_SLACK_ID')
roll_slack_client = slackclient.SlackClient(ROLL_SLACK_TOKEN)

is_ok = roll_slack_client.api_call("users.list").get('ok')
print(is_ok)

# how the bot is mentioned on slack
def get_mention(user):
    return '<@{user}>'.format(user=user)

roll_slack_mention = get_mention(ROLL_SLACK_ID)

def is_private(event):
    """Checks if private slack channel"""
    return event.get('channel').startswith('D')

def is_for_me(event):
    # check if not my own event
    type = event.get('type')

    if type and type == 'message' and not(event.get('user')==ROLL_SLACK_ID):
        # in case it is a private message return true
        if is_private(event):
            return True
        # in case it is not a private message check mention
        text = event.get('text')
        channel = event.get('channel')
        if roll_slack_mention in text.strip().split():
            return True

def is_leader(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['leader', 'roll leader', 'lead', 'meeting lead'])


def say_leader(user_mention):
    """Say Hi to a user by formatting their mention"""
    response_template = random.choice(['<@tigar>', '@Ju Yun', '@Xingfan Xia', '@Lazar Zamurovic', '@Micah', '@Dan Mayer'])
    return response_template.format(mention=user_mention)


# def say_bye(user_mention):
#     """Say Goodbye to a user"""
#     response_template = random.choice(['see you later, alligator...',
#                                        'adios amigo',
#                                        'Bye {mention}!',
#                                        'Au revoir!'])
#     return response_template.format(mention=user_mention)

def handle_message(message, user, channel):
    if is_leader(message):
        user_mention = get_mention(user)
        post_message(message=say_leader(user_mention), channel=channel)

def post_message(message, channel):
    roll_slack_client.api_call('chat.postMessage', link_names=1, channel=channel,
                          text=message, as_user=True)
def run():
    if roll_slack_client.rtm_connect():
        print('[.] leader-roller is ON...')
        while True:
            event_list = roll_slack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    print(event)
                    if is_for_me(event):
                        handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')

if __name__=='__main__':
    run()