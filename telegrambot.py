from config import TELEGRAM_SEND_MESSAGE_URL
import requests
import time
import json


class TelegramBot:

    def __init__(self):

        self._chat_id = None  # chat id for specific conversation
        self._text = None  # incoming message
        self._name = None  # the name of the user that had sent the message
        self._history = {}  # a dictionary to save the data
        self._chatids = [] # to save all chat ids that ever communicate this bot
        self.init_ids()

    def init_ids(self):
        with open('chat_ids.txt', 'r') as file:
            all = file.read()
        print("in id init   --------- ", all.split(',')[:-1])
        temp = all.split(',')[:-1]
        for sid in temp:
            self._chatids.append(int(sid))

    def parse_webhook_data(self, data):

        message = data.get('message')
        if message is None:
            message = data.get('edited_message')

        # parsing the data
        chatid = message['chat']['id']
        in_msg = message.get('text')  # if it have one
        name = message['from']['first_name']
        if message['from'].get('last_name') is not None:  # if it have last name
            name = name + str(message['from'].get('last_name'))

        self._chat_id = chatid
        if chatid not in self._chatids:
            with open('chat_ids.txt', 'a') as f:
                f.write(str(chatid) + ',')
            self._chatids.append(chatid)

        if in_msg is None:
            self.incoming_message_text = ""
        else:
            self.incoming_message_text = in_msg.lower()

        self._name = name
        key = message.get('message_id')
        self._history[key] = message

    # what to replay to the message parsing specific messages and send the message to the telegram servers
    def replay(self):

        if self.incoming_message_text == 'hello':
            self.outgoing_message_text = "Hello {}!".format(self._name)

        elif self.incoming_message_text == 'how are you?':
            self.outgoing_message_text = 'fine thank you'

        elif self.incoming_message_text == 'are you a telegram bot?':
            self.outgoing_message_text = "yes I'm"

        elif self.incoming_message_text == 'what is my chat id?':
            self.outgoing_message_text = "you'r chat id is {}".format(self._chat_id)

        else:
            self.outgoing_message_text = "I can't answer that, try:\nhello | how are you? | are you a telegram bot? | what is my chat id?"

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self._chat_id, self.outgoing_message_text))

        if_answerd = (res.status_code == 200)
        if if_answerd:
            self._history["answer"] = self.outgoing_message_text

        with open("history.json", "a") as f:
            json.dump(self._history, f)

        return if_answerd

        # the auto send message, send a message every minute to all users that ever communicates the bot

    def auto_send(self):

        print(self._chatids)
        while (1):

            for chatid in self._chatids:
                res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(chatid, "this is the auto msg"))
                print(res.status_code)
            time.sleep(30)


