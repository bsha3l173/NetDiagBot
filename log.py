__author__ = 'bsha3l173'

import logging
import datetime
from conf import LOG_FILENAME

class Log():

    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

    def log_d(self, message, text):
        last_name = ''
        first_name = ''
        user_name = ''
        if not message.from_user.first_name is None:
            first_name = message.from_user.first_name.encode('utf-8') + ' '
        if not message.from_user.last_name is None:
            last_name = message.from_user.last_name.encode('utf-8') + ' '
        if not message.from_user.username is None:
            user_name = '(' + message.from_user.username.encode('utf-8') + ')'

        name = last_name + first_name + user_name
        logging.debug(str(datetime.datetime.now()) + ' ' + str(message.chat.id) + ' ' + name + ': ' + text)

