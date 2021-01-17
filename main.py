from random import choice
from urllib.request import urlopen
import re

# from bs4 import BeautifulSoup
import requests
from flask import Flask, request
from pymessenger.bot import Bot

from dal import add_user, get_user, get_all_users

app = Flask(__name__)
ACCESS_TOKEN = 'EAASDGuTBaFYBAIhnP3P4j5QOopRUndjpzVM4ZAwuPnsEuTPnd8RHdNPEKVVNPgrMc9tQt3OvmkPEpjaXr4uvNgXXPIsqIzFTJBaSTD7JUaZA3mZAp0VmZBIFrvcLCAP00KqIpVjALZCCvM6EgyVCydWAeQtfUlRdRgN3XNWAx8AZDZD'
VERIFY_TOKEN = 'this_is_test_token'
BOT = Bot(ACCESS_TOKEN)

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
                        send_return_message(msg, recipient_id)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        # response_sent_nontext = get_message()
                        response_sent_nontext = puzzle_message()
                        send_message(recipient_id, response_sent_nontext)
        return "Message Processed"


def send_return_message(msg, recipient_id):
    print(msg)

    msg = msg.lower().replace(' ', '')

    if msg == "subscribe":

        if get_user(recipient_id):
            message1 = "You are already subscribed for daily chess puzzles!"

            send_message(recipient_id, message1)

        else:
            add_user(recipient_id)

            message1 = "You have subscribed for daily chess puzzles! :)"
            message2 = "You will receive a chess puzzle everyday at 20:00 EST. 👍 "
            message3 = "Chess puzzles are powered by lichess.org"

            send_message(recipient_id, message1)
            send_message(recipient_id, message2)
            send_message(recipient_id, message3)

    elif msg == "sendpuzzle":
        send_message(recipient_id, puzzle_message())

    elif msg == "status":
        # if registered
        message = "You are currently {} for daily chess puzzles.".format(
            "REGISTERED" if get_user(recipient_id) else "NOT REGISTERED")

        send_message(recipient_id, message)

    elif msg == "help":
        message1 = "♟️ Welcome to the Daily Chess Bot!️. This Messenger bot can send you daily chess puzzles for you to do. ♟️"
        message2 = ("Chess puzzles are a good way to improve your skills as a chess player and are great exercises to do often. " +
                   "Super Chess Grandmasters such as Hikaru Nakamura do puzzles regularly.")
        message3 = "Chess puzzles are powered by lichess.org"

        message4 = "Here is a list of the commands that you may use:"
        message5 = "👉 \"Help\": This command."
        message6 = "👉 \"Subscribe\": Use this command to initialize daily puzzles, if haven't done so already."
        message7 = "👉 \"Send Puzzle\": Use to receive a random puzzle"
        message8 = "👉 \"Unsubscribe\": Unsubscribe from daily problems."
        message9 = "👉 \"Status\": Check to see if you are getting daily puzzles. 🧩"

        send_message(recipient_id, message1)
        send_message(recipient_id, message2)
        send_message(recipient_id, message3)
        send_message(recipient_id, message4)
        send_message(recipient_id, message5)
        send_message(recipient_id, message6)
        send_message(recipient_id, message7)
        send_message(recipient_id, message8)
        send_message(recipient_id, message9)

    elif msg == "unsubscribe":
        if delete_user(recipient_id):

            message1 = "❌ You have unsubscribed from the daily puzzles."
            message2 = "To subscribe again in the future, use the subscribe command to do so."

            send_message(recipient_id, message1)
            send_message(recipient_id, message2)
        else:
            message1 = "You are currently not subscribed for daily puzzles."
            message2 = "There is no need to unsubscribe! :)"

            send_message(recipient_id, message1)
            send_message(recipient_id, message2)


    else:
        message1 = "Sorry 😥 I did not understand that command. Type help if you require assistance."
        send_message(recipient_id, message1)


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verify endpoint has been triggered"

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

    

    base_url = "https://lichess.org/training/{}"
    # url = get_id("https://lichess.org/training/{}".format(choice(topics)))
    url = base_url.format(choice(topics))

    return "Here is your random puzzle for you to attempt:\n{}\nBest of luck! :)".format(url)

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    BOT.send_text_message(recipient_id, response)
    return "success"


if __name__ == '__main__':
    print("App is now running...")
    app.run()
