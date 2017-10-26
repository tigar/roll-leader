import os, slackclient

ROLL_SLACK_NAME = os.environ.get('ROLL_SLACK_NAME')
ROLL_SLACK_TOKEN = os.environ.get('ROLL_SLACK_TOKEN')
# initialize slack client
valet_slack_client = slackclient.SlackClient(ROLL_SLACK_TOKEN)
# check if everything is alright
print(ROLL_SLACK_NAME)
print(ROLL_SLACK_TOKEN)
is_ok = valet_slack_client.api_call("users.list").get('ok')
print(is_ok)

# find the id of our slack bot
if(is_ok):
    for user in valet_slack_client.api_call("users.list").get('members'):
        if user.get('name') == ROLL_SLACK_NAME:
            print(user.get('id'))