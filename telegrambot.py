from config import TELEGRAM_SEND_MESSAGE_URL
import requests
import time



class TelegramBot:

    def __init__(self):

        self._chat_id = None   # chat id for specific conversation
        self._text = None      # incoming message
        self._name = None      # the name of the user that had sent the message
        self._chatids = []     # to save all incoming chatids


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
            self._chatids.append(chatid)

        if(in_msg == None):
            self.incoming_message_text = ""
        else:
            self.incoming_message_text = in_msg.lower()

        self._name = name


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

        return True if res.status_code == 200 else False

    # send the message to the telegram servers
    def send_message(self):

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self._chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False


    # the auto send message, send a message every minute to all users that ever communicates the bot
    def auto_send(self):

        while(1):

            print (self._chatids)
            for id in self._chatids:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(id, "this is the auto msg"))

            time.sleep(60)


