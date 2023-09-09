import string
from logging import Logger

from telebot import TeleBot
from telebot.types import Message

from fair.config import MessagesConfig
from fair.db import DBAdapter, DBError

from fair.bot.states import ManagerStates


# Reward user for completing a task at the location, only for managers

# 1. Show the list of players in the queue with pages (10 players per page)
# 2. Choose a player from the list
# 3. Ask for a reward amount with pre-defined templates (e.g. 10, 20, 30, 50, 100), custom amounts are questionable


def reward_handler(
        message: Message,
        bot: TeleBot,
        messages: MessagesConfig,
        db_adapter: DBAdapter,
        logger: Logger,
        **kwargs):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        current_player_id = data.get("current_player_id", None)                                         # TODO: add current_player_id to state payload
        try:
            player = db_adapter.get_player_by_id(current_player_id)
        except DBError as e:
            logger.error(e)
            bot.send_message(message.chat.id, messages.unknown_error)
            return
        else:
            if player is not None:
                amount = int(message.text)
                try:
                    balance_status = db_adapter.reward_by_player_id(current_player_id, amount)
                except DBError as e:
                    logger.error(e)
                    bot.send_message(message.chat.id, messages.unknown_error)
                    return
                else:
                    if balance_status:
                        bot.send_message(message.chat.id, messages.purchase_amount)                             # TODO: add purchase_amount message
                        bot.set_state(message.from_user.id, ManagerStates.main_menu, message.chat.id)
                    else:
                        bot.send_message(message.chat.id, messages.bad_player_balance)                          # TODO: add bad_player_balance message
            else:
                bot.send_message(message.chat.id, messages.bad_chosen_player)                                   # TODO: add bad_player_balance message


def register_handlers(bot: TeleBot):
    bot.register_message_handler(
        reward_handler,
        state=ManagerStates.choose_purchase_amount,
        pass_bot=True,
        is_digit=True
    )