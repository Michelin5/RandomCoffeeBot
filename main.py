import telebot
import os
from telebot import types
from base import Base, User
from log import BotLogger


logger = BotLogger('bot.log')

base = Base()
TOKEN = os.getenv('BOT_API_KEY')
bot = telebot.TeleBot('5655668531:AAEZMRXM8ymp0sNohNcXnL4v-T-aetN0s5Y')

@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    help_b = types.KeyboardButton('help')
    questionnaire = types.KeyboardButton('questionnaire')
    info_b = types.KeyboardButton('info')
    connect = types.KeyboardButton('connect')
    markup.add(help_b, questionnaire, info_b, connect)
    bot.send_message(message.chat.id, 'Menu', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'help':
        help_com(message)
    elif message.text == 'questionnaire':
        start_questionnaire(message)
    elif message.text == 'connect':
        checker = base.find_group(message.from_user.id)
        if checker == None:
            base.create_group(message.from_user.id)
        else:
            base.add_to_group(checker,message.from_user.id)

    talk(message)
    bot.register_next_step_handler(message, on_click)


questions = [
    "Твой пол? М/Ж",
    "Сколько тебе лет?",
    "В каком городе ты живешь?",
    "Выбери 3 интереса из списка и отправь мне",
    "Осталось два",
    "И еще один"
]

user_responses = {}


def start_questionnaire(message):
    user_id = message.from_user.id
    user_responses[user_id] = []
    ask_question(message)


def ask_question(message):
    user_id = message.from_user.id
    logger.log_info(f"Получено сообщение от пользователя {message.from_user.id}: {message.text}")
    current_question_index = len(user_responses[user_id])
    if current_question_index < len(questions):
        current_question = questions[current_question_index]
        bot.send_message(message.chat.id, current_question)
        bot.register_next_step_handler(message, process_answer)
    else:
        print(user_responses[user_id])
        bot.send_message(message.chat.id, "Анкета заполнена! \n /menu - вернуться в меню \n /connect - запустить процесс поиска новой группы")
        new_user = User(user_id, user_responses[user_id][0], user_responses[user_id][1], user_responses[user_id][2], [user_responses[user_id][3], user_responses[user_id][4], user_responses[user_id][5]])
        del(user_responses[user_id])
        usr = base.get_user_by_tg_id(new_user.tg)
        if (usr == None):
            base.create_user(new_user)
        else:
            base.update_user(new_user)


def process_answer(message):
    user_id = message.from_user.id
    current_question_index = len(user_responses[user_id]) - 1
    current_question = questions[current_question_index]
    user_responses[user_id].append(message.text)
    ask_question(message)


@bot.callback_query_handler(func=lambda call: True)
def pullback(callback):
    if callback.message:
        if callback.data == 'help':
            help_com(callback.message)
        elif callback.data == 'questionnaire':
            start_questionnaire(callback.message)
        elif callback.data == 'connect':
            checker = base.find_group(callback.message.from_user.id)
            if checker == None:
                base.create_group(callback.message.from_user.id)
            else:
                base.add_to_group(checker, callback.message.from_user.id)



@bot.message_handler(commands=['start'])
def main(message):
    if message.from_user.last_name == None:
        bot.reply_to(message, f'Привет, {message.from_user.first_name}')
    else:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
    logger.log_info(f"Пользователь {message.from_user.id} запустил бота командой /start")
    bot.send_message(message.chat.id, 'Рад, что вы решили воспользоваться моими услугами!')
    bot.send_message(message.chat.id, 'Чтобы открыть меню, введите /menu')


@bot.message_handler(commands=['questionnaire'])
def quest(message):
    logger.log_info(f"Пользователь {message.from_user.id} начал заполнение анкеты командой /questionnaire")
    start_questionnaire(message)


@bot.message_handler(commands=['connect'])
def connect_but(message):
    logger.log_info(f"Пользователь {message.from_user.id} запустил процесс поиска новой группы командой /connect")
    checker = base.find_group(message.from_user.id)
    if checker == None:
        base.create_group(message.from_user.id)
    else:
        base.add_to_group(checker, message.from_user.id)


@bot.message_handler(commands=['help'])
def help_com(message):
    msg = 'Список доступных команд: \n /start - запуск бота \n ' \
          '/questionnaire - пройти анкетирование/изменить ответы \n /info - узнать данные о себе, свои группы \n'\
          ' /connect - запустить процесс поиска новой группы \n /menu - все функции в виде кнопок'
    logger.log_info(f"Пользователь {message.from_user.id} запросил список команд командой /help")
    bot.send_message(message.chat.id, msg)

@bot.message_handler()
def talk(message):
    dict_checker = ['id', 'хочу узнать свой id', 'выведи мой id', 'какой мой id?', 'какой мой id']
    logger.log_info(f"Получено сообщение от пользователя {message.from_user.id}: {message.text}")

    if message.text.lower() == 'привет':
        if message.from_user.last_name == None:
            bot.reply_to(message, f'Привет, {message.from_user.first_name}')
            bot.send_message(message.chat.id, 'Чем могу быть сегодня полезен?')
        else:
            bot.reply_to(message, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
            bot.send_message(message.chat.id, 'Чем могу быть сегодня полезен?')

    elif message.text.lower() in dict_checker:
        bot.reply_to(message, f'Ваш ID: {message.from_user.id}')


bot.infinity_polling()