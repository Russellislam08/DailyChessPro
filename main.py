from random import choice
import re
from urllib.request import urlopen

# from bs4 import BeautifulSoup
import requests

from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAASDGuTBaFYBAIhnP3P4j5QOopRUndjpzVM4ZAwuPnsEuTPnd8RHdNPEKVVNPgrMc9tQt3OvmkPEpjaXr4uvNgXXPIsqIzFTJBaSTD7JUaZA3mZAp0VmZBIFrvcLCAP00KqIpVjALZCCvM6EgyVCydWAeQtfUlRdRgN3XNWAx8AZDZD'
VERIFY_TOKEN = 'this_is_test_token'
bot = Bot(ACCESS_TOKEN)

@app.route("/", methods=['GET', 'POST'])
def receive_message():

    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
           messaging = event['messaging']
           for message in messaging:
                print(message)
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    msg = message['message'].get('text')
                    if msg:
                        # msg = message['message'].get('text')
                        send_return_message(msg, recipient_id)
                        # response_sent_text = get_message()
                        # response_sent_text = puzzle_message()
                        # send_message(recipient_id, response_sent_text)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        # response_sent_nontext = get_message()
                        response_sent_nontext = puzzle_message()
                        send_message(recipient_id, response_sent_nontext)
        return "Message Processed"


def send_return_message(msg, recipient_id):
    print("This is the message: ")
    print(msg)

    if msg.lower().replace(' ', '') == "getstarted":
        print("This clause happened")

        message1 = "♟️ Welcome to the Chess bot! This bot will periodically send you chess puzzles for you to do. ♟️"
        message2 = "Chess puzzles are a good way to improve your skills as a chess player and are great exercises to do often."
        message3 = "You will receive a chess puzzle everyday at 20:00 EST. 👍 "


        send_message(recipient_id, message1)
        send_message(recipient_id, message2)
        send_message(recipient_id, message3)

    elif msg.lower().replace(' ', '') == "sendpuzzle":
        send_message(recipient_id, puzzle_message())

    else:
        # if they are registered
        message1 = "That is not a command. You can perform the following operations:"
        message2 = "'Get Started' to register for getting sent puzzles."
        message3 = "'Send Puzzle' to send a puzzle"

        send_message(recipient_id, message1)
        send_message(recipient_id, message2)
        send_message(recipient_id, message3)
        



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

# def get_id(url):

#     webpage = urlopen(url)
#     soup = BeautifulSoup(webpage, 'html.parser')
#     title = soup.find("meta",  property="og:title")
#     for tag in soup.find_all("meta"):
#         if tag.get("property", None) == "og:title":
#             puzzle_id = tag.get("content", None)
#         elif tag.get("property", None) == "og:url":
#             puzzle_id = tag.get("content", None)
#     print("This is puzzle id: ", puzzle_id)
#     puzzle_id = re.search("#[a-zA-Z0-9]{5}",puzzle_id).group().replace("#", "")

#     # r = requests.get(url)
#     # if r.status_code == 200:
#     # puzzle_id = re.search("#[a-zA-Z0-9]{5}",).group().replace("#", "")
#     return puzzle_id

def puzzle_message():
    topics = ['opening', 'middlegame', 'endgame', 'rookEndgame', 'bishopEndgame', 'pawnEndgame', 'knightEndgame',
              'queenEndgame', 'queenRookEndgame', 'advancedPawn', 'attackingF2F7', 'capturingDefender', 'discoveredAttack',
              'doubleCheck', 'exposedKing', 'fork', 'hangingPiece', 'kingsideAttack', 'pin', 'queensideAttack', 'sacrifice'
              'skewer', 'trappedPiece', 'attraction', 'clearance' 'defensiveMove', 'deflection', 'interference', 'intermezzo',
              'quietMove', 'xRayAttack', 'zugzwang']

    

    # url = "https://lichess.org/training/{}".format(choice(topics))
    base_url = "https://lichess.org/training/{}"
    # url = get_id("https://lichess.org/training/{}".format(choice(topics)))
    # url = base_url.format(get_id(base_url.format(choice(topics))))
    url = base_url.format(choice(topics))

    return "Here is your random puzzle for you to attempt:\n{}\nBest of luck! :)".format(url)

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == '__main__':
    print("App is now running...")
    app.run()

