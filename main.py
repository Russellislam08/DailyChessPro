import random

from flask import Flask, request, render_template
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAASDGuTBaFYBAIhnP3P4j5QOopRUndjpzVM4ZAwuPnsEuTPnd8RHdNPEKVVNPgrMc9tQt3OvmkPEpjaXr4uvNgXXPIsqIzFTJBaSTD7JUaZA3mZAp0VmZBIFrvcLCAP00KqIpVjALZCCvM6EgyVCydWAeQtfUlRdRgN3XNWAx8AZDZD'
VERIFY_TOKEN = 'this_is_test_token'
bot = Bot(ACCESS_TOKEN)

@app.route("/", methods=['GET'])
def receive_message():
    """ Return a friendly HTTP greeting. """
    return "Hello World!\n"
#    if request.method == 'GET':
#        token_sent = request.args.get("hub.verify_token")
#        return verify_fb_token(token_sent)
#    else:
#        output = request.get_json()
#        for event in output['entry']:
#           messaging = event['messaging']
#           for message in messaging:
#                if message.get('message'):
#                    #Facebook Messenger ID for user so we know where to send response back to
#                    recipient_id = message['sender']['id']
#                    if message['message'].get('text'):
#                        response_sent_text = get_message()
#                        send_message(recipient_id, response_sent_text)
#                    #if user sends us a GIF, photo,video, or any other non-text item
#                    if message['message'].get('attachments'):
#                        response_sent_nontext = get_message()
#                        send_message(recipient_id, response_sent_nontext)
#        return "Message Processed"


@app.route("/sendpuzzle", methods=['GET'])
def receive_message():
    """ Return a friendly HTTP greeting. """
    return "SENDING PUZZLE\n"

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Hello World"

#chooses a random message to send to the user
def get_message():
    # sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    sample_responses = ["I love you too baby! <3"]
    # return selected item to the user
    # return random.choice(sample_responses)
    return "Here is your random puzzle for the day: https://lichess.org/training. Best of luck! :)"

def puzzle_message():
    topics = ['opening', 'middlegame', 'endgame', 'rookEndgame', 'bishopEndgame', 'pawnEndgame', 'knightEndgame',
              'queenEndgame', 'queenRookEndgame']
    sample_responses = ["I love you too baby! <3"]
    return "Here is your random puzzle for the day: https://lichess.org/training. Best of luck! :)"

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == '__main__':
    app.run()

