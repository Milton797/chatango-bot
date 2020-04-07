#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import time

import config

####################
#   Special_Defs   #
####################


"""
FOR_ROOMS
"""


def onConnect(self, room):
    try:
        text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_connect")
        u = config.Tools.user_showname(room.user.name)
        print(
            text.format(
                config.StylePrint.time_now()[0],
                config.StylePrint.user_room_style(room.name.title()),
                config.StylePrint.user_room_style(u)
            )
        )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onDisconnect(self, room):
    try:
        if self._running is True:
            text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_disconnect")
            u = config.Tools.user_showname(room.user.name)
            print(
                text.format(
                    config.StylePrint.time_now()[0],
                    config.StylePrint.user_room_style(room.name.title()),
                    config.StylePrint.user_room_style(u)
                )
            )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onReconnect(self, room):
    try:
        text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_reconnect")
        u = config.Tools.user_showname(room.user.name)
        print(
            text.format(
                config.StylePrint.time_now()[0],
                config.StylePrint.user_room_style(room.name.title()),
                config.StylePrint.user_room_style(u),
                room.attempts
            )
        )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onLoginFail(self, args):
    try:
        text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_login_fail")
        if args.name != self.pm.name:
            if args.name in config.Database.rooms.keys():
                config.Database.erase_room(args.name)
                status_deleted = True
            else:
                status_deleted = False
        else:
            status_deleted = text[2].format(args.name)
        print(
            text[0].format(
                config.StylePrint.time_now()[0],
                config.StylePrint.user_room_style(args.name.title()),
                text[1][0] if status_deleted is not False else text[1][1]
            )
        )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onLoginRequest(self, room):
    try:
        text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_login_request")
        print(
            text.format(
                config.StylePrint.time_now()[0],
                config.StylePrint.user_room_style(room.name.title())
            )
        )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onJoin(self, room, user, ssid):
    try:
        if self._running is True:
            if config.Bot.see_users_p is True:
                text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_join")
                print(
                    text.format(
                        config.StylePrint.time_now()[0],
                        config.StylePrint.user_room_style(room.name.title()),
                        config.StylePrint.user_room_style(config.Tools.user_showname(user.name))
                    )
                )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onLeave(self, room, user, ssid):
    try:
        if self._running is True:
            if config.Bot.see_users_p is True:
                text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_leave")
                print(
                    text.format(
                        config.StylePrint.time_now()[0],
                        config.StylePrint.user_room_style(room.name.title()),
                        config.StylePrint.user_room_style(config.Tools.user_showname(user.name))
                    )
                )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onAnonJoin(self, room, user, ssid):
    try:
        if self._running is True:
            if config.Bot.see_anons_p is True:
                text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_anon_join")
                print(
                    text.format(
                        config.StylePrint.time_now()[0],
                        config.StylePrint.user_room_style(room.name.title()),
                        config.StylePrint.user_room_style(config.Tools.user_showname(user.name))
                    )
                )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onAnonLeave(self, room, user, ssid):
    try:
        if self._running is True:
            if config.Bot.see_anons_p is True:
                text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_anon_leave")
                print(
                    text.format(
                        config.StylePrint.time_now()[0],
                        config.StylePrint.user_room_style(room.name.title()),
                        config.StylePrint.user_room_style(config.Tools.user_showname(user.name))
                    )
                )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onUserLogin(self, room, user, puid):
    try:
        if self._running is True:
            if config.Bot.see_users_p is True:
                text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_user_login")
                print(
                    text.format(
                        config.StylePrint.time_now()[0],
                        config.StylePrint.user_room_style(room.name.title()),
                        config.StylePrint.user_room_style(config.Tools.user_showname(user.name))
                    )
                )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onUserLogout(self, room, user, puid):
    try:
        if self._running is True:
            if config.Bot.see_users_p is True:
                text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_user_logout")
                print(
                    text.format(
                        config.StylePrint.time_now()[0],
                        config.StylePrint.user_room_style(room.name.title()),
                        config.StylePrint.user_room_style(config.Tools.user_showname(user.name))
                    )
                )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onAnonLogin(self, room, user, ssid):
    try:
        if self._running is True:
            if config.Bot.see_anons_p is True:
                text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_anon_login")
                print(
                    text.format(
                        config.StylePrint.time_now()[0],
                        config.StylePrint.user_room_style(room.name.title()),
                        config.StylePrint.user_room_style(config.Tools.user_showname(user.name))
                    )
                )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onMessageDelete(self, room, user, message):
    try:
        text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_message_delete")
        u = config.Tools.user_showname(user.name)
        print(
            text.format(
                config.StylePrint.time_now()[0],
                config.StylePrint.user_room_style(room.name.title()),
                config.StylePrint.user_room_style(u), message.body
            )
        )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onDeleteUser(self, room, user, msgs):
    try:
        text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_message_delete_user")
        u = config.Tools.user_showname(user.name)
        print(
            text.format(
                config.StylePrint.time_now()[0],
                config.StylePrint.user_room_style(room.name.title()),
                config.StylePrint.user_room_style(u),
                "\n".join(
                    ["【%s】┇【%s】┇【%s】┇【%s】: %s" %
                     (time.strftime(config.Bot.hour_format, time.localtime(x.time)),
                      config.StylePrint.user_room_style(x.room.name.title()),
                      config.StylePrint.user_room_style(config.Tools.user_showname(x.user.name)),
                      config.StylePrint.channel_tipe(x), x) for x in reversed(msgs)]
                )
            )
        )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onFloodWarning(self, room):
    try:
        if room.name != self.pm.name:
            dic = config.Database.take_room(room.name)
            text = config.Database.take_lang_room(dic["lang"], "on_flood_warning")
            room.setSilent(True)
            self.setTimeout(30, room.setSilent, False)
            self.setTimeout(31, config.Tools.answer_room_pm, room, text[0], True)
        else:
            text = config.Database.take_lang_room(config.Bot.bot_lang, "on_flood_warning")
            print(text[1])
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onFloodBan(self, room, tiempo):
    try:
        text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_flood_ban")
        print(
            text[0].format(
                config.StylePrint.time_now()[0],
                config.StylePrint.user_room_style(room.name.title()),
                time.strftime("%I:%M:%S:%p|%d/%m/%Y", time.localtime(time.time() + tiempo))
            )
        )
        self.setTimeout(
            tiempo, print, text[1].format(
                config.StylePrint.time_now()[0],
                config.StylePrint.user_room_style(room.name.title())
            )
        )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onFloodBanRepeat(self, room, tiempo):
    try:
        text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_flood_ban_repeat")
        print(
            text[0].format(
                config.StylePrint.time_now()[0],
                config.StylePrint.user_room_style(room.name.title()),
                time.strftime("%I:%M:%S:%p|%d/%m/%Y", time.localtime(time.time() + tiempo))
            )
        )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


"""
FOR_PM
"""


def onPMConnect(self, pm):
    try:
        text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_pm_connect")
        u = config.Tools.user_showname(pm.currentname)
        print(
            text.format(
                config.StylePrint.time_now()[0],
                config.StylePrint.user_room_style(u)
            )
        )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))


def onPMDisconnect(self, pm):
    try:
        if self._running is True:
            text = config.Database.take_lang_bot(config.Bot.bot_lang, "on_pm_disconnect")
            u = config.Tools.user_showname(pm.currentname)
            print(
                text.format(
                    config.StylePrint.time_now()[0],
                    config.StylePrint.user_room_style(u)
                )
            )
    except (Exception, BaseException):
        return "Error: {}".format(str(config.Tools.error_def()))

######
# Fin #
######
