from telebot import TeleBot

from fair.config import ButtonsConfig

from fair.bot.handlers import (
    basic_commands_flow,
    player_registration_flow,
    manager_registration_flow,
)


def register_handlers(bot: TeleBot, buttons: ButtonsConfig):
    # register all handlers here
    basic_commands_flow.register_handlers(bot, buttons)
    player_registration_flow.register_handlers(bot)
    manager_registration_flow.register_handlers(bot)
