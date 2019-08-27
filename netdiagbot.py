#coding:utf-8
__author__ = 'bsha3l173'

import telebot, socks, socket, os
from conf import TOKEN, PROXY_ADDR, PROXY_PORT
from log import Log

log = Log()

socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, PROXY_ADDR, PROXY_PORT)
socket.socket = socks.socksocket

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    name = ''
    if not message.from_user.first_name is None:
        name = message.from_user.first_name.encode('utf-8')
    if name == '':
        bot.send_message(message.chat.id, 'Привет! Я помогу вам продиагностировать сеть. Выберите нужную комманду.\nДля получения полного списка введите /help')
    else:
        bot.send_message(message.chat.id, 'Привет, {name}! Я помогу вам продиагностировать сеть. Выберите нужную комманду.\nДля получения полного списка введите /help'.format(name=name))
    log.log_d(message, '/start')

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, '/ping - Execute ping')
    log.log_d(message, '/help')

@bot.message_handler(commands=['ping'])
def ping_message(message, bol_wrong=False):
    if bol_wrong == False:
        ip = bot.send_message(message.chat.id, 'Укажите ip-адрес(v4)')
        log.log_d(message, '/ping -bol_wrong=False')
    else:
        ip = bot.send_message(message.chat.id, 'Некорректный ввод. Укажите ip-адрес(v4)')
        log.log_d(message, '/ping -bol_wrong=True')

    bot.register_next_step_handler(ip, ping)


def check_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def ping(message):
    if check_ip(message.text.encode('utf-8')):
        ip = message.text.encode('utf-8')
        bot.send_message(message.chat.id, 'Пингуем: {ip}...'.format(ip=message.text))
        log.log_d(message, '/ping ' + ip + '...' )
        response = os.system("ping -n 1 " + ip)
        if response == 0:
            bot.send_message(message.chat.id, '{ip} is up'.format(ip=message.text))
            log.log_d(message, '/ping - response: '+ ip + ' is up')
        else:
            bot.send_message(message.chat.id, '{ip} is down'.format(ip=message.text))
            log.log_d(message, '/ping - response: '+ ip + ' is down')
    else:
        log.log_d(message, '/ping - Incorrect ipaddr')
        ping_message(message, True)


def main():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        main()

main()
