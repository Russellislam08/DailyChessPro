from random import choice
from urllib.request import urlopen
import os
import re

import requests
from flask import Flask, request
from pymessenger.bot import Bot

from dal import add_user, get_user, get_all_users, delete_user

app = Flask(__name__)
ACCESS_TOKEN = os.environ.get('REDIRECT_URI')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
BOT = Bot(ACCESS_TOKEN)


@app.route("/sendpuzzle", methods=['GET', 'POST'])
def send_daily_puzzle():
    users = get_all_users()
    [send_message(user.get('user_id'), puzzle_message()) for user in users]
    return "Sent daily puzzle!"
	

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
                    recipient_id = message['sender']['id']
                    msg = message['message'].get('text')
                    if msg:
                        send_return_message(msg, recipient_id)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    # if message['message'].get('attachments'):
                    #     response_sent_nontext = puzzle_message()
                    #     send_message(recipient_id, response_sent_nontext)
        return "Message Processed"


def send_return_message(msg, recipient_id):
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
        message6 = "👉 \"Commands\": Shows you all of the available commands, which are also shown here."
        message7 = "👉 \"Subscribe\": Use this command to initialize daily puzzles, if haven't done so already."
        message8 = "👉 \"Send Puzzle\": Use to receive a random puzzle"
        message9 = "👉 \"Unsubscribe\": Unsubscribe from daily problems."
        message10 = "👉 \"Status\": Check to see if you are getting daily puzzles. 🧩"

        send_message(recipient_id, message1)
        send_message(recipient_id, message2)
        send_message(recipient_id, message3)
        send_message(recipient_id, message4)
        send_message(recipient_id, message5)
        send_message(recipient_id, message6)
        send_message(recipient_id, message7)
        send_message(recipient_id, message8)
        send_message(recipient_id, message9)
        send_message(recipient_id, message10)

    elif msg == "commands":
        message1 = "Here is a list of the commands that you may use:"
        message2 = "👉 \"Help\": Explanation of the bot."
        message3 = "👉 \"Commands\": This command."
        message4 = "👉 \"Subscribe\": Use this command to initialize daily puzzles, if haven't done so already."
        message5 = "👉 \"Send Puzzle\": Use to receive a random puzzle"
        message6 = "👉 \"Unsubscribe\": Unsubscribe from daily puzzles."
        message7 = "👉 \"Status\": Check to see if you are getting daily puzzles. 🧩"

        send_message(recipient_id, message1)
        send_message(recipient_id, message2)
        send_message(recipient_id, message3)
        send_message(recipient_id, message4)
        send_message(recipient_id, message5)
        send_message(recipient_id, message6)
        send_message(recipient_id, message7)


    elif msg == "hi" or msg == "hello" or msg == "hey":
        message = "Hey there! :)"
        send_message(recipient_id, message)
        send_return_message("help", recipient_id)

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
        message1 = "Sorry 😥 I did not understand that command. Type \"help\" if you want to see what I can do."
        send_message(recipient_id, message1)


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verify endpoint has been triggered"


def puzzle_message():
    topics = ['opening', 'middlegame', 'endgame', 'rookEndgame', 'bishopEndgame', 'pawnEndgame', 'knightEndgame',
              'queenEndgame', 'queenRookEndgame', 'advancedPawn', 'attackingF2F7', 'capturingDefender', 'discoveredAttack',
              'doubleCheck', 'exposedKing', 'fork', 'hangingPiece', 'kingsideAttack', 'pin', 'queensideAttack', 'sacrifice'
              'skewer', 'trappedPiece', 'attraction', 'clearance' 'defensiveMove', 'deflection', 'interference', 'intermezzo',
              'quietMove', 'xRayAttack', 'zugzwang']

    base_url = "https://lichess.org/training/{}"
    url = base_url.format(choice(topics))

    return "Here is your random puzzle for you to attempt:\n{}\nBest of luck! :)".format(url)

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    BOT.send_text_message(recipient_id, response)
    return "success"


if __name__ == '__main__':
    app.run()
