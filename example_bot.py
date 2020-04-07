#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import warnings

import config
import megach

megach.debug = False

if megach.debug is True:
    warnings.simplefilter("always")


#################
# RoomManager #
#################


class ExampleBot(megach.RoomManager):

    def onInit(self):
        # Auto Start
        config.Tools.auto_start(self)

        # Automatic tasks
        self.setInterval(900, config.Tools.auto_tasks)

    def onMessage(self, room, user, message):
        # Print message.
        config.StylePrint.safe_print_bot(self, room, user, message, "")

        # Do cmd or auto answer.
        config.Tools.answer_pm_rooms(self, room, user, message)

    def onPMMessage(self, pm, user, message):
        # Print message.
        status = config.Database.take_lang_bot(config.Bot.bot_lang, "on_pm_message_online")
        config.StylePrint.safe_print_bot(self, pm, user, message, status)

        # Do cmd or auto answer.
        config.Tools.answer_pm_rooms(self, pm, user, message)

    def onPMOfflineMessage(self, pm, user, message):
        # Print message.
        status = config.Database.take_lang_bot(config.Bot.bot_lang, "on_pm_message_offline")
        config.StylePrint.safe_print_bot(self, pm, user, message, status)

    def onPMMessageSend(self, pm, user, message):
        # Print message.
        status = config.Database.take_lang_bot(config.Bot.bot_lang, "on_pm_message_send")
        config.StylePrint.safe_print_bot(self, pm, user, message, status)

#######
# End #
#######
